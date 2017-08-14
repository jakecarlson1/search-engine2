import traceback
import pykka

import logging_utils as log
import message_utils as msg

class IndexHandler(pykka.ThreadingActor):

    def __init__(self):
        super(IndexHandler, self).__init__()
        self.index = {}

    def on_stop(self):
        log.log_info("Stopping IndexHandler...")
        log.log_info("IndexHandler stopped")

    def on_receive(self, message):
        if message['method'] == 'store_page':
            data = message['data']
            if data['page']:
                self.load_by_page(data['page'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="IndexHandler.store_page no page provided")
        if message['method'] == 'search':
            data = message['data']
            if data['word']:
                result = self.search(data['word'])
                return msg.build_response(status=0, data=result)
            else:
                return msg.build_response(status=-1, error_msg="IndexHandler.search no word provided")

    def load_by_page(self, page):
        log.log_info("IndexHandler is adding a page...")
        for w in page.keys():
            if w not in self.index.keys():
                self.index[w] = {}
            for i in page[w].keys():
                self.index[w][i] = page[w][i]
                # log.log_info("Added word: {:} document: {:} count: {:}".format(w, i, self.index[w][i]))
        log.log_info("Done adding page")

    def search(self, word):
        result = {}
        if word in self.index.keys():
            result = self.index[word]
        return result
