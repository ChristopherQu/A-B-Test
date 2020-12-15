#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from scipy import stats
import math


# ### Invariants: Number of cookies:
# - Number of Cookies
# - Number of Clicks
# - Click-through Probability

# ### 1. Calculating Standard Deviation
# #### Baseline Values
# <font face = 'Segoe UI'>Unique cookies to view course overview page per day: 40000<br>
# Unique cookies to click "Start free trial" per day: 3200<br>
# Enrollments per day: 660<br>
# Click-through-probability on "Start free trial": 0.08<br>
# Probability of enrolling, given click: 0.20625<br>
# Probability of payment, given enroll: 0.53<br>
# Probability of payment, given click: 0.1093125</font>

# #### When the sample size is equal to 5,000, we got the following standard errors for each metric.

# In[2]:


# sample size for the metrics
sampleSize = 5000
ratio = 5000 / 40000
startCookie = 3200 * ratio
enrollment = 660 * ratio

# STD for gross conversion
p1 = 0.20625
grossConv = round(math.sqrt(p1 * (1 - p1) / startCookie), 4)
print("STD for Gross Conversion: " + str(grossConv))

# STD for rentention
p2 = 0.53
rentention = round(math.sqrt(p2 * (1 - p2) / enrollment), 4)
print("STD for Rentension: " + str(rentention))

# STD for Net conversion
p3 = 0.1093125
netConv = round(math.sqrt(p3 * (1 - p3) / startCookie), 4)
print("STD for Net Rentension: " + str(netConv))


# ### 2. The Number of Page Views needed
# #### Sample Size:
# <font face = 'Segoe UI'>By using <font face = 'Segoe UI Black'>Sample Size Calculator</font> (link: https://www.evanmiller.org/ab-testing/sample-size.html), I got the following sample size results for each evaluation metrics.<br>
# Gross Conversion: 25,835<br>
# Rentension: 39,115<br>
# Net Conversion: 27,413<br> 
# </font>
# #### Page View

# In[3]:


pageGC = 2 * 25835 / 3200 * 40000
pageR = 2 * 39115 / 660 * 40000
pageNC = 2 * 27413 / 3200 * 40000
totalPage = round(max(pageGC, pageR, pageNC), 0)
print("Page View for Gross Conversion: " + str(pageGC))
print("Page View for Rentension: " + str(pageR))
print("Page View for Net Conversion: " + str(pageNC))
print("The page views that will be needed for this test is: " + str(totalPage))


# #### Length of Experiment
# <font face = 'Segoe UI'>Assume 100% traffic will be diverted to this experiment

# In[4]:


# Days for all three metrics
print("Days for all three metrics: " + str(round(totalPage / 40000, 0)))

# Days for the metrics of Gross Conversion and Net Conversion
print("Days for Gross Conversion and Net Conversion metrics: " + str(round(pageNC / 40000, 0)))


# <font face = 'Segoe UI'> Based on results above, we could know if we take three metrics into account, the experiment will last too long. However, taking only two metrics will just take 17 days. Therefore, we could decrease the traffic percentage to increase the days of experiment for two metrics.<br><br>Here, we will test 40% and 60% to see the changes.

# In[5]:


print("Days for Gross Conversion and Net Conversion metrics (40%): " + str(round(pageNC / (40000 * 0.4), 0)))
print("Days for Gross Conversion and Net Conversion metrics (60%): " + str(round(pageNC / (40000 * 0.6), 0)))


# <font face = 'Segoe UI'>Based on the results above, diverting 60% of traffic could be a better percentage for both analysis and experiment because we have both enough time period and reliable results.

# ### 3. Sanity Check
# <font face = 'Segoe UI'>For the invariant Metrics

# In[6]:


controlDF = pd.read_excel("Final Project Results.xlsx", sheet_name = "Control")
experimentDF = pd.read_excel("Final Project Results.xlsx", sheet_name = "Experiment")


# In[7]:


# Calculate the number of page views and clicks in both group
controlPage = controlDF.Pageviews.sum()
controlClick = controlDF.Clicks.sum()
experimentPage = experimentDF.Pageviews.sum()
experimentClick = experimentDF.Clicks.sum()

# Set p = 0.5 because we expect two groups could have the same number of views or click for the test.
P = 0.5
MUTIPLE = 1.96

# For cookies
stdCookies = math.sqrt(P * (1 - P) / (controlPage + experimentPage))
meanCookies = 0.5
cookieLB, cookieUB = round(meanCookies - MUTIPLE * stdCookies, 4), round(meanCookies + MUTIPLE * stdCookies, 4)
print("The confidential interval for cookies: " + str(tuple([cookieLB, cookieUB])))
print("Observerd value for cookies: " + str(round(controlPage / (controlPage + experimentPage), 4)) + "\n")

# For clicks
stdClicks = math.sqrt(P * (1 - P) / (controlClick + experimentClick))
meanClicks = 0.5
clickLB, clickUB = round(meanClicks - MUTIPLE * stdClicks, 4), round(meanClicks + MUTIPLE * stdClicks, 4)
print("The confidential interval for clicks: " + str(tuple([clickLB, clickUB])))
print("Observerd value for clicks: " + str(round(controlClick / (controlClick + experimentClick), 4)) + "\n")

# For Click-through-probability
clickProb = (controlClick + experimentClick) / (controlPage + experimentPage) # pooled prob
stdClicks = math.sqrt(clickProb * (1 - clickProb) * (1 / controlPage + 1 / experimentPage)) # std
clickDiff = (experimentClick / experimentPage) - (controlClick / controlPage) # diff between control and exp
clickMOE = 1.96 * stdClicks # Margin of Error
clickLB, clickUB = round(-1 * clickMOE, 4), round(clickMOE, 4)
print("The confidential interval for CTP: " + str(tuple([clickLB, clickUB])))
print("Observerd value for CTP: " + str(round(clickDiff, 4)))


# ### 4. Effect Size Tests
# <font face = 'Segoe UI'>For each of evalution metrics: Gross Conversion & Net Conversion

# In[8]:


# Remove all NA values first
controlDF2 = controlDF.dropna(axis = 0, thresh = 4)
experimentDF2 = experimentDF.dropna(axis = 0, thresh = 4)

# Caculating Gross Conversion
controlClick2 = controlDF2.Clicks.sum()
controlEnroll = controlDF2.Enrollments.sum()
experimentClick2 = experimentDF2.Clicks.sum()
experimentEnroll = experimentDF2.Enrollments.sum()

grossConversionProb = (controlEnroll + experimentEnroll) / (controlClick2 + experimentClick2) # Probability
stdGrossConversion = math.sqrt(grossConversionProb * (1 - grossConversionProb) * (1 / controlClick2 + 1 / experimentClick2)) # std
grossConversionDiff = experimentEnroll / experimentClick2 - controlEnroll / controlClick2
grossConversionMOE = 1.96 * stdGrossConversion # Margin of error for Gross Conversion
grossConversionLB, grossConversionUB = round(grossConversionDiff - grossConversionMOE, 4),                                         round(grossConversionDiff + grossConversionMOE, 4)
print("The confidential interval for Gross Conversion: " + str(tuple([grossConversionLB, grossConversionUB])))

# Calculating Net Conversion
controlPayment = controlDF2.Payments.sum()
experimentPayment = experimentDF2.Payments.sum()

netConversionProb = (controlPayment + experimentPayment) / (controlClick2 + experimentClick2) # Probability
stdNetConversion = math.sqrt(netConversionProb * (1 - netConversionProb) * (1 / controlClick2 + 1 / experimentClick2))
netConversionDiff = experimentPayment / experimentClick2 - controlPayment / controlClick2
netConversionMOE = 1.96 * stdNetConversion
netConversionLB, netConversionUB = round(netConversionDiff - netConversionMOE, 4), round(netConversionDiff + netConversionMOE, 4)
print("The confidential interval for Net Conversion: " + str(tuple([netConversionLB, netConversionUB])))


# <font face = 'Segoe UI'>The boundary for minimum detectable effect for Gross Conversion is __0.01__, the confidential interval we got from test result is __(-0.0291, -0.0120)__. Since (-0.01, 0.01) isn't in the confidential interval and the confidential interval doesn't include 0, we could say the experiment is __practical significance and statistical significance__.<br>The boundary for minimum detectable effect for Net Conversion is __0.0075__, the confidential interval we got from test result is __(-0.0116, 0.0019)__. Since the subset (-0.0075, 0.0019) of (-0.0075, 0.0075) is in the confidential interval and the confidential interval includes 0, we could say the experiment is __NOT practical significance and NOT statistical significance__.

# ### 5. Sign Test for evaluation metrics
# <font face = 'Segoe UI'>Under 95% confidence level

# In[9]:


# Construct a new DataFrame for the analysis
controlDF3 = controlDF2.set_index("Date")
experimentDF3 = experimentDF2.set_index("Date")
combinedDF = controlDF3.join(experimentDF3, lsuffix = "_con", rsuffix = "_exp")
combinedDF['GrossConversion_con'] = combinedDF['Enrollments_con'] / combinedDF['Clicks_con']
combinedDF['NetConversion_con'] = combinedDF['Payments_con'] / combinedDF['Clicks_con']
combinedDF['GrossConversion_exp'] = combinedDF['Enrollments_exp'] / combinedDF['Clicks_exp']
combinedDF['NetConversion_exp'] = combinedDF['Payments_exp'] / combinedDF['Clicks_exp']

combinedDF = combinedDF[combinedDF['GrossConversion_con'] != combinedDF['GrossConversion_exp']]
combinedDF = combinedDF[combinedDF['NetConversion_con'] != combinedDF['NetConversion_exp']]

combinedDF['GrossConversionSuccess'] = combinedDF['GrossConversion_exp'] > combinedDF['GrossConversion_con']
combinedDF['NetConversionSuccess'] = combinedDF['NetConversion_exp'] > combinedDF['NetConversion_con']

# Count the number for Sign test
total = len(combinedDF)
gcSuccess = len(combinedDF[combinedDF['GrossConversionSuccess'] == True])
ncSuccess = len(combinedDF[combinedDF['NetConversionSuccess'] == True])

pValueGC = round(stats.binom_test(gcSuccess, n = total, p = 0.5), 4)
pValueNC = round(stats.binom_test(ncSuccess, n = total, p = 0.5), 4)
print("P-value for Gross Conversion: " + str(pValueGC))
print("P-value for Net Conversion: " + str(pValueNC))


# <font face = 'Segoe UI'>Since the P-value for Gross Conversion is __0.0026 < 0.05__, thus, we could reject the Null Hypothesis. Also, Gross Conversion is __Statistical Significance__.<br>
# For Net Conversion, its p-value is __0.6776 > 0.05__. We are unable to reject Null Hypothesis, thus, it is __NOT Statistical Significance__.

# ### 6. Conclusion
# <font face = 'Segoe UI'>For Net Conversion, both Effect Size Test and Sign Test are not statistical significance and practical significance, which may not be the basis for the conclusion. Besides, the confidential interval also indicates Udacity has the risk of losing money from users.<br><br>For the Gross Conversion, both Effect Size Test and Sign Test are statistical significance and practical significance, this means we indeed could decrease the number of students who enroll the courses when they see the notification, which correspondingly could decrease the cost for the users in the trial period.<br><br>To help students get a better understanding of whether they are qualified or not for the course, we could also add a pre-requisite test for them before they click the "Start free trial" to help them test themselves. This could also be evaluated with another A/B test.
