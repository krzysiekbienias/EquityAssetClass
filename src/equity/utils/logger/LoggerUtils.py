import logging
import sys
import os


class LoggerBuilder:
    def __init__(self):
        pass

    def define_logger(self,logging_file):
        os.chdir('/Users/krzysiekbienias/Desktop/logger_files')
        logging.basicConfig(filename=logging_file+'.Log',
                            level=logging.INFO,
                            format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')
        logger=logging.getLogger()
        return logger

    def logging_conf(self):
        stdout_handler=logging.StreamHandler(sys.stdout)
        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s:',
                                    '%Y-%m-%d'+' '+ '%H:%M:%S')
        stdout_handler.setFormatter(formatter)
        logger=logging.getLogger()
        logger.addHandler(stdout_handler)
        logger.propagate=False


if __name__=='__main__':
    pass
