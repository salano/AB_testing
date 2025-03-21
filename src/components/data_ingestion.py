import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
import io
from dataclasses import dataclass
from typing import Optional




@dataclass
class DataIngestionConfig:
    control_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','data.csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self, file_path: str, sheet: Optional[str] = None):
        logging.info('Entered data ingestion component/method')
        try:
            data = self.load(file_path, info = True, insheet = sheet)
            logging.info('Read dataset into dataframe')

            logging.info('ingestion of data completed')

            return data
        except Exception as e:
            raise CustomException(e, sys)
        
    def load(self, path: str, info: str = True, insheet: Optional[str] = None):
        try:
            if len(path.split(".csv")) > 1:
                read = pd.read_csv(path)
            elif len(path.split(".xlsx")) > 1:
                read = pd.read_excel(path, sheet_name= insheet)

            if info:
                if len(read) > 0:
                    print("# Data imported!")
                    print("# ------------------------------------", "\n")
                
                    print("# DIMENSIONS -------------------------")
                    print("Observation:", read.shape[0], "Column:", read.shape[1], "\n")
            
                    print("# DTYPES -----------------------------")
                    if len(read.select_dtypes("object").columns) > 0:
                        print("Object Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("object").columns), "\n", 
                            read.select_dtypes("object").columns.tolist(), "\n")
                    if len(read.select_dtypes("integer").columns) > 0:
                        print("Integer Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("integer").columns), "\n", 
                            read.select_dtypes("integer").columns.tolist(), "\n")
            
                    if len(read.select_dtypes("float").columns) > 0:
                        print("Float Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("float").columns), "\n", 
                            read.select_dtypes("float").columns.tolist(), "\n")
            
                    if len(read.select_dtypes("bool").columns) > 0:
                        print("Bool Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("bool").columns), "\n", 
                            read.select_dtypes("bool").columns.tolist(), "\n")
            
                    print("# MISSING VALUE ---------------------")
                    print("Are there any missing values? \n ", np.where(read.isnull().values.any() == False, 
                                                                    "No missing value!", "Data includes missing value!"), "\n")
                    buf = io.StringIO()
                    read.info(buf=buf)
                    info = buf.getvalue().split('\n')[-2].split(":")[1].strip()
                    print("# MEMORY USAGE ---------------------- \n", info)
                
                else:
                    print("# Data did not import!")
            
            return read
        except Exception as e:
            raise CustomException(e, sys)

    def describe_data(self, dataframe, info: str = True):
        try:
            read = dataframe

            if info:
                if len(read) > 0:
                    print("# Data imported!")
                    print("# ------------------------------------", "\n")
                
                    print("# DIMENSIONS -------------------------")
                    print("Observation:", read.shape[0], "Column:", read.shape[1], "\n")
            
                    print("# DTYPES -----------------------------")
                    if len(read.select_dtypes("object").columns) > 0:
                        print("Object Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("object").columns), "\n", 
                            read.select_dtypes("object").columns.tolist(), "\n")
                    if len(read.select_dtypes("integer").columns) > 0:
                        print("Integer Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("integer").columns), "\n", 
                            read.select_dtypes("integer").columns.tolist(), "\n")
            
                    if len(read.select_dtypes("float").columns) > 0:
                        print("Float Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("float").columns), "\n", 
                            read.select_dtypes("float").columns.tolist(), "\n")
            
                    if len(read.select_dtypes("bool").columns) > 0:
                        print("Bool Variables:", "\n", "# of Variables:", 
                            len(read.select_dtypes("bool").columns), "\n", 
                            read.select_dtypes("bool").columns.tolist(), "\n")
            
                    print("# MISSING VALUE ---------------------")
                    print("Are there any missing values? \n ", np.where(read.isnull().values.any() == False, 
                                                                    "No missing value!", "Data includes missing value!"), "\n")
                    buf = io.StringIO()
                    read.info(buf=buf)
                    info = buf.getvalue().split('\n')[-2].split(":")[1].strip()
                    print("# MEMORY USAGE ---------------------- \n", info)
                
                else:
                    print("# Data did not import!")
            
            return read
        except Exception as e:
            raise CustomException(e, sys)

        