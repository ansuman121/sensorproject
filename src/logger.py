import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%y_%H_%M_%s')}.log" #name of the logfile in and it will be written in present time as name

log_path =os.path.join(os.getcwd(),"Logs",LOG_FILE) #the path that will be created for log file

os.makedirs(log_path,exist_ok=True)#path created

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
)