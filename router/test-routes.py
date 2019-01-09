import subprocess
import argparse
import requests
import urllib3
from commons.constants import *

# ref.: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
urllib3.disable_warnings()


def init_parser():
    parser = argparse.ArgumentParser(description='check every route within an OpenShift cluster')
    parser.add_argument('-u', dest='user', help='the cluster user admin to login', default=SYSTEM_ADMIN)
    parser.add_argument('-p', dest='password', help='the cluster admin password')
    parser.add_argument('--url', dest='url', help='the cluster URL', default='https://localhost:8443')
    parser.add_argument('--skip-login', dest='skip_login', nargs='?', help='completely skip oc login (you must be logged in)', const=True, default=False)
    parser.add_argument('-k', dest='ignore_selfsign', nargs='?', help='ignores self-signed certificates when connecting to routes and OpenShift API', const=True, default=False)
    return parser

def login(user, password, url):
    if user == SYSTEM_ADMIN:
        subprocess.call(["oc", "login", "-u", user])
    else:
        subprocess.call(["oc", "login", url, "-u", user, "-p", password])

def get_all_routes():
    output = subprocess.check_output(
        "oc get routes -o jsonpath='{range .items[*]}[{.spec.host}, {.spec.tls.termination}]{end}' --all-namespaces",
        stderr=subprocess.STDOUT,
        shell=True).decode("utf-8")
    routes = {}
    if not output:
        return routes

    for item in output.split('['):
        if not item:
            continue
        route = item[0:-1].split(',') 
        if not route[1].strip():
            routes[route[0]] = { 
                'tls' : False,
                'protocol' : 'http',
                'url' : 'http://{}'.format(route[0])
            }
        else:
            routes[route[0]] = { 
                'tls' : True, 
                'protocol' : 'https',
                'url' : 'https://{}'.format(route[0])
            }

    return routes

def check_routes(routes, ignore_selfsign):
    for route in routes:
        print("{}[CHECKING] Route {}{}".format(bcolors.BOLD, route, bcolors.ENDC))
        try:
            r = requests.get(routes[route]["url"], verify=not ignore_selfsign)
        except requests.exceptions.RequestException as err:
            print("{}[ERROR] Impossible to get to route {}. Error: '{}'".format(bcolors.FAIL, route, err))
            if isinstance(err, requests.exceptions.SSLError):
                print("Is this cluster using self-signed certificate? Try running the script again with '-k' parameter.{}".format(bcolors.ENDC))
            continue

        routes[route]["status"] = r.status_code
        
        if r.status_code // httpCodes.SC_OK == 1:
            print("{}[OK] Route {} is ok. HTTP Status Code is {}. Time taken {}{}".format(bcolors.OKGREEN, route, r.status_code, r.elapsed, bcolors.ENDC))
        if r.status_code // httpCodes.SC_REDIRECTION == 1:
            print("{}[OK] Route {} returned a redirect code. HTTP Status Code is {}. Time taken {}{}".format(bcolors.OKGREEN, route, r.status_code, r.elapsed, bcolors.ENDC))
        if r.status_code // httpCodes.SC_CLIENT_ERR == 1:
            print("{}[WARN] Route {} returned a client error code. HTTP Status is {}. Time taken {}{}".format(bcolors.WARNING, route, r.status_code, r.elapsed, bcolors.ENDC))
        if r.status_code // httpCodes.SC_SERVER_ERR == 1:
            print("{}[ERROR] Route {} returned a server error code. HTTP Status is {}. Time taken {}{}".format(bcolors.FAIL, route, r.status_code, r.elapsed, bcolors.ENDC))
        
        # TODO: check certificates

parser = init_parser().parse_args()
if not parser.skip_login:
    login(parser.user, parser.password, parser.url)

check_routes(get_all_routes(), parser.ignore_selfsign)