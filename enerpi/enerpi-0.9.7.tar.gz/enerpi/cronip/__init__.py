#!/venv/bin/python
# -*- coding: utf-8 -*-
"""
# Este script está preparado para ejecutarse poco después del boot y notificar
por email su situación en la red (LAN/WAN).
"""
import datetime as dt
import logging
import os
import psutil
import re
import smtplib
import socket
import subprocess
import sys
import time
import yaml

VERBOSE = True
WAIT_INIT = 60
TIME_PAUSE = 5

BASEDIR = os.path.dirname(os.path.abspath(__file__))
PATH_SECRETS = os.path.join(BASEDIR, 'secrets.yaml')

LOG_LEVEL = 'INFO'  # 'DEBUG'
LOG_FILE = os.path.join(BASEDIR, 'cronip.log')
EXT_IP_FILE = os.path.join(BASEDIR, 'external_ip.txt')

# Configuration
with open(PATH_SECRETS) as _file:
    SECRETS = yaml.load(_file.read())
EMAIL_TARGET = SECRETS['email_target']
EMAIL_SERVER_USER = SECRETS['email_server']
EMAIL_SERVER_PWD = SECRETS['email_server_pw']
EMAIL_INITS = SECRETS.get('email_inits', False)
EMAIL_DEBUG = None
if 'debug_mode' in SECRETS:
    EMAIL_DEBUG = SECRETS['debug_mode']

def _get_cmd_output(cmd, default=None, verbose=True, **kwargs):
    list_cmd = cmd.split()
    # kwargs.update({'stdout': subprocess.PIPE})
    try:
        out = subprocess.check_output(list_cmd, **kwargs).decode()
        if out.endswith('\n'):
            return True, out[:-1]
        return True, out
    except subprocess.TimeoutExpired as e:
        time.sleep(TIME_PAUSE / 2)
        if verbose:
            print(
                '\nERROR subprocess.CalledProcessError: {} invocando el comando: {}'.format(
                    e, cmd))
    except subprocess.CalledProcessError as e:
        if verbose:
            print(
                '\nERROR subprocess.CalledProcessError: {} invocando el comando: {}'.format(
                    e, cmd))
    except FileNotFoundError as e:
        if verbose:
            print(
                '\nERROR FileNotFoundError: {} invocando el comando: {}'.format(
                    e, cmd))
    if default:
        return False, default
    return False, 0


def send_email(email_subject, email_content, target):
    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(EMAIL_SERVER_USER, EMAIL_SERVER_PWD)
        email = 'To: {}\nFrom: {}\nSubject: {}\n\n{}\n'.format(
            target, EMAIL_SERVER_USER, email_subject, email_content)
        smtpserver.sendmail(EMAIL_SERVER_USER, target, email.encode())
        smtpserver.close()
        logging.info('EMAIL SENDED={}'.format(email_subject))
        return True
    except smtplib.SMTPException as e:
        logging.error(
            'EMAIL NOT SENDED={}; SMTPException: {}'.format(email_subject, e))
    except socket.gaierror as e:
        logging.error(
            'EMAIL NOT SENDED={}; socket.gaierror: {}; '
            '¿Hay conexión a internet??'.format(email_subject, e))
    except Exception as e:
        logging.error(
            'EMAIL NOT SENDED={}; Exception: {}'.format(email_subject, e))
    return False


def _notify_email(d_result, extra_info=False, with_email=False):
    email_subject = 'RPI {} started! [IP: {}, {}]'.format(
        d_result['name'], d_result['ip_ext'], d_result['IP'])
    confs = ['name', 'user', 'path_home', 'IP']
    info_host = '\n'.join(
        ['  -> {:10} : {}'.format(k.upper(), d_result[k]) for k in confs])
    if extra_info:
        template = 'Configuración:\n{}\n\n**IP EXTERNA**: {}\n' \
                   '(Obtención en {:.3f} segs)\n\nIFCONFIG:\n{}'
        email_content = template.format(
            info_host, d_result['ip_ext'],
            d_result['time_ip_ext'], d_result['ifconfig'])
    else:
        template = 'Configuración:\n{}\n\n**IP EXTERNA**: {}\n' \
                   '(Obtención en {:.3f} segs)'
        email_content = template.format(
            info_host, d_result['ip_ext'], d_result['time_ip_ext'])
    if 'location_info' in d_result:
        email_content += '\n\nLocation:\t{}\n'.format(
            d_result['location_info'])

    ok_email = True
    if with_email and (EMAIL_TARGET is not None) and EMAIL_INITS:
        ok_email = send_email(email_subject, email_content, EMAIL_TARGET)
        if ok_email:
            logging.debug(
                'SALIDA OK de name:{}, file:{}'.format(__name__, __file__))
        else:
            logging.debug(
                'SALIDA SIN NOTIFICAR POR EMAIL de name:{}, file:{}'.format(
                    __name__, __file__))
    if ok_email and (EMAIL_DEBUG is not None):
        send_email(email_subject, email_content, EMAIL_DEBUG)


def get_machine_info(verbose):
    # Machine
    # NAME, IP, USER, IS_MAC, NUM_CPU, BOOT_TIME
    regexpr_ifconfig = re.compile(
        r'inet (addr:)?(?P<IP>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) ')
    # regexpr_IP = re.compile(r'(?P<IP1>\d{1,3})\.(?P<IP2>\d{1,3})\.
    # (?P<IP3>\d{1,3})\.(?P<IP4>\d{1,3})')

    def _extract_ifconfig(res_ifconfig):
        # IP(s) de la máquina local:
        busqueda = regexpr_ifconfig.findall(res_ifconfig)
        ips_locales = [b[1] for b in busqueda if b[1] != '127.0.0.1']
        return ips_locales

    # Nombre, tipo, user de la máquina local:
    is_mac = True if sys.platform == 'darwin' else False
    ok_name, name = _get_cmd_output('/bin/hostname', default='rpi')
    ok_current_user, current_user = _get_cmd_output(
        '/usr/bin/id -u -n', default='pi')
    # IP(s) de la máquina local:
    ok_ifconfig_output, ifconfig_output = _get_cmd_output(
        '/sbin/ifconfig', default='IFCONFIG No disponible')
    # ok_iwconfig_output, iwconfig_output = _get_cmd_output('/sbin/iwconfig wlan0',
    #  default='IWCONFIG No disponible', verbose=False)
    ip, hay_conexion, ips_lan = '127.0.0.1', False, []
    if ok_ifconfig_output:
        ips_lan = _extract_ifconfig(ifconfig_output)
        if len(ips_lan) > 0:
            ip = ips_lan[0]
            hay_conexion = True
    dict_machine = {'is_mac': is_mac, 'name': name, 'user': current_user,
                    'hay_conexion': hay_conexion, 'IP': ip,
                    'IPs': ips_lan, 'n_IPs': len(ips_lan),
                    'nCPU': (
                    psutil.cpu_count(), psutil.cpu_count(logical=False)),
                    'boot_time': dt.datetime.fromtimestamp(psutil.boot_time())}
    # if ok_iwconfig_output:
    #     dict_machine['iwconfig'] = iwconfig_output
    dict_machine['ifconfig'] = ifconfig_output
    # dict_machine['usb_devices'] = get_usb_devices()
    if verbose:
        [print('{0}:\t{1}'.format(k, v)) for k, v in dict_machine.items()]
    return dict_machine


def get_ext_ip(timeout=10):
    tic = time.time()
    n_retry = 0
    ok, ip, time_obtain, location_info = False, '', 1e6, None
    while n_retry < 2:
        # ok, ip_ext = _get_cmd_output('/usr/bin/curl ifconfig.me', default=None, timeout=timeout)
        # ok, ip_ext = _get_cmd_output('wget http://ipinfo.io/ip -qO -', default=None, timeout=timeout)

        ok = location_info is not None
        if ok:
            ip_ext = location_info.ip
        # print('Intento de ip_ext: {}'.format(ip_ext))
        toc = time.time()
        if ok:
            # ip = ip_ext[:-1]
            ip = ip_ext
        time_obtain = toc - tic

        try:
            with open(EXT_IP_FILE) as file_ip:
                old_ip = file_ip.read()
        except FileNotFoundError:
            old_ip = ''

        if ok and (not old_ip or old_ip != ip_ext):
            with open(EXT_IP_FILE, 'w') as file_ip:
                file_ip.write(ip_ext)
                mascara = 'WRITING NEW EXT_IP in {}: {}. T_OBTENCIÓN: {:.2f} seg'
        elif not ok:
            mascara = 'ERROR EXT_IP ({}) TIMEOUT?: {}. T_OBTENCIÓN: {:.2f} seg'
            n_retry += 1
        else:
            mascara = 'OK EXT_IP ({}) NOT CHANGING: {}. T_OBTENCIÓN: {:.2f} seg'
            n_retry = 1000
        logging.debug(mascara.format(EXT_IP_FILE, ip, time_obtain))
    return ok, ip, location_info, time_obtain


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description='RPI START NOTIFY SERVICE')
    p.add_argument('-s', '--silent', action='store_true', help='HIDES OUTPUT')
    p.add_argument('-e', '--email', action='store_true', help='SENDS EMAIL')
    p.add_argument('-p', '--print', action='store_true', help='PRINT LOG FILE')
    p.add_argument('--extra', action='store_true', help='REPORT EXTRA INFO')
    p.add_argument('--delete', action='store_true', help='DELETE LOG FILE')
    p.add_argument('--nowait', action='store_true',
                   help="DON'T WAIT FOR NETWORK {} SECS".format(WAIT_INIT))
    args = p.parse_args()
    _verbose = not args.silent

    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                        datefmt='%d/%m/%Y %H:%M:%S',
                        format='%(levelname)s [%(filename)s_%(funcName)s] - %(asctime)s: %(message)s')

    if not args.nowait:
        time.sleep(WAIT_INIT)
    path_home = '/home/homeassistant'

    os.chdir(path_home)
    logging.debug('INIT CRONIP con path_home: {}'.format(path_home))

    if args.print:
        with open(LOG_FILE) as f:
            log_lines = f.readlines()
        print('LAST {} LOG ENTRIES:'.format(50))
        [print(l[:-1]) for l in log_lines[-50:]]
    elif args.delete:
        logging.info('LOG DELETED (SIZE=0) --> {}'.format(LOG_FILE))
        print('LOG DELETED (SIZE=0) --> {}'.format(LOG_FILE))
        with open(LOG_FILE, 'w') as f:
            f.write('')
    else:
        results = get_machine_info(_verbose)
        results.update({'path_home': path_home})
        ok_ip_ext, ext_ip, location_info, time_ip_ext = get_ext_ip()
        msg = 'RESULTADOS:\n{}\n--> IP_EXT: {} (OK: {}, TIME: {} seg), INFO: {}'
        msg = msg.format(results, ext_ip, ok_ip_ext, time_ip_ext, location_info)
        if _verbose:
            print(msg)
        logging.debug(msg)
        results.update({'hay_ip_ext': ok_ip_ext, 'ip_ext': ext_ip,
                        'time_ip_ext': time_ip_ext,
                        'location_info': location_info})
        if ok_ip_ext:
            _notify_email(results, args.extra, args.email)
        else:
            second_retry = 0
            while second_retry < 2 and not ok_ip_ext:
                logging.error(
                    'NO SE ENCUENTRA IP EXTERNA. IP: {}'.format(results['IP']))
                second_retry += 1
                time.sleep(TIME_PAUSE)
                ok_ip_ext, ext_ip, location_info, time_ip_ext = get_ext_ip(
                    timeout=15)
                results.update({'hay_ip_ext': ok_ip_ext, 'ip_ext': ext_ip,
                                'time_ip_ext': time_ip_ext})
            _notify_email(results, args.extra, args.email)
            logging.info('ENCONTRADA IP EXTERNA. IP: {}, INFO: {}'.format(
                results['ip_ext'], location_info))
        if ok_ip_ext:  # check HA location config
            time.sleep(WAIT_INIT / 2)
            _check_location(location_info, not args.silent)
