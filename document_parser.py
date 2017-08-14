import traceback
import pickle
import pykka
import xml.etree.ElementTree as ET

import logging_utils as log
import message_utils as msg

class DocumentParser(pykka.ThreadingActor):

    def __init__(self):
        super(DocumentParser, self).__init__()
        self.stop_words = []

    def on_start(self):
        # load stop words
        log.log_info("DocumentParser.on_start loading stop words")
        try:
            log.log_info("Reading from persistance file")
            with open("stop-words.p", "r") as f:
                self.stop_words = pickle.load(f)
        except:
            log.log_info("Could not read from persistance, rebuilding")
            with open("stop-words.txt", 'r') as f:
                for line in f:
                    line = line.strip()
                    self.stop_words.append(line)

        log.log_info("Stop words loaded")

    def on_stop(self):
        log.log_info("Stopping DocumentParser...")

        log.log_info("Writing stop words to persistance file")
        with open("stop-words.p", "w") as f:
            pickle.dump(self.stop_words, f)
        log.log_info("Stop words saved")

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
        try:
            log.log_info("DocumentParser.load_file parsing xml...")
            tree = ET.parse(_file)
            root = tree.getroot()
            log.log_info("Loading pages...")
            for page in root.findall('page'):
                page_id = int(page.find('id').text)
                log.log_info("Loading page: {:}".format(page_id))

            log.log_info("Done loading pages")
        except:
            log.log_error("DocumentParser.load_file error parsing xml")
            log.log_debug(traceback.format_exc())
