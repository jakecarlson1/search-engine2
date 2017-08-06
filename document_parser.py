import pykka
import xml.etree.ElementTree as ET

import logging_utils as log
import message_utils as msg

class DocumentParser(pykka.ThreadingActor):

    def __init__(self):
        super(DocumentParser, self).__init__()

    # def on_start(self):
    #     # load stop words

    def on_stop(self):
        log.log_info("DocumentParser.on_stop Stopping...")
        log.log_info("DocumentParser stopped")

    def on_receive(self, message):
        if message['method'] == 'load_file':
            data = message['data']
            if data['file']:
                self.load_file(data['file'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="DocumentParser.load_file no file provided")

    def load_file(self, _file):
        # with open(_file, 'r') as f:
        #     for line in f:
        #         log.log_info(line)
        try:
            log.log_info("DocumentParser.load_file parsing xml...")
            tree = ET.parse(_file)
            root = tree.getroot()
            for page in root.findall('page'):
                page_id = int(page.find('revision/id').text)
                log.log_info("Loading page: {:}".format(page_id))
        except:
            log.log_error("DocumentParser.load_file error parsing xml")
