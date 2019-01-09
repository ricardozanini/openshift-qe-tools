# sysadmin default login
SYSTEM_ADMIN = "system:admin"

# colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# status codes. red.: https://httpstatuses.com/
class httpCodes:
    SC_OK = 200
    SC_REDIRECTION = 300
    SC_CLIENT_ERR = 400
    SC_SERVER_ERR = 500
