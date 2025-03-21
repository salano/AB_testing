Business problems
Which search tag generate more revenue through advertisement '#The Power of X' or '#Be Bold. Be X'?
Which search tag generate a higher click through rate '#The Power of X' or '#Be Bold. Be X'?

Data Exploration # DIMENSIONS -------------------------
Observation: 72612 Column: 3

    # DTYPES -----------------------------
    Object Variables:
    # of Variables: 1
    ['search_tags']

    Integer Variables:
    # of Variables: 2
    ['impressions', 'clicks']

    # MISSING VALUE ---------------------
    Are there any missing values?
    No missing value!

    # of rows in tag A: 12116
    # of rows in tag B: 12077

    First five records

    search_tags  impressions  clicks
    0  #The Power of X          837       8
    1   #Be Bold. Be X         2634      44
    3   #Be Bold. Be X         2327      48
    4   #Be Bold. Be X         1538      20
    5   #Be Bold. Be X          813      11

Use the first 12000 rows from both search tags since the total data points in both tags are not the same.

The dataset don't contain a revenue column,
so adding a revenue column using a random normal distribution with mean mean:93273 and standard dev: 1444
for testing purposes.

Top 5 records after adding revenue Column search_tags impressions clicks revenue
0 #The Power of X 837 8 93240.15452
15 #The Power of X 618 5 93215.00448
17 #The Power of X 617 7 94419.00627
20 #The Power of X 996 14 91437.42533
21 #The Power of X 868 20 96071.37615

Plot the search tags against revenue
Quantilte-Quantile plot - Straight diagonal line indicates normality
![Alt text](data\QQ_1.png)
Histograms and boxplots plot - Distribution of data
![Alt text](data\QQ_1.png)
As expected the data looks normally distributed from the histogram, boxplot and Quantile - Quantile plots

Summary statictics of revenue:

All records unique: True
count mean std min 1% \
revenue 24000.00000 93269.68385 1441.92904 86863.88657 89935.27660

                 5%         10%         20%         50%         80%  \

revenue 90902.13397 91424.47235 92051.51317 93269.08709 94474.19124

                90%         95%         99%         max

revenue 95117.31637 95642.54761 96650.06996 98918.74962

The number of records below 25.0% is 6000 with a value of 548619587.3918992 or 24.5% of total.

The number of records below 50.0% is 12000 with a value of 1105438161.6726909 or 49.4% of total.

The number of records below 75.0% is 18000 with a value of 1667852268.0931094 or 74.5% of total.

The number of records below 99.0% is 23760 with a value of 2215171421.094448 or 99.0% of total.

24000 of records lies within 2 STD of the mean value from a total 24000 population

                    count      median        mean        std         max
    search_tags
    #Be Bold. Be X   12000 93270.29453 93265.41444 1439.05172 98486.12084
    #The Power of X  12000 93264.65878 93273.95326 1444.84798 98918.74962

We can see from the summary statictis that the means of the search tags are similar:

93265 and 93273 for '#The Power of X' and '#Be Bold. Be X' respectively

OUTLIERS

25th=92302, 75th=94254, IQR=1951, Lower=89374, Upper=97181

Outliers are identified as any revenue value whic is 1.5 times the IQR

The number of Identified outliers: 154
Percent of outliers: 0.64%

Since the percentage is so low and we generated the revenue randomly from a normal distribution we will not remove any outlies for this test

A/B Testing

For the test, we assign '#The Power of X' and '#Be Bold. Be X' for group (A) and group (B) respectively

We perform a Shapiro-Wilk test for normality on both groups
Test Stat - Group A = 0.9997, p-value = 0.1260
H0 is accepted for Control group --pvalue 0.20900237560272217
Test Stat - Group B = 0.9998, p-value = 0.2090
H0 is accepted for Treatment group --pvalue 0.20900237560272217

The Shapiro-Wilk test indicates both of the groups data points are normally distributed

We now perform Levene''s Test to determine if there are Homogenity between the variences in the groups

H0: Variances are Homogeneous.

H1: Variances are not Homogeneous.

Test Stat = 0.4991, p-value = 0.4799
H0 is accepted for homogeneous variance distribution is provided --pvalue 0.47990114927181504

From results of the Levene''s Test, we conclude that the variences between the two groups are similar

Independent Samples T Test
We will now conduct an Independent Sample T-test to determine if the average revenue between the two groups are similar

Test Stat = 0.6140, p-value = 0.5392
H0 is accepted : There is no statistically significant difference between the Average Revenue of the control and treatment groups. --pvalue 0.5392083546793202

As a result of Independent Samples T Test, there is no a statistically significant difference between the groups
because p-value = 0.5392 < 0.05 so H0 is accpted. Considering the is no gain between groups, the gains are similar
at 93265 and 93273 for '#The Power of X' and '#Be Bold. Be X'.

We will no perform a two proportion Z-test (A/B test) using the ad views (impressions) and the amount of clicks

Two Proportion Z-Test
The Two-Proportions Z-Test is used to compare two ratios.

H0 : There is a statistically significant difference between the Click Through Rate of '#The Power of X' and '#Be Bold. Be X' groups.
H1 : There is no statistically significant difference between the Click Through Rates of '#The Power of X' and '#Be Bold. Be X' groups.
0.04224761423243143
0.0368355487771523

H0 is rejected There is no statistically significant difference between the groups --pvalue 0.0
The click through rates are similar between the groups. In both cases 4 out of 100 people will click on the ad
