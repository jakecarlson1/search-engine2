from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import traceback
import pickle
import pykka
import re
import xml.etree.ElementTree as ET

import logging_utils as log
import message_utils as msg

class DocumentParser(pykka.ThreadingActor):

    def __init__(self, _index_handler):
        super(DocumentParser, self).__init__()
        self.ps = PorterStemmer()
        self.index_handler = _index_handler
        self.stop_words = []
        self.word_re = re.compile('[\w]+')
        self.unwanted_chars = ['[', ']', '{', '}', '(', ')', '|', '\\', '/', '#', ',', '.', '?', '=', '+', '-', '_', '<', '>', ':']

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
        log.log_info("DocumentParser received message: {:}".format(message))
        if message['method'] == 'load_file':
            data = message['data']
            if data['file']:
                self.load_file(data['file'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="DocumentParser.load_file no file provided")
        if message['method'] == 'stem_word':
            data = message['data']
            if data['word']:
                stem = self.stem_word(data['word'])
                return msg.build_response(status=0, data={'stem': stem})
            else:
                return msg.build_response(status=-1, error_msg="DocumentParser.stem_word no word provided")

        return msg.build_response(status=-13, error_msg="No method to process message: {:}".format(message))

    def load_file(self, _file):
        try:
            log.log_info("DocumentParser.load_file parsing xml...")
            tree = ET.parse(_file)
            root = tree.getroot()
            log.log_info("Loading pages...")
            for page in root.findall('page'):
                page_id = int(page.find('id').text)
                log.log_info("Loading page: {:}".format(page_id))
                page_data = self.parse_xml_page(page)
                self.index_handler.ask(msg.build_request(method='store_page', data={'page': page_data}))
            log.log_info("Done loading pages")
        except:
            log.log_error("DocumentParser.load_file error parsing xml")
            log.log_debug(traceback.format_exc())

    def parse_xml_page(self, page):
        result = {}
        page_id = int(page.find('id').text)
        page_text = page.find('revision/text').text
        for c in page_text:
            if c in self.unwanted_chars:
                page_text = page_text.replace(c, ' ')
        for word in page_text.split():
            try:
                # log.log_info("Processing word: {:}".format(word))
                word = word.strip().lower()
                if word != "" and self.word_re.match(word) and word not in self.stop_words:
                    word = self.stem_word(word)
                    if word not in result.keys():
                        result[word] = {}
                    if page_id in result[word].keys():
                        result[word][page_id] += 1
                    else:
                        result[word][page_id] = 1
            except (UnicodeEncodeError) as e:
                log.log_warning("Tried processing non-ascii character")
                # log.log_debug(traceback.format_exc())
        return result

    def stem_word(self, word):
        return self.ps.stem(str(word).lower())
