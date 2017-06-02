import os
import shutil

# BASED ON:
# https://jamielinux.com/docs/openssl-certificate-authority/
# http://gagravarr.org/writing/openssl-certs/errors.shtml


DEFAULT_ORGANISATION = {
    'country': 'GB',
    'state': 'England',
    'location': 'London',
    'organisaton': 'WIDE IO Ltd',
    'unit': 'Development team'
}

BASEDIR = os.environ.get("CABASEDIR", os.path.expanduser("/tmp"))
CADIRECTORY = os.path.join(BASEDIR, ".virtca")
CERTSDIRECTORY = os.path.join(BASEDIR, ".certs")
system = os.system

OPENSSL_CONFIG = """
[ ca ]
default_ca = CA_default

[ CA_default ]
# Directory and file locations.
dir               = {CADIRECTORY}
certs             = $dir/certs
crl_dir           = $dir/crl
new_certs_dir     = $dir/newcerts
database          = $dir/index.txt
serial            = $dir/serial
RANDFILE          = $dir/private/.rand

# The root key and root certificate.
private_key       = $dir/private/{NAME}.key.pem
certificate       = $dir/certs/{NAME}.cert.pem

# For certificate revocation lists.
crlnumber         = $dir/crlnumber
crl               = $dir/crl/{NAME}.crl.pem
crl_extensions    = crl_ext
default_crl_days  = 30

# SHA-1 is deprecated, so use SHA-2 instead.
default_md        = sha256

name_opt          = ca_default
cert_opt          = ca_default
default_days      = 375
preserve          = no
policy            = policy_{POLICY}

[ policy_strict ]
# The root CA should only sign intermediate certificates that match.
# See the POLICY FORMAT section of `man ca`.
countryName             = match
stateOrProvinceName     = match
organizationName        = match
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ policy_loose ]
# Allow the intermediate CA to sign a more diverse range of certificates.
# See the POLICY FORMAT section of the `ca` man page.
countryName             = optional
stateOrProvinceName     = optional
localityName            = optional
organizationName        = optional
organizationalUnitName  = optional
commonName              = supplied
emailAddress            = optional

[ req ]
# Options for the `req` tool (`man req`).
default_bits        = 2048
distinguished_name  = req_distinguished_name
string_mask         = utf8only

# SHA-1 is deprecated, so use SHA-2 instead.
default_md          = sha256

# Extension to add when the -x509 option is used.
x509_extensions     = v3_ca

[ req_distinguished_name ]
# See <https://en.wikipedia.org/wiki/Certificate_signing_request>.
countryName                     = Country Name (2 letter code)
stateOrProvinceName             = State or Province Name
localityName                    = Locality Name
0.organizationName              = Organization Name
organizationalUnitName          = Organizational Unit Name
commonName                      = Common Name
emailAddress                    = Email Address

# Optionally, specify some defaults.
countryName_default             = {country}
stateOrProvinceName_default     = {state}
localityName_default            = {location}
0.organizationName_default      = {organisaton}
#organizationalUnitName_default =
#emailAddress_default           =

[ v3_ca ]
# Extensions for a typical CA (`man x509v3_config`).
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ v3_intermediate_ca ]
# Extensions for a typical intermediate CA (`man x509v3_config`).
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, digitalSignature, cRLSign, keyCertSign

[ usr_cert ]
# Extensions for client certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = client, email
nsComment = "OpenSSL Generated Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = clientAuth, emailProtection

[ server_cert ]
# Extensions for server certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = server
nsComment = "OpenSSL Generated Server Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer:always
keyUsage = critical, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth

[ multi_cert ]
# Extensions for server + client certificates (`man x509v3_config`).
basicConstraints = CA:FALSE
nsCertType = server, client, email
nsComment = "OpenSSL Generated Server+Client Certificate"
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth, emailProtection


[ crl_ext ]
# Extension for CRLs (`man x509v3_config`).
authorityKeyIdentifier=keyid:always

[ ocsp ]
# Extension for OCSP signing certificates (`man ocsp`).
basicConstraints = CA:FALSE
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, OCSPSigning
"""

KEYENCRYPT = " -aes256"
KEYENCRYPT = ""


class CA:
    """
    Implements a simple Certificate Authority system for OpenSSL
    the code is based on https://jamielinux.com/docs/openssl-certificate-authority/
    """

    def __init__(self, directory=CADIRECTORY, certs=CERTSDIRECTORY, autoreset=False, verbose=True, validate=True):
        self.verbose = verbose
        self.validate = validate
        self.deploy = (certs is not None)
        self.directory = directory
        self.idirectory = os.path.join(directory, "intermediate")
        self.certs = certs
        if os.path.exists(self.directory) and autoreset:
            shutil.rmtree(self.directory)
            shutil.rmtree(self.certs)
        if not os.path.exists(self.certs):
            os.mkdir(self.certs)

    def create_rootpair(self):
        os.mkdir(self.directory)
        os.chdir(self.directory)
        os.mkdir("certs")
        os.mkdir("crl")
        os.mkdir("csr")
        os.mkdir("newcerts")
        os.mkdir("private")
        system("chmod 700 private")
        open("index.txt", "wb").write("")
        open("serial", "wb").write("1000")
        open("crlnumber", "wb").write("1000")
        open("openssl_ca.cnf", "wb").write(
            OPENSSL_CONFIG.format(CADIRECTORY=self.directory,
                                  POLICY='strict',
                                  NAME='ca',
                                  **DEFAULT_ORGANISATION
                                  )
        )
        open("openssl_host.cnf", "wb").write(
            OPENSSL_CONFIG.format(CADIRECTORY=self.directory,
                                  POLICY='loose',
                                  NAME='ca',
                                  **DEFAULT_ORGANISATION
                                  )
        )
        # root key
        system("openssl genrsa %s -out private/ca.key.pem 4096" % (KEYENCRYPT,))
        system("chmod 400 private/ca.key.pem")
        # root certificate
        system("openssl req -config openssl_ca.cnf  -key private/ca.key.pem -new -x509 -days 7300 -sha256"
               " -extensions v3_ca -out certs/ca.cert.pem "
               "-subj \"/C=GB/ST=England/L=London/O=WIDE IO LTD/OU=WIDE IO Ltd Certificate Authority"
               "/CN=WIDE IO Ltd Root CA\""
               )
        system("chmod 444 certs/ca.cert.pem")
        system("cat certs/ca.cert.pem > ./certs/ca-chain.cert.pem")  # also allow direct signatures
        if self.verbose:
            system("openssl x509 -noout -text -in certs/ca.cert.pem")
        if self.deploy:
            shutil.copy2("certs/ca.cert.pem", os.path.join(self.certs, "ca.cert.pem"))
            system("c_rehash %s" % (self.certs,))

    def create_intermediate(self):
        os.mkdir(self.idirectory)
        os.chdir(self.idirectory)
        os.mkdir("certs")
        os.mkdir("crl")
        os.mkdir("csr")
        os.mkdir("newcerts")
        os.mkdir("private")
        system("chmod 700 private")
        open("index.txt", "wb").write("")
        open("serial", "wb").write("1000")
        open("crlnumber", "wb").write("1000")
        open("openssl_host.cnf", "wb").write(OPENSSL_CONFIG.format(CADIRECTORY=self.idirectory,
                                                                   POLICY='loose',
                                                                   NAME='intermediate',
                                                                   **DEFAULT_ORGANISATION))
        # root key
        system("openssl genrsa %s -out private/intermediate.key.pem 4096" % (KEYENCRYPT,))
        system("chmod 400 private/intermediate.key.pem")

        # intermediate csr
        system("openssl req -config openssl_host.cnf -new  -sha256 -out csr/intermediate.csr.pem  "
               "-key private/intermediate.key.pem -subj \"/C=GB/ST=England/L=London/O=WIDE IO LTD"
               "/OU=WIDE IO Ltd Certificate Authority/CN=WIDE IO Ltd intermediate CA\"")

        os.chdir(self.directory)
        system("openssl ca -batch -config openssl_ca.cnf -extensions v3_intermediate_ca -days 3650 -notext "
               "-md sha256 -in intermediate/csr/intermediate.csr.pem -out intermediate/certs/intermediate.cert.pem")
        system("chmod 444 intermediate/certs/intermediate.cert.pem")
        if self.verbose:
            system("openssl x509 -noout -text -in intermediate/certs/intermediate.cert.pem")
        if self.validate:
            system("openssl verify -CAfile certs/ca.cert.pem intermediate/certs/intermediate.cert.pem")
        system("cat intermediate/certs/intermediate.cert.pem certs/ca.cert.pem > intermediate/certs/ca-chain.cert.pem")
        # system("cat intermediate/certs/intermediate.cert.pem > intermediate/certs/ca-chain.cert.pem")
        system("chmod 444 intermediate/certs/ca-chain.cert.pem")
        if self.deploy:
            shutil.copy2("intermediate/certs/intermediate.cert.pem", os.path.join(self.certs, "intermediate.cert.pem"))
            system("c_rehash %s" % (self.certs,))

    def create_for_host(self, host="localhost", host_type="multi", days=365, organisaton=None, keyencrypt="",
                        authority=None):
        if organisaton is None:
            organisaton = DEFAULT_ORGANISATION

        if authority is None:
            if os.path.exists(self.idirectory):
                authority = "intermediate"
            else:
                authority = "."
        os.chdir(self.directory)
        system("openssl genrsa %s -out %s/private/%s.key.pem 2048" % (keyencrypt, authority, host))
        if len(keyencrypt):
            system("openssl rsa -in %s/private/%s.key.pem -out %s/private/%s.key-unc.pem" % (authority, host,
                                                                                             authority, host))

        system("chmod 400 %s/private/%s.key.pem" % (authority, host,))
        system("openssl req -config %s/openssl_host.cnf -key %s/private/%s.key.pem -new -sha256 "
               "-out %s/csr/%s.csr.pem -subj \"/C=%s/ST=%s/L=%s/O=%s/OU=%s/CN=%s\"" % (authority, authority,
                                                                                       host, authority, host,
                                                                                       organisaton['country'],
                                                                                       organisaton['state'],
                                                                                       organisaton['location'],
                                                                                       organisaton['organisaton'],
                                                                                       organisaton['unit'], host))
        system("openssl ca -batch -config %s/openssl_host.cnf -extensions %s_cert -days %d -notext -md sha256"
               " -in %s/csr/%s.csr.pem -out %s/certs/%s.cert.pem" % (authority, host_type, days, authority, host,
                                                                     authority, host))
        system("chmod 444 %s/certs/%s.cert.pem" % (authority, host,))

        if self.verbose:
            system("openssl x509 -noout -text -in %s/certs/%s.cert.pem" % (authority, host,))
        if self.validate:
            system("openssl verify -CAfile %s/certs/ca-chain.cert.pem %s/certs/%s.cert.pem" % (authority, authority,
                                                                                               host,))
            if self.deploy:
                system("openssl verify -CApath %s %s/certs/%s.cert.pem" % (self.certs, authority, host,))


if __name__ == "__main__":
    import sys
    host = "localhost"
    autoreset = False
    verbose = False
    host_type = "multi"
    ac = 1
    if sys.argv[ac] in ["-v", "-R", "-c", "-s"]:
        if sys.argv[ac] == "-v":
            verbose = True
        if sys.argv[ac] == "-R":
            autoreset = True
        if sys.argv[ac] == "-c":
            host_type = "client"
        if sys.argv[ac] == "-s":
            host_type = "server"
        ac += 1

    ca = CA(autoreset=autoreset, verbose=verbose)
    if not os.path.exists(ca.directory):
        ca.create_rootpair()

    if sys.argv[ac] == "-i":
        if not(os.path.exists(ca.idirectory)):
            ca.create_intermediate()
        ac += 1
    if len(sys.argv) > ac:
        host = sys.argv[ac]
    ca.create_for_host(host, host_type=host_type)
