r"""torecsys.utils.tqdm is a sub module of utils for logging during training"""

import logging
from tqdm.autonotebook import tqdm

class TqdmHandler(logging.StreamHandler):
    r"""logging.StreamHandler for logging with tqdm progress bar"""
    def __init__(self):
        """initialize TqdmHandler"""
        logging.StreamHandler.__init__(self)
    
    def emit(self, record : str):
        r"""Format and write message
        
        Args:
            record (str): message to be written during progress 
        """
        msg = self.format(record)
        tqdm.write(msg)
