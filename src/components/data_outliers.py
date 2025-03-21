import os
import sys
from src.exception import CustomException
from src.logger import logging
from numpy import percentile


class DataOutlier:
    def __init__(self):
        pass

    def initiate_data_outlier(self, df, value_name: str = None, cutoff_value: float = 1.5):
        logging.info('Entered data Outlier component')
        try:
            q25, q75 = percentile(df[value_name], 25), percentile(df[value_name], 75)
            iqr = q75 - q25
            # calculate the outlier cutoff
            cut_off = iqr * cutoff_value
            lower, upper = q25 - cut_off, q75 + cut_off
            print( "25th=%d, 75th=%d, IQR=%d, Lower=%d, Upper=%d" % (q25, q75, iqr, lower, upper))
            # identify outliers
            outliers = df[(df[value_name] <lower)|(df[value_name] >upper)]
            print("Outliers identified")
            print(f"Nymber of outliers: {outliers}\n")
            print( "The number of Identified outliers: %d" % len(outliers))
            outliers_removed = df[(df[value_name] >=lower) & (df[value_name] <=upper)]
            print("Percent of outliers: %.2f%%" % (100*(1-len(outliers_removed)/len(df))))
            return outliers_removed
        except Exception as e:
            raise CustomException(e, sys)