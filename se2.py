import sys
import time

import logging_utils as log
import message_utils as msg

from orchestrator import Orchestrator

orchestrator = None

def main(argv):
    log.flush_log()
    log.log_info("Hello")

    # process arguments
    document = None
    if '-d' in argv:
        document = argv[argv.index('-d') + 1]

    # launch orchestrator
    orchestrator = Orchestrator.start()
    if document:
        response = orchestrator.ask(msg.build_request(method='load_file', data={'file': document}))
        if response['status'] != 0:
            log.log_error(response['error_msg'])
        else:
            log.log_info("Loaded file")

    is_running = True
    while is_running:
        query = raw_input("Search: ")
        log.log_info("Query: {:}".format(query))
        if query == "q" or query == "quit":
            is_running = False
        else:
            response = orchestrator.ask(msg.build_request(method='search', data={'query': query}))
            if response['status'] == 0:
                log.log_info("Found word: {:}".format(response['data']))
                print "Found word: {:}".format(response['data'])
            else:
                log.log_error(response['error_msg'])

    orchestrator.stop()
    log.log_info("Goodbye")

if __name__ == '__main__':
    try:
        main(sys.argv)
    except (KeyboardInterrupt):
        if orchestrator:
            orchestrator.stop()
            if response['status'] == 0:
                log.log_info("Cleanup successful")
        log.log_info("Goodbye")
