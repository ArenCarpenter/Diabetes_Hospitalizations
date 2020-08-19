# Diabetes Hospitalizations

Aren Carpenter & JP Ventura 
Data Science Cohort 062220

## Introduction

Diabetes affects 30 million Americans, almost 10% of the population, as of 2015. It is a family of diseases that affects how your body can utilize blood sugar (specifically, glucose). While vital for powering your cells, a buildup of glucose in the blood can lead to serious health problems. Type I diabetes usually emerges pre-adolescence and is characterized by one's immune system incorrectly targeting insulin-producing cells. Type II can emerge at any age and is characterized by cells becoming resistent to insulin binding. This keeps glucose from being transported into the cells and causes a buildup of glucose in the blood. 

There are a plethora of factors that impact diabetes, including genetics and environmental factors. Family history is the driving factor for Type I diabetes. For Type II diabetes, in addition to family history, there are many more environmental factors, such as weight, inactivity, age, race, and other underlying health concerns. 

HbA1c is a measure of how glycated one's red blood cells are. This gives a better picture of glucose levels over a few months, rather than a single point test like blood glucose levels. For diabetics, just a 1% increase in HbA1c can increase microvascular complications by 25%. 


## The Model

We used a logistic regression model to enable interpreting our coefficients and drawing relative comparisons between features. 

### Data Collection & Cleaning

Our data set was a subset of some 75 million inpatient visits between 1998 and 2008. The specific dataset consists of 100,000 inpatient visits for only diabetic patients. Because this set spans ten years, we had to remove repeat visits as some patients were admitted several times in that period. The datset also had 25 features for specific diabetic treatments that had to be dropped as many were not used by any of our observations.

Show some EDA

### Feature Engineering

We observed that the effect of age on readmittance was clearly different between different age ranges. Therefore, we binned age into 0-30, 30-60, and 60-100 categories. Various diagnoses were reported when patients were admitted inpatient via ICD-9 medical billing codes, but only the first three were listed. It was intractable to use get_dummies due to the sheer number of possible diagnoses we observed. Therefore, we created columns for if diabetes (ICD-9 code 250.xx) was listed as one of the top diagnoses.

From outside research, we know that the HbA1C test is very important for assessing long-term management of glucose levels in the blood. However, less than 20% of inpatient visits resulted in a HbA1c test. Furthermore, if a patient was given a HbA1c test, one would hope that patient's medication would be adjusted if necessary. As we had a feature for 'Change in Meds' we were able to engineer a feature for when a patient likely needed an adjustment and if it was done or not. 

EDA for HbA1c

## Insights and Suggestions

The main insight

Vis

Some lesser insights

Vis

Recommendations

## Future Directions

What could we do better? 

What could we do next?

