import traceback
import pykka

import logging_utils as log
import message_utils as msg

class QueryProcessor(pykka.ThreadingActor):

    def __init__(self, _document_parser, _index_handler):
        super(QueryProcessor, self).__init__()
        self.document_parser = _document_parser
        self.index_handler = _index_handler

    def on_stop(self):
        log.log_info("Stopping QueryProcessor...")
        log.log_info("QueryProcessor stopped")

    def on_receive(self, message):
        log.log_info("QueryProcessor received message: {:}".format(message))
        if message['method'] == 'query':
            data = message['data']
            if data['query']:
                return self.process_query(message['data']['query'])
            else:
                return msg.build_response(status=-1, error_msg="QueryProcessor.query no query provided")

        return msg.build_response(status=-13, error_msg="No method to process message: {:}".format(message))

    def process_query(self, query):
        # assume single word query
        stem_word = self.stem_word(query)
        if stem_word != "":
            response = self.index_handler.ask(msg.build_request(method='search', data={'word': stem_word}))
            if response['status'] == 0:
                # TODO(JC): Add document retrival
                return msg.build_response(status=0, data=response['data'])
            else:
                return msg.build_response(status=-3, error_msg="QueryProcessor.process_query failed: {:}".format(response['error_msg']))
        else:
            return msg.build_response(status=-2, error_msg="Stemmed word is empty string")

    def stem_word(self, word):
        response = self.document_parser.ask(msg.build_request(method='stem_word', data={'word': word}))
        if response['status'] == 0:
            return response['data']['stem']
        else:
            log.log_error("Orchestrator could not stem word: {:}".format(response['error_msg']))
            return ""
