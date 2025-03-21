from src.components.data_ingestion import DataIngestion
from src.components.clean_data import DataCleaning
from src.components.vizualization import DataVizualization
from src.components.summary import DataSummary
from src.components.data_outliers import DataOutlier
from src.utils import AB_Test_continuous, AB_testing_prop1, AB_testing_prop2,AB_test_discrete
import pandas as pd
import numpy as np



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


if __name__ == "__main__":
    '''
    #data ingestion   
    data_file_path = r"data\cookie_cats.csv"
    ing_obj = DataIngestion()
    data_1 = ing_obj.initiate_data_ingestion(data_file_path)
    print(data_1.head())

    #data cleaning
    clean_obj = DataCleaning()
    data_2 = clean_obj.initiate_data_deduplication(data_1,'userid')
    print(data_2.head())
    #data_2 = obj.initiate_mismatch_checker(data_2,"group","control","treatment",
    #                                       "landing_page","old_page","new_page")

    #Initial data vizualization
    viz_obj = DataVizualization()
    viz_obj.initiate_continuous_data_vizualization(data_2, "sum_gamerounds", "version","gate_30","gate_40","Before Removing The Extreme Value")

   
    #run summary
    sum_obj = DataSummary()
    sum_obj.initiate_data_summary(data_2, "userid", "version", "sum_gamerounds")

    print("OUTLIERS\n")
    #print("Remove max value")
    #data_3 = data_2[data_2['sum_gamerounds'] < data_2['sum_gamerounds'].max()]
    out_obj = DataOutlier()
    #outlier cutoff 6 times IQR
    data_3 = out_obj.initiate_data_outlier(data_2, "sum_gamerounds", 1.5)

    #Vizualization after outlier removal
    viz_obj.initiate_continuous_data_vizualization(data_3, "sum_gamerounds", "version","gate_30","gate_40","After Removing The Extreme Value")
    viz_obj.initiate_qq_vizualization(data_3, "sum_gamerounds")



    #run summary
    sum_obj.initiate_data_summary(data_3, "userid", "version", "sum_gamerounds")

    #first 20 users
    print(data_3.groupby("sum_gamerounds").userid.count().reset_index().head(20))

    # How many users reached gate 30 & gate 40 levels?
    print(data_3.groupby("sum_gamerounds").userid.count().loc[[30,40]])

    # Retention Problem
    r_df = pd.DataFrame({"RET1_COUNT": data_3["retention_1"].value_counts(),
                "RET7_COUNT": data_3["retention_7"].value_counts(),
                "RET1_RATIO": data_3["retention_1"].value_counts() / len(data_3),
                "RET7_RATIO": data_3["retention_7"].value_counts() / len(data_3)})
    print(r_df)

    '''
    #55 percent of the players didn't play the game 1 day after insalling
    #81 percent of the players didn't play the game 7 day after insalling

    '''

    print(data_3.groupby(["version", "retention_1"]).sum_gamerounds.agg(["count", "median", "mean", "std", "max"]))

    print(data_3.groupby(["version", "retention_7"]).sum_gamerounds.agg(["count", "median", "mean", "std", "max"]))

    '''
    #Looking at the summary statistics of retention variables by version and comparing with sum_gamerounds, there are similarities between groups. However, it will be more helpful to see if there is a statistically significant difference.
    '''

    data_3["Retention"] = np.where((data_3.retention_1 == True) & (data_3.retention_7 == True), 1,0)
    print(data_3.groupby(["version", "Retention"])["sum_gamerounds"].agg(["count", "median", "mean", "std", "max"]))

    '''
    #Similar results are seen when the number of users who came and did not come 1 day and 7 days after the game was installing. Approximately 12.000 users among the total users played the game both 1 day and 7 days after installing the game. 14% of the total users include people who will continue the game in the future.

    '''

    '''
    #When the retention variables are combined and the two groups are compared, the summary statistics are similar here as well.
    '''

    data_3["NewRetention"] = list(map(lambda x,y: str(x)+"-"+str(y), data_3.retention_1, data_3.retention_7))
    print(data_3.groupby(["version", "NewRetention"]).sum_gamerounds.agg(["count", "median", "mean", "std", "max"]).reset_index())

    #A/B testing
    print("{} is control group (A) and {} is treatment group (B)\n".format("gate_30", "gate_40"))
    AB_results = AB_Test_continuous(data_3,"version", "sum_gamerounds", "gate_30", "Average game rounds")
    print(AB_results)

    print("Which level has more advantages in terms of player retention?")
    print("1-day and 7-day average retention are higher when the gate is at level 30 than when it is at level 40.")

    print(data_3.groupby("version").retention_1.mean(), data_3.groupby("version").retention_7.mean())

    print("The gate should be at level 30 but average retentions look like similar. We need more data for similarity.")
    '''
    

    '''
    #Testing area
    #test1
   #data ingestion   
    data1_file_path = r"data\ab_testing.xlsx"
    ing_obj = DataIngestion()
    df_control = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Control Group")
    df_control['Group'] = "Control Group"
    df_test = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Test Group")
    df_test['Group'] = "Test Group"

    #union datasets
    data = pd.concat([df_control, df_test], axis=0).reset_index()
    print(data.head())

    #Initial data vizualization
    viz_obj = DataVizualization()
    #print(data.index.is_unique)
    #data.drop('index', axis=1, inplace=True)
    data['id'] = data.index
    viz_obj.initiate_continuous_data_vizualization(data, "Purchase", "Group","Control Group","Test Group","Before Removing The Extreme Value")
    #plot to check if distribution is normal
    viz_obj.initiate_qq_vizualization(data, "Purchase")

     #run summary
    sum_obj = DataSummary()
    sum_obj.initiate_data_summary(data, "id", "Group", "Purchase")

    print("OUTLIERS\n")
    out_obj = DataOutlier()
    #outlier cutoff x times IQR
    data_outl = out_obj.initiate_data_outlier(data, "Purchase", 1.5)

    #A/B testing
    AB_results = AB_Test_continuous(data, "Group", "Purchase", "Control Group", "Average purchases")
    print(AB_results)
    '''
    '''
    #test2
    #data ingestion   
    data1_file_path = r"data\ab_testing.xlsx"
    ing_obj = DataIngestion()
    df_control = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Control Group")
    df_control['Group'] = "Control Group"
    df_test = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Test Group")
    df_test['Group'] = "Test Group"

    #union datasets
    data = pd.concat([df_control, df_test], axis=0).reset_index()
    print(data.head())

    #Initial data vizualization
    viz_obj = DataVizualization()
    #print(data.index.is_unique)
    #data.drop('index', axis=1, inplace=True)
    data['id'] = data.index
    viz_obj.initiate_continuous_data_vizualization(data, "Earning", "Group","Control Group","Test Group","Before Removing The Extreme Value")
    #plot to check if distribution is normal
    viz_obj.initiate_qq_vizualization(data, "Earning")

     #run summary
    sum_obj = DataSummary()
    sum_obj.initiate_data_summary(data, "id", "Group", "Earning")

    print("OUTLIERS\n")
    out_obj = DataOutlier()
    #outlier cutoff x times IQR
    data_outl = out_obj.initiate_data_outlier(data, "Earning", 1.5)

    #A/B testing
    AB_results = AB_Test_continuous(data, "Group", "Earning", "Control Group", "Average Earning")
    print(AB_results)
    '''

    '''
    As a result of Independent Samples T Test, there is a statistically significant difference between them because p-value = 0.0000 < 0.05 so H0 is rejected. Considering the gain in the test group, the test group earns more. That's why we should choose average bidding.
    '''

    '''
    #test3 proportions

    #data ingestion   
    data1_file_path = r"data\ab_testing.xlsx"
    ing_obj = DataIngestion()
    df_control = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Control Group")
    df_control['Group'] = "Control Group"
    df_test = ing_obj.initiate_data_ingestion(data1_file_path, sheet="Test Group")
    df_test['Group'] = "Test Group"

    #union datasets
    data = pd.concat([df_control, df_test], axis=0).reset_index()
    print(data.head())

    AB_testing_prop1(df_control, df_test,"Impression", "Click","Click Through Rate ")
    AB_testing_prop2(data, "Group", "Control Group", "Impression", "Click", "Click Through Rate")


    print("Based on the current average click-through rates,\n")
    print("    the Control click through rate: 5 out of 100 people click on the ad, while\n")
    print("    Treatment group average click through rate 3 out of 100.\n")

    print("So, if the company wants to increase the click-through rate, it may prefer the control group.")'
    '''

    '''
    #Test 3
    #data ingestion   
    data_file_path = r"data\ab_data.csv"
    ing_obj = DataIngestion()
    data_1 = ing_obj.initiate_data_ingestion(data_file_path)
    print(data_1.head())

    #data cleaning
    clean_obj = DataCleaning()
    data_2 = clean_obj.initiate_data_deduplication(data_1,'user_id')
    print(data_2.head())
    # Check if there is mismatch between group and landing_page
    df_mismatch = data_2[(data_2["group"]=="treatment")&(data_2["landing_page"]=="old_page")
                    |(data_2["group"]=="control")&(data_2["landing_page"]=="new_page")]
    n_mismatch = df_mismatch.shape[0]
    print(f"The number of mismatched rows:{n_mismatch} rows" )
    print("Percent of mismatched rows:%.2f%%" % (n_mismatch/data_2.shape[0]*100))

    #clean data of duplicate users and group mismatched and create refined list
    data_3 = data_2[(data_2["group"]=="treatment")&(data_2["landing_page"]=="new_page")
                    |(data_2["group"]=="control")&(data_2["landing_page"]=="old_page")]
    
    data_4 = clean_obj.initiate_data_deduplication(data_3,'user_id')
    print(data_4.head())

    # Conversion Rate
    df_counts = pd.DataFrame({"Control_COUNT": data_4[data_4.group=="control"].converted.value_counts(),
                "Treatment_COUNT": data_4[data_4.group=="treatment"].converted.value_counts(),
                "Control_RATIO": data_4[data_4.group=="control"].converted.value_counts()/ len(data_4[data_4.group=="control"]),
                "Trement_RATIO": data_4[data_4.group=="treatment"].converted.value_counts() / len(data_4[data_4.group=="treatment"])})
    print(df_counts)

    #Initial data vizualization
    viz_obj = DataVizualization()
    viz_obj.initiate_discrete_data_vizualization(data_4, "converted","group")

    #A/B testing
    AB_results = AB_test_discrete(data_4, "group", "converted", "conversion rate")
    print(AB_results) '
    '''

    #data ingestion   
    data_file_path = r"data\Marketing campaign dataset.csv"
    ing_obj = DataIngestion()
    data = ing_obj.initiate_data_ingestion(data_file_path)
    #Limit tag two search tags: #The Power of X (A) and #Be Bold. Be X (B)
    data_1 = data[(data.search_tags == "#The Power of X") | (data.search_tags == "#Be Bold. Be X") ]
    print("# of rows in tag A: {}".format(len(data[(data.search_tags == "#The Power of X")])))
    print("# of rows in tag B: {}".format(len(data[(data.search_tags == "#Be Bold. Be X")])))
    print(data_1.head())
    
    #Create Dataframe of 12000 rows for each tag for testing
    df1 = data[data.search_tags == "#The Power of X"][:12000]
    df2 = data[data.search_tags == "#Be Bold. Be X"][:12000]
    w_data = pd.concat([df1, df2], axis=0)

    #Add A random normal revenue columns using mean:93273 and standard dev: 1444
    w_data["revenue"] = list(np.random.normal(loc=93273.4375, scale=1444.81674239821, size=24000))
    print(w_data.head())


    #Initial data vizualization
    viz_obj = DataVizualization()
    #print(data.index.is_unique)
    #data.drop('index', axis=1, inplace=True)
    w_data['id'] = w_data.index
    viz_obj.initiate_continuous_data_vizualization(w_data, "revenue", "search_tags","#The Power of X","#Be Bold. Be X","Before Removing The Extreme Value")
    #plot to check if distribution is normal
    viz_obj.initiate_qq_vizualization(w_data, "revenue")

    
     #run summary
    sum_obj = DataSummary()
    sum_obj.initiate_data_summary(w_data, "id", "search_tags", "revenue")
   

    print("OUTLIERS\n")
    out_obj = DataOutlier()
    #outlier cutoff x times IQR
    data_outl = out_obj.initiate_data_outlier(w_data, "revenue", 1.5)
  
    #A/B testing
    AB_results = AB_Test_continuous(w_data, "search_tags", "revenue", "#The Power of X", "Average Revenue")
    print(AB_results)

    #Proportion A/B testing


    AB_results = AB_testing_prop2(w_data, "search_tags", "A", "impressions", "clicks", "Click Through Rate")
    print(AB_results)
    exit()

    print("Based on the current average click-through rates,\n")
    print("    the Control click through rate: 5 out of 100 people click on the ad, while\n")
    print("    Treatment group average click through rate 3 out of 100.\n")

    print("So, if the company wants to increase the click-through rate, it may prefer the control group.")






