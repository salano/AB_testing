from src.exception import CustomException
from src.logger import logging
import sys
import numpy as np
import pandas as pd


from scipy.stats import shapiro
from statsmodels.stats.proportion import proportions_ztest
import scipy.stats as stats


# A/B Testing  on continuous metrics-------solution
def AB_Test_continuous(dataframe, group, target, Group_value_1, msg):
    try:
        u_test = None
        print("A/B Testing\n")

        print("Assumptions:\n")
        print("    Check normality.\n")
        print("    If Normal Distribution, check homogeneity\n")

        '''
        Steps:¶
            Split & Define Control Group & treatment Group
            Apply Shapiro Test for normality
            If parametric apply Levene Test for homogeneity of variances
            If Parametric + homogeneity of variances apply T-Test
            If Parametric - homogeneity of variances apply Welch Test
            If Non-parametric apply Mann Whitney U Test directly
        '''

        # Define A/B groups
        dataframe[group] = np.where(dataframe[group] == Group_value_1, "A", "B")
        
        # Split A/B
        groupA = dataframe[dataframe[group] == "A"][target]
        groupB = dataframe[dataframe[group] == "B"][target]

        # Assumption: Normality
        ntA = shapiro(groupA)[1] < 0.05
        ntB = shapiro(groupB)[1] < 0.05

        test_statA, A_pvalue = shapiro(groupA)
        test_statB, B_pvalue = shapiro(groupB)
        # H0: Distribution is Normal! - False
        # H1: Distribution is not Normal! - True
        print('Test Stat - Group A = %.4f, p-value = %.4f' % (test_statA, A_pvalue))
        if A_pvalue > 0.05:
            print("H0 is accepted for {} group --pvalue {}".format('Control', B_pvalue))
        else:
            print("H0 is rejected for {} group --pvalue {}".format('Control', B_pvalue))

        print('Test Stat - Group B = %.4f, p-value = %.4f' % (test_statB, B_pvalue))
        if B_pvalue > 0.05:
            print("H0 is accepted for {} group --pvalue {}".format('Treatment', B_pvalue))
        else:
            print("H0 is rejected for {} group --pvalue {}".format('Treatment', B_pvalue))

        if (ntA == False) & (ntB == False): # "H0: Normal Distribution"
            # Parametric Test
            # Assumption: Homogeneity of variances
            print('Variance Homogenity Assumption\n')
            print("Levene's Test\n")

            print("H0: Variances are Homogeneous.\n")

            print("H1: Variances are not Homogeneous.\n")
            leveneTest = stats.levene(groupA, groupB)[1] < 0.05
            # H0: Homogeneity: False
            # H1: Heterogeneous: True
            test_stat, pvalue = stats.levene(groupA, groupB)
            print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

            if pvalue > 0.05:
                print("H0 is accepted for {}  --pvalue {}".format('homogeneous variance distribution is provided', pvalue))
            else:
                print("H0 is rejected for {}  --pvalue {}".format('homogeneous variance distribution not is provided', pvalue))

            print("Independent Samples T Test\n")
            
            if leveneTest == False:
                # Homogeneity
                u_test = "T-test (homogenity)"
                print("Independent Samples T Test\n")
                print("We checked these necessary conditions in the previous step. Again, the dependent variable in each group should be normally distributed (Normality), but Variances is not homogeneous. (No Homogeneity)\n")
                print("Apart from these two conditions, the following conditions must also be met:\n")
                print("    The dependent variable must be continuous.\n")
                print("    The argument must be categorical.\n")
                print("    The dataset should not contain outliers.\n")
                ttest = stats.ttest_ind(groupA, groupB, equal_var=True)[1]
                # H0: M1 == M2 - False
                # H1: M1 != M2 - True
                test_stat, pvalue = stats.ttest_ind(groupA, groupB, equal_var=True)
                print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

                if pvalue > 0.05:
                    print("H0 is accepted : {}  --pvalue {}".format(f'There is no statistically significant difference between the {msg} of the control and treatment groups.', pvalue))
                else:
                    print("H0 is rejected : {}  --pvalue {}".format(f'There is statistically significant difference between the {msg} of the control and treatment groups.', pvalue))

            else:
                # Heterogeneous
                u_test = "T-test (Heterogeneous)"
                print("Independent Samples T Test\n")
                print("We checked these necessary conditions in the previous step. Again, the dependent variable in each group should be normally distributed (Normality). Variances should be homogeneous. (Homogeneity)\n")
                print("Apart from these two conditions, the following conditions must also be met:\n")
                print("    The dependent variable must be continuous.\n")
                print("    The argument must be categorical.\n")
                print("    The dataset should not contain outliers.\n")
                ttest = stats.ttest_ind(groupA, groupB, equal_var=False)[1]
                # H0: M1 == M2 - False
                # H1: M1 != M2 - True
                test_stat, pvalue = stats.ttest_ind(groupA, groupB, equal_var=False)
                print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

                if pvalue > 0.05:
                    print("H0 is accepted : {}  --pvalue {}".format(f'There is no statistically significant difference between the {msg} of the control and treatment groups.', pvalue))
                else:
                    print("H0 is rejected : {}  --pvalue {}".format(f'There is statistically significant difference between the {msg} of the control and treatment groups.', pvalue))
        else:
            # Non-Parametric Test
            u_test = "Mann Whitney U"
            print("Mann–Whitney U test\n")

            print("A few necessary prerequisites for this test can be listed as follows:\n")
            print("    The independent variable must be categorical.\n")
            print("    The dependent variable must be continuous or sequential.\n")
            print("    The sample selected from the population should be random.\n")
            print("    The scores obtained from the groups should not show normal distribution.\n")
            ttest = stats.mannwhitneyu(groupA, groupB)[1] 
            # H0: M1 == M2 - False
            # H1: M1 != M2 - True
            test_stat, pvalue = stats.mannwhitneyu(groupA, groupB)
            if pvalue > 0.05:
                print("\nH0 is accepted : {}  --pvalue {}".format(f'There is no statistically significant difference between the {msg} of the control and treatment groups.', pvalue))
            else:
                print("\nH0 is rejected : {}  --pvalue {}".format(f'There is statistically significant difference between the {msg} of the control and treatment groups.', pvalue))

        # Result
        temp = pd.DataFrame({
            "AB Hypothesis":[ttest < 0.05], 
            "p-value":[ttest],
            "Test": u_test
        })
        temp["Test Type"] = np.where((ntA == False) & (ntB == False), "Parametric", "Non-Parametric")
        temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Fail to Reject H0", "Reject H0")
        temp["Comment"] = np.where(temp["AB Hypothesis"] == "Fail to Reject H0", "A/B groups are similar!", "A/B groups are not similar!")

        # Columns
        if (ntA == False) & (ntB == False):
            temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")
            temp = temp[["Test", "Test Type", "Homogeneity","AB Hypothesis", "p-value", "Comment"]]
        else:
            temp = temp[["Test", "Test Type","AB Hypothesis", "p-value", "Comment"]]
        
        # Print Hypothesis
        print("# A/B Testing Hypothesis")
        print("H0: A == B")
        print("H1: A != B", "\n")
        
        return temp
            
    except Exception as e:
        raise CustomException(e, sys)
    
# A/B Testing on discrete metrics-------solution
def AB_test_discrete(dataframe, group, metric, msg):
    try:
        print("Hypothesis:\n")
        print(f"H0: {msg} of Control verson = {msg} of treatment\n")

        print(f"H1: {msg} of Control verson != {msg} of treatment\n")

        prob = 0.95
        # interpret p-value
        alpha = 1-prob
        # Split groups
        group_c = dataframe[dataframe[group] == "control"][metric]
        group_t = dataframe[dataframe[group] == "treatment"][metric]
        
        size = dataframe.shape[0]  
        table = pd.DataFrame({"C_COUNT": group_c.value_counts(),
                "T_COUNT": group_t.value_counts()}).to_numpy()
        
        if size < 1000:
            # Fisher Exact Test
            odd_ratio, p_value = stats.fisher_exact(table, alternative="two-sided")
            print("odd ratio is : " + str(odd_ratio))
            print("p_value is : " + str(p_value))
        else:
            # Pearson Chi Square Test
            stat, p_value, dof, expected = stats.chi2_contingency(table)
            prob = 0.95
            critical = stats.chi2.ppf(prob, dof)
            print('probability=%.3f, critical=%.3f, stat=%.3f, fredoom of degree=%d' % (prob, critical, stat, dof))
        # Result
        temp = pd.DataFrame({
            "Test":[size<1000],
            "P_value":[p_value],
            "AB Hypothesis":[p_value < 0.05], 
        })
        temp["Test"] = np.where(temp["Test"]==True, "Fisher Exact Test", "Chi Square Test")
        temp["AB Hypothesis"] = np.where(temp["AB Hypothesis"] == False, "Fail to Reject H0", "Reject H0")
        temp["Comment"] = np.where(temp["AB Hypothesis"] == "Fail to Reject H0", "A/B groups are similar!", "A/B groups are not similar!")
        
        return temp
    except Exception as e:
        raise CustomException(e, sys)
    

# Proportion A/B Testing on continuous metrics (two datasets)-------solution
def AB_testing_prop1(df1, df2, category, response, meaure_msg: str):
    try:
        print("Two Proportion Z-Test")
        print("The Two-Proportions Z-Test is used to compare two ratios.\n")

        print(f"H0 : There is a statistically significant difference between the {meaure_msg} of control and treatment groups.")
        print(f"H1 : There is no statistically significant difference between the {meaure_msg}s of control and treatment groups.")

        response_a = df1[response].sum()
        category_a = df1[category].sum()
        print(response_a/category_a)

        response_b = df2[response].sum()
        category_b = df2[category].sum()
        print(response_b/category_b)

        nresponse = np.array([response_a, response_b])

        n_categories = np.array([category_a, category_b])

        p_stat, pvalue = proportions_ztest(count=nresponse, nobs=n_categories)
        if pvalue > 0.05:
            print("H0 is accepted: {} --pvalue {}".format('There is a statistically significant difference between the groups', pvalue))
        else:
            print("H0 is rejected {} --pvalue {}".format('There is no statistically significant difference between the groups', pvalue))

    except Exception as e:
        raise CustomException(e, sys)
    

# Proportion A/B Testing on continuous metrics-------solution
def AB_testing_prop2(dataframe, group, group_value, category, response, meaure_msg: str):
    try:
        print("Two Proportion Z-Test")
        print("The Two-Proportions Z-Test is used to compare two ratios.\n")

        print(f"H0 : There is a statistically significant difference between the {meaure_msg} of control and treatment groups.")
        print(f"H1 : There is no statistically significant difference between the {meaure_msg}s of control and treatment groups.")

        # Split groups
        group_c = dataframe[dataframe[group] == group_value]
        group_t = dataframe[dataframe[group] != group_value]

        response_a = group_c[response].sum()

        category_a = group_c[category].sum()
        print(response_a/category_a)

        response_b = group_t[response].sum()
        category_b = group_t[category].sum()
        print(response_b/category_b)

        nresponse = np.array([response_a, response_b])

        n_categories = np.array([category_a, category_b])

        p_stat, pvalue = proportions_ztest(count=nresponse, nobs=n_categories)
        if pvalue > 0.05:
            print("\nH0 is accepted: {} --pvalue {}".format('There is a statistically significant difference between the groups', pvalue))
        else:
            print("\nH0 is rejected {} --pvalue {}".format('There is no statistically significant difference between the groups', pvalue))

    except Exception as e:
        raise CustomException(e, sys)
    
    