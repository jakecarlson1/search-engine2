log_file = 'engine.log'

def log_info(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[INFO ] - {:}\n".format(message))


def log_warning(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[WARNI] - {:}\n".format(message))

def log_error(message=""):
    message = message.replace('\n', '\t')
    with open(log_file, 'a') as f:
        f.write("[ERROR] - {:}\n".format(message))

def flush_log():
    print >> open(log_file, 'w'), ''
