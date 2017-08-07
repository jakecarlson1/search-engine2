import traceback
import pykka

import logging_utils as log
import message_utils as msg

class IndexHandler(pykka.ThreadingActor):

    def __init__(self):
        super(IndexHandler, self).__init__()

    def on_stop(self):
        log.log_info("Stopping IndexHandler...")
        log.log_info("IndexHandler stopped")
