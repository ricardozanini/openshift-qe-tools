# OpenShift QE Tools

_(Working in Progress) - use at your own discretion_

A bunch of scripts and tools to ease monitoring, testing and health checking OpenShift 3.x clusters.

## 0. Install Python3 and the required packages

If using RHEL, [follow this guide](https://developers.redhat.com/blog/2018/08/13/install-python3-rhel/) to install `python3`.

Having installed `python3`, install the required modules to run the scripts:

```console
cd openshift-qe-tools
python3 -m pip install -r requirements.txt
```

## 1. Router

Inside the `router` path we have scripts to check the health of OpenShift routes.

### test-routes.py

Simple script to check if all your routes are ok. It basically queries the `router` API and pings every route to check its returned HTTP status code. If something isn't right you'll see colorful `WARN` and `ERROR` messages in your console.

#### How to use

Simply call `python3 test-routes.py`. The script will use the default `system:admin` user and will login at your local cluster. For more details about usage use:

```console
$ python3 test-routes.py -h

usage: test-routes.py [-h] [-u USER] [-p PASSWORD] [--url URL]
                      [--skip-login [SKIP_LOGIN]] [-k [IGNORE_SELFSIGN]]

check every route within an OpenShift cluster

optional arguments:
  -h, --help            show this help message and exit
  -u USER               the cluster user admin to login
  -p PASSWORD           the cluster admin password
  --url URL             the cluster URL
  --skip-login [SKIP_LOGIN]
                        completely skip oc login (you must be logged in)
  -k [IGNORE_SELFSIGN]  ignores self-signed certificates when connecting to
                        routes and OpenShift API
```