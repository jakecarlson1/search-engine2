import traceback
import pykka
import re

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
                return self._process_query(message['data']['query'])
            else:
                return msg.build_response(status=-1, error_msg="QueryProcessor.query no query provided")

        return msg.build_response(status=-13, error_msg="No method to process message: {:}".format(message))

    def _process_query(self, query):
        # assume single word query
        query = str(query).lower()
        stem_word = self._stem_word(query)
        if stem_word != "":
            response = self.index_handler.ask(msg.build_request(method='search', data={'word': stem_word}))
            if response['status'] == 0:
                # TODO(JC): Add document retrival
                result = self._beautify_result(response['data'], query)
                return msg.build_response(status=0, data=result)
            else:
                return msg.build_response(status=-3, error_msg="QueryProcessor.process_query failed: {:}".format(response['error_msg']))
        else:
            return msg.build_response(status=-2, error_msg="Stemmed word is empty string")

    def _stem_word(self, word):
        response = self.document_parser.ask(msg.build_request(method='stem_word', data={'word': word}))
        if response['status'] == 0:
            return response['data']['stem']
        else:
            log.log_error("Orchestrator could not stem word: {:}".format(response['error_msg']))
            return ""

    def _beautify_result(self, data, word):
        # sort by term frequency
        # docs = data.keys()
        docs = sorted(data.items(), key=lambda x: x[1], reverse=True)
        log.log_info("Docs for query: {:}".format(docs))

        # build string result
        result = ""
        count = 1
        for d in docs:
            # get text, title, author, date for doc
            title, text, author, date = self._get_doc_info(d[0])
            text = self._beautify_text(text, word)

            # format entry
            result += "[{:}]\t\033[94m{:}\033[0m - Doc: {:}\n\t{:} - {:}\n\t{:}\n".format(count, title, d[0], author, date, text)
            count += 1

        return result

    def _get_doc_info(self, doc_id):
        response = self.document_parser.ask(msg.build_request(method='get_doc', data={'doc_id': doc_id}))
        if response['status'] == 0:
            data = response['data']
            return data['title'], data['text'], data['author'], data['date']
        else:
            log.log_error("Could not get info for doc: {:}".format(response['error_msg']))

    def _beautify_text(self, text, word):
        match = re.search('(?:\w+\W+){,10}' + word + '(?:\W+\w+){,10}', str(text).lower())
        result = text[match.start():match.end()].replace('\n', '')
        return result
