import sys
from src.logger import logger

def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = (
        f"Error in script [{file_name}] line [{exc_tb.tb_lineno}] message [{error}]"
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

        # log automatique (optionnel mais utile)
        logger.exception(self.error_message)

    def __str__(self):
        return self.error_message