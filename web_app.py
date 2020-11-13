import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

st.header("Predicting Diabetes Rehospitalizations")
st.write("""
This is a Streamlit web app created so users could explore my multiple logistic regression model predicting the need for
rehospitalization of diabetic patients based on a numnber of electronic health records (EHR). 

This [data](https://data.world/uci/diabetes-130-us-hospitals-for-years-1999-2008) was collected from diabetic 
patients from 1998 - 2008 and only consists of inpatient hospitalizations lasting at least 1 day. There are about 
100,000 observations.

Use the sidebar to select input features. Each feature defaults to its mean or mode, as appropriate.

""")

st.sidebar.header('User Input Features')

def user_input_features():
    race = st.sidebar.selectbox('Race', ('Caucasian', 'AfricanAmerican', 'Hispanic', 'Other', 'Asian'))
    gender = st.sidebar.selectbox('Gender', ('Female', 'Male'))
    binned_age = st.sidebar.selectbox('Age Group', ('[0-30)', '[30-60)', '[60-100)'))
    A1Cresult = st.sidebar.selectbox('HbA1c Test Result', ('None', 'Norm', '>7', '>8'))
    A1C_test = st.sidebar.selectbox('Got HbA1c Test?', (0, 1))
    change = st.sidebar.selectbox('Change in Meds?', (0, 1))
    A1C_test_and_changed = st.sidebar.selectbox('Got HbA1c Test and Change in Meds?', (0, 1))
    time_in_hospital = st.sidebar.slider('Days in Hospital', 1, 14, 4)
    num_lab_procedures = st.sidebar.slider('Num of Lab Procedures', 1, 132, 44)
    num_procedures = st.sidebar.slider('Num of Procedures', 0, 6, 2)
    num_medications = st.sidebar.slider('Num of Medications', 1, 79, 16)
    number_outpatient = st.sidebar.slider('Num of Outpatient Visits', 0, 36, 1)
    number_emergency = st.sidebar.slider('Num of Emergency Visits', 0, 42, 0)
    number_inpatient = st.sidebar.slider('Num of Inpatient Visits', 0, 12, 0)
    number_diagnoses = st.sidebar.slider('Num of Diagnoses', 3, 16, 7)
    admission_type_id = st.sidebar.selectbox('Admission Type', (1, 2, 3, 4, 5, 6, 7, 8))
    discharge_disposition_id = st.sidebar.slider('Discharge Disposition', 1, 28, 4)
    admission_source_id = st.sidebar.slider('Admission Source', 1, 25, 4)
    max_glu_serum = st.sidebar.selectbox('Max Glucose Serum', ('None', 'Norm', '>200', '>300'))
    metformin = st.sidebar.selectbox('Prescribed Metformin?', ('No', 'Steady', 'Up', 'Down'))
    glipizide = st.sidebar.selectbox('Prescribed Glipizide?', ('No', 'Steady', 'Up', 'Down'))
    glyburide = st.sidebar.selectbox('Prescribed Glyburide?', ('No', 'Steady', 'Up', 'Down'))
    insulin = st.sidebar.selectbox('Prescribed Insulin?', ('No', 'Steady', 'Up', 'Down'))
    diabetesMed = st.sidebar.selectbox('Taking Other Diabetes Med?', ('No', 'Yes'))
    diabetes_as_diag_1 = st.sidebar.selectbox('Diabetes as #1 Diagnosis? (Select one)', (0,1))
    diabetes_as_diag_2 = st.sidebar.selectbox('Diabetes as #2 Diagnosis? (Select one)', (0,1))
    diabetes_as_diag_3 = st.sidebar.selectbox('Diabetes as #3 Diagnosis? (Select one)', (0,1))

    data = {'time_in_hospital': time_in_hospital,
            'num_lab_procedures': num_lab_procedures,
            'num_procedures': num_procedures,
            'num_medications': num_medications,
            'number_outpatient': number_outpatient,
            'number_emergency': number_emergency,

            'number_inpatient': number_inpatient,
            'number_diagnoses': number_diagnoses,
            'admission_type_id': admission_type_id,
            'discharge_disposition_id': discharge_disposition_id,
            'admission_source_id': admission_source_id,

            'change': change,
            'A1C_test': A1C_test,
            'A1C_test_and_changed': A1C_test_and_changed,
            'diabetes_as_diag_1': diabetes_as_diag_1,
            'diabetes_as_diag_2': diabetes_as_diag_2,

            'diabetes_as_diag_3': diabetes_as_diag_3,
            'race': race,
            'gender': gender,
            'max_glu_serum': max_glu_serum,
            'A1Cresult': A1Cresult,

            'metformin': metformin,
            'glipizide': glipizide,
            'glyburide': glyburide,
            'insulin': insulin,
            'diabetesMed': diabetesMed,
            'binned_age': binned_age
            }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

df = pd.read_csv('https://query.data.world/s/fzhdybgova7pqh6amwfzrnhumdc26t')

# Data Cleaning Steps
df.drop_duplicates(subset='patient_nbr', inplace=True)
df.drop(['encounter_id','patient_nbr','weight', 'payer_code', 'medical_specialty'], axis=1, inplace=True)
df = df[df.race != '?'] # about 1,000 obs
df = df[df.gender != 'Unknown/Invalid'] # 1 obs
df.readmitted.replace({'NO': 0, '<30': 1, '>30': 2}, inplace=True)

df = df[pd.to_numeric(df['diag_1'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['diag_2'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['diag_3'], errors='coerce').notnull()]

df.diag_1 = df.diag_1.astype('float64')
df.diag_2 = df.diag_2.astype('float64')
df.diag_3 = df.diag_3.astype('float64')

# Feature Engineering
df['A1C_test'] = np.where(df.A1Cresult == 'None', 0, 1)
df.change = np.where(df.change == 'No', 0, 1)
df['A1C_test_and_changed'] = np.where((df.change == 1) & (df.A1C_test == 1), 1, 0)

conditions = [
    (df.age ==  '[0-10)') | (df.age == '[10-20)') | (df.age == '[20-30)'),
    (df.age == '[30-40)') | (df.age == '[40-50)') | (df.age == '[50-60)'),
    (df.age == '[60-70)') | (df.age == '[70-80)') | (df.age == '[80-90)') | (df.age == '[90-100')]

choices = [
    '[0-30)',
    '[30-60]',
    '[60-100)']

df['binned_age'] = np.select(conditions, choices, default=np.nan)
df = df[df.binned_age != 'nan']
df.drop(['age'], axis=1, inplace=True)

df['diabetes_as_diag_1'] = np.where((df.diag_1 >= 250) & (df.diag_1 <251), 1, 0)
df['diabetes_as_diag_2'] = np.where((df.diag_2 >= 250) & (df.diag_2 <251), 1, 0)
df['diabetes_as_diag_3'] = np.where((df.diag_3 >= 250) & (df.diag_3 <251), 1, 0)
df.drop(['diag_1', 'diag_2', 'diag_3'], axis=1, inplace=True)

meds_to_remove = ['repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', 'tolbutamide',
            'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone', 'tolazamide', 'examide',
            'citoglipton', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone',
            'metformin-rosiglitazone', 'metformin-pioglitazone']
df.drop(meds_to_remove, axis=1, inplace=True)

X = df.drop('readmitted', axis = 1)
df = pd.concat([input_df, X], axis=0)

encode = ['race', 'gender', 'max_glu_serum', 'A1Cresult', 'metformin', 'glipizide', 'glyburide',
          'insulin', 'diabetesMed', 'binned_age']

for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]
df = df[:1]

#Write out input selection
st.subheader('User Input (Pandas DataFrame)')
st.write(df)

#Load in model
load_clf = pickle.load(open('diabetes_model.pkl', 'rb'))

# Apply model to make predictions
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader('Prediction')
st.write("""
This is a multi-class classification model. Options are: 

1) 'NO' --> this patient was not readmitted within a year, 

2) '<30' --> this patient was readmitted within 30 days, or 

3) '>30' --> this patient was readmitted after 30 days. 

This generally corresponds to the severity of the patient's diabetes as well as the specific care, or lack thereof, during the visit.
""")

readmitted = np.array(['NO','<30','>30'])
st.write(readmitted[prediction])

st.subheader('Prediction Probability')
st.write("""
0 --> 'NO'

1 --> '<30'

2 --> '>30'
""")
st.write(prediction_proba)

st.subheader('Exploratory Data Analysis')
st.write("""
We identified some important features in the readmittance rate that you can explore below. To begin, here is the distribution
of the classes in the original data set. We see that a majority of patients are not readmitted within a year. Patients that 
are readmitted often have complications to their diabetes or the specific care recieved.
""")
st.image(Image.open('Images/Readmit_rate.png'), width = 500)

st.write("""
Now looking at the patient population given the long-term blood sugar HbA1c test, we see only about 20% of patients received
this test, but, of those, 50% then had their medication changed and were less likely to be readmitted.
""")
st.image(Image.open('Images/HbA1c_test.png'), width = 500)

st.write("""
Finally, we see that age plays an important role. As expected, older patients have more complications due to their diabetes.
Age was binned according to this chart into 0-30, 30-60, and 60-100.
""")
st.image(Image.open('Images/Readmit_vs_age.png'), width = 500)

st.subheader('More Information')
st.write("""
For a deeper dive into the project, please visit the [repo on GitHub](https://github.com/ArenCarpenter/Diabetes_Hospitalizations) 
where you can find all the code used in analysis, modeling, visualizations, etc. You can also read my 
[articles](https://arencarpenter.medium.com/) in Towards Data Science on my other projects. 
""")