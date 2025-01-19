import sys

def error_message_details(error , error_details:sys):
    _,_,exc_tb = error_details.exc_info()       #error details contains 3 items and we only need the 3rd one

    file_name  = exc_tb.tb_frame.f_code.co_filename
    error_message = "error occured python script name[{0}] line number[{1}] error message[{2}]".format(

        file_name,exc_tb.tb_lineno,str(error)
    )
    #this will give the error message
    return error_message


class customexception(Exception):
    def __init__(self,error_message , error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message , error_details = error_details)

    
    def __str__(self):
        return self.error_message
         
#this is a custom exception module we directly use this module from any other module , for exception handling