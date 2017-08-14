log_file = 'engine.log'
_info = "INFO "
# _info = "\033[92mINFO \033[0m"
_warn = "\033[93mWARNI\033[0m"
_error = "\033[91mERROR\033[0m"
_debug = "\033[94mDEBUG\033[0m"

def log_info(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[{:}] - {:}\n".format(_info, message))

def log_warning(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[{:}] - {:}\n".format(_warn, message))

def log_error(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[{:}] - {:}\n".format(_error, message))

def log_debug(message=""):
    with open(log_file, 'a') as f:
        f.write("[{:}] - {:}\n".format(_debug, message))

def flush_log():
    print >> open(log_file, 'w'), ''
