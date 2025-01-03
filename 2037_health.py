# -*- coding: utf-8 -*-
"""2037_Health.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i7woQ5Pd32S6-nb8RLJvaEOPKQpT6MzV
"""

!pip install Kaggle
!pip install -U dataprep
!pip install pycaret[full]

!pip install jinja2==3.1.2

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from dataprep.eda import *
from pycaret.classification import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns

from google.colab import files
uploaded = files.upload()

df=pd.read_csv('aw_fb_data.csv')

df.head()

df=df.drop(['Unnamed: 0','X1'],axis=1)

df.info()

df_aw=df[df['device']=='apple watch']

df_fb=df[df['device']=='fitbit']

df_aw=df_aw.drop('device',axis=1)

df_fb=df_fb.drop('device',axis=1)

df_fb['activity'].value_counts()

labels = ['Lying','Running 7 METs','Running 5 METs','Running 3 METs', 'Sitting', 'Self Pace walk'] # καθορισμός ετικετών

values = df_aw['activity'].value_counts() # μετρήσεις των δραστηριοτήτων στο DataFrame 'df_aw'

colors = ['red', 'royalblue','green','yellow','pink','grey'] # καθορισμός χρωμάτων

fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)]) # δημιουργία διαγράμματος πίτας με Plotly

fig.update_traces(hoverinfo='label+value',textfont_size=15,marker=dict(colors=colors)) #ρυθμίσεις στοιχείων διαγράμματος

fig.update_layout(annotations=[dict(text='AW 6 types of Activity', x=0.50, y=0.5, font_size=15, showarrow=False)]) # ρυθμίσεις ετικετών

fig.show() # εμφάνιση διαγράμματος

df_aw.plot()

sns.pairplot(df_aw,hue='activity')

df_train, df_test = train_test_split(df_aw, random_state =100 ,test_size = 0.3)

setup_df = setup( data= df_train, target = 'activity',session_id=100, data_split_stratify=True, remove_outliers=True)

lgbm = create_model("lightgbm")

plot_model(estimator = lgbm, plot= "confusion_matrix",plot_kwargs = {'percent' : True})

predict_model(lgbm)

pred = predict_model(lgbm, data=df_test)

pred.head()

rf = create_model("rf")

plot_model(estimator=rf, plot="confusion_matrix", plot_kwargs={'percent': True})

predict_model(rf)

pred = predict_model(rf, data=df_test)

pred.head()

#Στην συγκεκριμένη εργασία, και οι δύο αλγόριθμοι έχουν σε μεγάλο βαθμό ακριβώς ίδια αποτελέσματα όσο αφορά τα νούμερα των metrics.
#Ωστόσο, ο RandomForest είναι οριακά καλύτερος εάν κρίνουμε από:
#AUC (rf...0.9482) ενώ (lgbm...0.9406).
#Επίσης, Kappa (rf...0.6960) ενώ (lgbm...0.6958).
#Τελικά, με βάση τα αποτελέσματα ο Random Forest είναι το καλύτερο μοντέλο, αν και με πολύ μικρή διαφορά.