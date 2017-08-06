import pykka

import logging_utils as log
import message_utils as msg

class Logger(pykka.ThreadingActor):

    def __init__(self):
        super(DocumentParser, self).__init__()

        # self.write_len = 2048
        self.write_string = ""
        self.log_file = "engine.log"

    def on_start(self):
        try:
            self._log_info("Logger.on_start")
        except:
            self._log_error("Logger.on_start failed")

    def on_receive(self, message):
        if message['method'] == 'log_info':
            data = message['msg']
            if data['msg']:
                self._log_info(data['msg'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="Logger.log_info no message provided")

        elif message['method'] == 'log_warning':
            data = message['msg']
            if data['msg']:
                self._log_warning(data['msg'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="Logger.log_warning no message provided")

        elif message['method'] == 'log_error':
            data = message['msg']
            if data['msg']:
                self._log_error(data['msg'])
                return msg.build_response(status=0)
            else:
                return msg.build_response(status=-1, error_msg="Logger.log_error no message provided")

    def _log_info(self, _msg):
        try:
            # log.log_info("Logger._log_info write")
            self.write_string = self.write_string + "[INFO ] - {:} - \n".format(_msg)
            # if len(self.write_string) >= self.write_len:
            self.write_to_log()
        except:
            # log.log_error("Logger._log_info could not write to log")
            self._log_error("Logger failed to log info")


    def _log_warning(self, _msg):
        try:
            self.write_string = self.write_string + "[WARNI] - {:} - \n".format(_msg)
            # if len(self.write_string) >= self.write_len:
            self.write_to_log()
        except:
            # log.log_error("Logger._log_warning could not write to log")
            self._log_error("Logger failed to log warnings")

    def _log_error(self, _msg):
        try:
            self.write_string = self.write_string + "[ERROR] - {:} - \n".format(_msg)
            # if len(self.write_string) >= self.write_len:
            self.write_to_log()
        except:
            # log.log_error("Logger._log_error could not write to log")
            return

    def _write_to_log(self):
        with open(self.log_file, 'a') as f:
            f.write(self.write_string)
            f.close()
            self.write_string = ""
