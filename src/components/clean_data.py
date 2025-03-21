import os
import sys
from src.exception import CustomException
from src.logger import logging


class DataCleaning:
    def __init__(self):
        pass

    def initiate_data_deduplication(self, df, id: str = None):
        logging.info('Entered data Cleaning component')
        try:
            # Locate rows of duplicate data
            dups = df.duplicated()
            print(dups.any())

            # Number of Unique id/All users unique
            print("All users unique: ".format(df[id].nunique() == df.shape[0]))

            # Check duplicate unique identifier
            print(df[df[id].duplicated()])

            #drop duplicates from refined list
            df.drop_duplicates(subset=id, inplace=True) 

            logging.info('Cleaning of data completed')

            return df
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_mismatch_checker(self, df, group_name: str = None, group_value_1: str = None
                                ,group_value_2: str = None
                                ,exp_col: str = None, exp_value_1: str = None, exp_value_2: str = None
                                  ):
        logging.info('Entered data mismatch check component')
        try:
            # Check if there is mismatch between group and landing_page
            df_mismatch = df[(df[group_name]==group_value_2)&(df[exp_col]==exp_value_1)
                            |(df[group_name]==group_value_1)&(df[exp_col]==exp_value_2)]
            n_mismatch = df_mismatch.shape[0]
            print(f"The number of mismatched rows:{n_mismatch} rows" )
            print("Percent of mismatched rows:%.2f%%" % (n_mismatch/df.shape[0]*100))

            #clean data of duplicate users and group mismatched and create refined list
            df2 = df[(df[group_name]==group_value_2)&(df[exp_col]==exp_value_2)
                            |(df[group_name]==group_value_1)&(df[exp_col]==exp_value_2)]
            
            return df2

            logging.info('Cleaning of data completed')

            return df
        except Exception as e:
            raise CustomException(e, sys)