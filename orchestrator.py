import pykka

import logging_utils as log
import message_utils as msg

from document_parser import DocumentParser

class Orchestrator(pykka.ThreadingActor):

    def __init__(self):
        super(Orchestrator, self).__init__()

        self.document_parser = None

    def on_start(self):
        try:
            log.log_info("Starting DocumentParser...")
            self.document_parser = DocumentParser.start()
            log.log_info("DocumentParser started")
        except:
            log.log_error("Could not start DocumentParser")

    def on_stop(self):
        log.log_info("Orchestrator.on_stop Stopping...")
        self.document_parser.stop()
        log.log_info("Orchestrator stopped")

    def on_receive(self, message):
        if message['method'] == 'load_file':
            if message['data']['file']:
                response = self.document_parser.ask(message)
                if response['status'] == 0:
                    return msg.build_response(status=0)
                else:
                    return msg.build_response(status=-2, error_msg="Orchestrator.load_file failed: {:}".format(response['error_msg']))
            else:
                return msg.build_response(status=-1, error_msg="No file provided to Orchestrator.load_file")
