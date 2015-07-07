#!/usr/local/bin/python

import sys
from gm_common import *

if __name__ == "__main__" :
    script_code=sys.argv[1]    
    script_log_file=sys.argv[2]
    send_mail(script_code,script_log_file)
