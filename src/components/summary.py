import os
import sys
from src.exception import CustomException
from src.logger import logging


class DataSummary:
    def __init__(self):
        pass

    def initiate_data_summary(self, df, id: str = None, group: str = None, value_name: str = None):
        logging.info('Entered data Summary component')
        try:
            print('SUMMARY STATS\n')

            # Number of Unique accounts/All records unique
            print("All records unique: {} ".format(df[id].nunique() == df.shape[0]))
            # Summary Stats:
            print(df.describe([0.01, 0.05, 0.10, 0.20, 0.80, 0.90, 0.95, 0.99])[[value_name]].T)

            df_25 = df[df[value_name] <=df[value_name].quantile(0.25)]
            df_50 = df[df[value_name] <=df[value_name].quantile(0.50)]
            df_75 = df[df[value_name] <=df[value_name].quantile(0.75)]
            df_99 = df[df[value_name] <=df[value_name].quantile(0.99)]


            print("\nThe number of rows/units below {:.1%} is {} with a value of {} or {:.1%} of total.\n "
                  .format(0.25, len(df_25), df_25[value_name].sum(),
                           (df_25[value_name].sum()/df[value_name].sum())  ))
            print("\nThe number of rows/units below {:.1%} is {} with a value of {} or {:.1%} of total.\n "
                  .format(0.50, len(df_50), df_50[value_name].sum(),
                           (df_50[value_name].sum()/df[value_name].sum())  ))
            print("\nThe number of rows/units below {:.1%} is {} with a value of {} or {:.1%} of total.\n "
                  .format(0.75, len(df_75), df_75[value_name].sum(),
                           (df_75[value_name].sum()/df[value_name].sum())  ))
            print("\nThe number of rows/units below {:.1%} is {} with a value of {} or {:.1%} of total.\n "
                  .format(0.99, len(df_99), df_99[value_name].sum(),
                           (df_99[value_name].sum()/df[value_name].sum())  ))
            
            std = df[value_name].std()

            two_std = df[(df[value_name] >=std - 2) | (df[value_name] <=std + 2)]
            print("\n {} of rows/units lies within 2 STD of the mean value from a total {} population\n"
                  .format(len(two_std), len(df)))

            # A/B Groups & Target Summary Stats
            print(df.groupby(group)[value_name].agg(["count", "median", "mean", "std", "max"])) 

            logging.info('Summary of data completed')

            return df
        except Exception as e:
            raise CustomException(e, sys)