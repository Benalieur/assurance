############################################################ Imports ############################################################
import streamlit as st
import pandas as pd
import numpy as np
from joblib import load


model = load('models/Pipeline.pkl')

############################################################ Fonctions ############################################################

def calculer_charge(infos:list):
    infos = np.array(infos)
    columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region']
    df = pd.DataFrame(infos.reshape(-1, len(columns)), columns=columns)

    predict = model.predict(df)
    predict = round(predict[0], 2)

    return predict

def calcul_bmi(bmi):
    if bmi < 18.5:
        bmi = "maigreur"
    elif bmi < 25:
        bmi = "normal"
    elif bmi < 30:
        bmi = "surpoids"
    elif bmi < 35:
        bmi = "obesite_moderee"
    elif bmi < 40:
        bmi = "obesite_severe"
    else:
        bmi = "obesite_morbide"

    return bmi

############################################################ Affichage ############################################################

st.title("Estimation de la prime d'assurance")

age = st.number_input("Age du client :", min_value=18)

sex = st.selectbox("Genre du client :",['female', 'male'])

bmi = st.radio("Connaissez-vous l'IMC du client ?", ['Oui', 'Non'])
imc = 20
if bmi == "Oui":
    imc = st.number_input("IMC du client :", min_value=0.0)
    imc = round(imc, 1)

if bmi == "Non":
    taille = st.number_input("Taille du client en cm :", min_value=0)
    poid = st.number_input("Poid du client en kg:", min_value=0.0)
    if taille != 0 and poid != 0:
        imc = round((poid / ((taille/10)**2))*100, 1)

if imc > 50:
    imc = 50

imc = calcul_bmi(int(imc))

enfants = st.number_input("Nombre d'enfants du client :", min_value=0)
if enfants > 5:
    enfants = 5

fumeur = st.radio("Le client est fumeur :", ['yes', 'no'])

if fumeur == 'yes':
    fumeur = 'Oui'
else : 
    fumeur = 'Non'

region = st.selectbox("Region du client :", ['southwest', 'southeast', 'northwest', 'northeast'])

if st.button('Calculer'):
    st.write(calculer_charge([age, sex, imc, enfants, fumeur, region]))