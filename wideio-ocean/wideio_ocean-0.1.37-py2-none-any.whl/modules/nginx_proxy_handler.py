import logging
import os
import subprocess
import sys

# ACME - https://github.com/diafygi/acme-tiny
LDAP_DISABLED = os.environ.get("OCEAN_LDAP_DISABLED")

NGINX_CONF = """
user www-data;
worker_processes 1;
#daemon off;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {{
    worker_connections  1024;
}}


http {{

    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    keepalive_timeout 65;
    proxy_read_timeout 200;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/html text/css text/xml
               application/x-javascript application/xml
               application/atom+xml text/javascript;

    # Only retry if there was a communication error, not a timeout
    # on the Tornado server (to avoid propagating "queries of death"
    # to all frontends)

    proxy_next_upstream error;

    {EXTRA_CONF}

    {SERVER_DEFS}
}}
"""

# NOTE: to be considered eventually - https://www.nginx.com/resources/admin-guide/nginx-tcp-ssl-upstreams/
PROXY_SERVER_DEF = """
    server {{
       {LISTEN_PORT}
       server_name {SERVER_NAME};

       {SSL_DEFS}

        # Allow file uploads
        client_max_body_size 50M;

       {LOCATIONS}

       location / {{
          proxy_pass {PROXY_URL};
          proxy_set_header  Host              $http_host;   #
          proxy_set_header  X-Real-IP         $remote_addr; # pass on real client's IP
          proxy_set_header  X-Forwarded-For   $proxy_add_x_forwarded_for;
          proxy_set_header  X-Forwarded-Proto $scheme;
          proxy_set_header  X-Forwarded-Host  $http_host; # tomcat
          proxy_read_timeout                  900;
          {EXTRA}
       }}
    }}
"""

STATIC_SERVER_DEF = """
    server {{
       {LISTEN_PORT}
       server_name {SERVER_NAME};

       {SSL_DEFS}

       {LOCATIONS}

       location / {{
          root {ROOT};
          {EXTRA}
       }}
    }}
"""

SSL_DEFS = """
    ssl                  on;
    ssl_certificate      {CERT};
    ssl_certificate_key  {KEY};

    # Recommendations from https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html
    ssl_protocols TLSv1.1 TLSv1.2;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
"""

NOT_SSL_DEFS = """
    if ($request_uri !~ ^/.well-known/acme-challenge/(.*)$) {
        return 301 https://$server_name$request_uri;
    }
"""

SSL_LOCS = """
location /.well-known/acme-challenge/ {
        alias /var/www/challenges/;
        try_files $uri =404;
}
"""


class NGINXProxyHandler(object):
    """
    Module to add routes to local containers in NGINX.
    Eventually also routing NGINX to serve correct static data for this domain.

    "nginx": [ { "name": "",
                 "port":"443",
                 "proxy":"http://${CONTAINER_IP}:80/" ,
                 "volumes":{"/media" : {}
                           }
                 },
                 "require":[],
                 "ssl": {"key":"xxxx","cert":"xxx"}
                 "extraargs": {
                    ## a few additional -v may be requires
                    "-v "
                 }
             ]
    """

    @classmethod
    def on_ocean_start(cls, ocean):
        """Ensures that we have an updated manifest for nginx."""
        cls._ocean = ocean
        cls._ocean.manifest.setdefault("local-system", {})
        cls._ocean.manifest["local-system"]["nginx"] = {
            "dockerimg": "h3nrik/nginx-ldap",
            "expose": ["80:80", "443:443"],
            "requires": [],
            "with_ssl": True,  # < get a dummy certificate for websites not specifying their certificate
            "extraargs": [
                "--net=host",
                "-v " + cls._ocean.MPL + "/cfg/nginx/nginx.conf:/etc/nginx/nginx.conf:ro",
                "-v " + cls._ocean.MPL + "/var/log/nginx:/var/log/nginx",
                "-v " + cls._ocean.MPL + "/cfg/nginx/challenges:/var/www/challenges",
                "-v " + os.path.join(cls._ocean.MPL, "hosts") + ":/etc/hosts"
            ]
        }
        cls._ocean.manifest["local-system"]["no-run"] = {
            "no-run": True,
            "no-container": True,
            "requires": []
        }
        cls._update_manifest_nginx()

    @classmethod
    def on_pre_start(cls, name, *args):
        """Apply patch to run before nginx actually starts."""
        if name in ["nginx"]:
            if "-or" not in args:
                cls._ocean.start(name, *(args + ("-or",)))
                cls._rewrite_conf()
                cls._update_manifest_nginx()
                cls._ocean._alt_fullyconnect()

    @classmethod
    def update_nginx(cls):
        """ Command to rewirte the configuration. """
        cls._rewrite_conf()
        # TODO: KILL -HUP if running

    @classmethod
    def _rewrite_conf(cls):
        """
        Rewrite the nginx.conf file.
        """
        server_defs = []
        extra_conf = []
        for c in cls._ocean.manifest.items():
            for sn in c[1].keys():
                s = cls._ocean._get(sn)
                if ("nginx" in s) and (s.get("no_run", False) or cls._ocean.is_started(sn)):
                    snginx = s["nginx"]
                    if isinstance(snginx, dict):
                        snginx = [snginx]
                    for sdef in snginx:
                        use_ssl = s.get("use_ssl")
                        locations = []
                        ssl_defs = ""
                        ssl_options = {
                            "CERT": "/.cert.pem",
                            "KEY": "/.key.pem"
                        }
                        server_port = ["80"]
                        if use_ssl:
                            server_port = ["80", "443 ssl"]
                            ssl_defs = SSL_DEFS.format(**ssl_options)
                            locations.append(SSL_LOCS)
                        sname = sdef.get("server_name", " ".join(s.get("cnames", "")))
                        if (len(sname)) and "proxy_url" in sdef:
                            for p in server_port:
                                server_defs.append(PROXY_SERVER_DEF.format(
                                    SERVER_NAME=sname,
                                    SSL_DEFS=(ssl_defs if "ssl" in p else NOT_SSL_DEFS),
                                    LISTEN_PORT="\n".join(["listen %s;" % (p,)]),
                                    LOCATIONS="\n".join(locations) + sdef.get("extra", ""),
                                    PROXY_URL=sdef["proxy_url"],
                                    EXTRA=sdef.get("extra_main_server", "")
                                ))
                        elif (len(sname)) and "static" in sdef:
                            for p in server_port:
                                server_defs.append(STATIC_SERVER_DEF.format(
                                    SERVER_NAME=sname,
                                    SSL_DEFS=(ssl_defs if "ssl" in p else ""),
                                    LISTEN_PORT="\n".join(["listen %s;" % (p,)]),
                                    LOCATIONS="\n".join(locations),
                                    ROOT="/static/" + sn,
                                    EXTRA=sdef.get("extra_main_server", "")
                                ))
                        elif "custom_server" in sdef:
                            server_defs.append(sdef["custom_server"])
                        else:
                            logging.warning("Unsupported NGINX section in %s" % (sn,))
                        if "extra_conf" in sdef:
                            extra_conf.append(sdef["extra_conf"])

        config = NGINX_CONF.format(
            SERVER_DEFS="\n".join(
                server_defs
            ),
            EXTRA_CONF="\n".join(
                extra_conf
            )
        )

        cfg = cls._ocean._get_cfgp("nginx")
        if not os.path.exists(cfg):
            os.mkdir(cfg)

        open(os.path.join(cfg, "nginx.conf"), "wb").write(config.encode('utf8'))

        return config

    @classmethod
    def _get_all_cnames(cls, with_srv=False, all=False):
        """
        Return the cnames associated with all the hosts and additional cnames from environment.
        """
        cnames = []
        extras = os.environ.get("OCEAN_EXTRA_CERT_NAMES", "")

        if len(extras):
            if with_srv:
                cnames = [x.split(":") for x in extras.split(",")]
            else:
                cnames = extras.split(",")

        for c in cls._ocean.manifest.items():
            for sn in c[1].keys():
                s = cls._ocean._get(sn)
                if "cnames" in s and (all or ("nginx" in s and "use_ssl" in s and s["use_ssl"])):
                    if with_srv:
                        for cname in s["cnames"]:
                            cnames.append((sn, cname))
                    else:
                        cnames += s["cnames"]
        return cnames

    @classmethod
    def _build_csr_for_all_cnames(cls):
        """Prepare a CSR for all the CNAMEs that we want to cover with the certificate."""
        cfg = cls._ocean._get_cfgp("nginx")
        key = os.path.join(cfg, "key")
        csr = os.path.join(cfg, "csr")
        sanconfigfn = os.path.join(cfg, "sanconfig")
        all_cnames = cls._get_all_cnames()
        sanconfig = open("/etc/ssl/openssl.cnf").read()
        sanconfig += "[SAN]\nsubjectAltName=" + ",".join(["DNS:%s" % (n,) for n in all_cnames if len(n)])
        open(sanconfigfn, "wb").write(sanconfig.encode('utf8'))
        p = subprocess.Popen("openssl req -new -sha256 -key {key} -subj \"/\" -reqexts SAN -config {config}".format(
            key=key,
            config=sanconfigfn
        ),
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = p.communicate()
        if (e):
            sys.stderr.write(e.decode('utf8'))
        open(csr, "wb").write(o)

    @classmethod
    def _acme_get_cert(cls):
        """Obtain the certificate from let's encrypt."""
        # "python acme_tiny.py --account-key ./account.key --csr ./domain.csr"
        from acme_tiny import get_crt
        cfg = cls._ocean._get_cfgp("nginx")
        if not os.path.exists(cfg):
            os.mkdir(cfg)

        accountkey = os.path.join(cfg, "accountkey")
        csr = os.path.join(cfg, "csr")
        cert = os.path.join(cfg, "cert")
        challenges = os.path.join(cfg, "challenges")
        if not os.path.exists(challenges):
            os.mkdir(challenges)

        if not os.path.exists(accountkey):
            os.system("openssl genrsa 4096 > " + accountkey)

        if cls._ocean._get_config("LETSENCRYPT_ENV", "prod") == "prod":
            ca = "https://acme-v01.api.letsencrypt.org"
        else:
            ca = "https://acme-staging.api.letsencrypt.org"

        acme_log = logging.getLogger("acme-log")
        acme_log.addHandler(logging.StreamHandler())
        acme_log.setLevel(logging.INFO)

        signed_crt = get_crt(accountkey, csr, challenges, log=acme_log, CA=ca)
        intermediate_crt = open(os.path.join(cls._ocean.MP, "lets-encrypt-x3-cross-signed.pem")).read()
        open(cert, "wb").write((signed_crt + intermediate_crt).encode("utf8"))
        open(cert + ".letsencrypt", "wb").write((signed_crt + intermediate_crt).encode("utf8"))

    @classmethod
    def nginx_lets_encrypt_init(cls):
        """Initialise the let's encrypt certificate."""
        assert (cls._ocean.is_started("nginx"))
        cls._build_csr_for_all_cnames()
        cls._acme_get_cert()
        cls._ocean.restart("nginx")

    @classmethod
    def nginx_lets_encrypt_update(cls):
        """Renew the let's encrypt certificate."""
        assert (cls._ocean.is_started("nginx"))
        cls._acme_get_cert()
        cls._ocean.restart("nginx")

    @classmethod
    def _update_manifest_nginx(cls):
        """Update the manifest section for nginx based on the rest of the current manifest."""
        for c in cls._ocean.manifest.items():
            for sn, s in c[1].items():
                if "nginx" in s:
                    snginx = s["nginx"]
                    if isinstance(snginx, dict):
                        snginx = [snginx]
                    for sdef in snginx:
                        extraargs = sdef.get("extraargs", [])
                        if "static" in sdef:
                            ea = "-v %s:%s" % (os.path.join(cls._ocean.MPL, "src", c[0], sn), "/static/" + sn)
                            if ea not in extraargs:
                                extraargs.append(ea)
                        if extraargs:
                            for e in extraargs:
                                if e not in cls._ocean.manifest["local-system"]["nginx"]["extraargs"]:
                                    cls._ocean.manifest["local-system"]["nginx"]["extraargs"].append(e)
                    if (sn not in cls._ocean.manifest["local-system"]["nginx"]["requires"]
                            and ("static" not in snginx[0] and "no_run" not in snginx[0])):
                        cls._ocean.manifest["local-system"]["nginx"]["requires"].append(sn)
                if sn != "no-run" and ("no-run" in s or "no_run" in s or "no-container" in s) and (not s.get("requires")):
                    if s.get("type", "service") != "environment":
                        cls._ocean.manifest["local-system"]["no-run"]["requires"].append(sn)

    @classmethod
    def nginx_all_cnames(cls):
        return '\n'.join(["%s : %s" % t for t in sorted(filter(lambda x: len(x[1]),
                                                               cls._get_all_cnames(with_srv=True, all=True)))])
        # return '\n'.join(sorted( cls._get_all_cnames(with_srv=True)))


__handler__ = NGINXProxyHandler
