import os
import sys
from src.exception import CustomException
from src.logger import logging

import matplotlib.pyplot as plt
import statsmodels.api as sm
from pylab import rcParams
rcParams['figure.figsize'] = 15, 5
import seaborn as sns
sns.set_style("whitegrid")


class DataVizualization:
    def __init__(self):
        pass

    def initiate_discrete_data_vizualization(self, df, value_name: str = None, group: str = None):
        logging.info('Entered data vizualization component')
        try:
            
            fig, axes = plt.subplots(1,3)

            sns.histplot(x=group, y=value_name, data=df, ax=axes[0])
            axes[0].set_title("Distribution of total data")

            sns.countplot(x=value_name, data=df, hue=group, ax=axes[1])
            axes[1].set(title="# value for Each group", ylabel="Count/value")

            sns.pointplot(x=group, y=value_name, data=df, ax=axes[2])
            # axes[2].set_ylim([0.115, 0.125])
            axes[2].set(title="Rate for Each Group",ylabel="Rate")

            plt.show()
            
            return None
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_continuous_data_vizualization(self,
                                    df, value_name: str = None,
                                    group_name: str = None,
                                    group_1: str = None, group_2: str = None
                                    ,subline: str = None):
        logging.info('Entered data vizualization component')
        try:
            
            fig, axes = plt.subplots(1, 3, figsize = (12,5))
            df[(df[group_name] == group_1)].hist(value_name, ax = axes[0], color = "steelblue")
            df[(df[group_name] == group_2)].hist(value_name, ax = axes[1], color = "steelblue")
            sns.boxplot(x = df[group_name], y = df[value_name], ax = axes[2])

            plt.suptitle(subline, fontsize = 20)
            axes[0].set_title("Distribution of {} (A)".format(group_1), fontsize = 15)
            axes[1].set_title("Distribution of {} (B)".format(group_2), fontsize = 15)
            axes[2].set_title("Distribution of Two Groups", fontsize = 15)

            plt.tight_layout(pad = 4);
            plt.show()

            df[df[group_name] == group_1].reset_index().set_index("index")[value_name].plot(legend = True, label = group_1, figsize = (16,5))
            df[df[group_name] == group_2].reset_index().set_index("index")[value_name].plot(legend = True, label = group_2)
            plt.suptitle(subline, fontsize = 20);
            plt.show()
            
            return None
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_total_vs_num_vizualization(self, df, value_name: str = None, num: int = 50):
        logging.info('Entered data vizualization component')
        try:
            
            fig, axes = plt.subplots(2, 1, figsize = (25,10))
            df.groupby(value_name)[id].count().plot(ax = axes[0])
            df.groupby(value_name)[id].count()[:num].plot(ax = axes[1])
            plt.suptitle("The number of accounts in the game rounds played", fontsize = 25)
            axes[0].set_title("How many accounts are there all game rounds?", fontsize = 15)
            axes[1].set_title(f"How many accounts are there first {num} game rounds?", fontsize = 15)
            plt.tight_layout(pad=5);

            plt.show()
            
            return None
        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_qq_vizualization(self, df, value_name: str = None):
        logging.info('Entered data vizualization component')
        try:
            
            sm.qqplot(df[value_name])
            plt.tight_layout(pad=5);
            plt.suptitle(f"Checking {value_name} against a normal distribution", fontsize = 20);
            plt.show()
            
            return None
        except Exception as e:
            raise CustomException(e, sys)
        
    