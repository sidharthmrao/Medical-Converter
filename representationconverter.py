import pandas as pd
import numpy as np
from diagnosisfunctions import textfixup as txtfix

sheet = 0


def main(sheet):

    df = pd.read_excel("Diagnosis_1-13.xlsx", sheet_name = [sheet])


    df = df[sheet]

    #Patient Info: Must be entered manually and deleted from xlsx sheet
    age = 19
    sex = "Female"
    print(f"What is the Final Diagnosis for Sheet {sheet+1}?")
    final = txtfix(input())[0]


    columns = df.columns.values

    symprob = df["Probability of Symptoms/Signs"]
    majcomp = txtfix(df["Major Complaint"][0])[0]
    othsign = df["Other Signs and Symptoms"]
    diffdia = [txtfix(x)[0] for x in df["Differential Diagnosis"] if str(x) != "nan"]
    probdia = df["Probability of Diagnosis"]
    pertneg = df["Pertinent Negatives"]
    severity= df["Severity"]
    nature  = df["Nature of Diagnosis"]

    class Diagnosis:
        def __init__(self, differentialdiagnosis, pertinentnegatives, severityofdiagnosis, probabilityofdiagnosis, natureofdiagnosis, othersignsandsymptoms, majorcomplaint, patientage, patientsex, finaldiagnosis):
            self.differentialdiagnosis = differentialdiagnosis
            self.pertinentnegatives = pertinentnegatives
            self.severityofdiagnosis = severityofdiagnosis
            self.probabilityofdiagnosis = probabilityofdiagnosis
            self.natureofdiagnosis = natureofdiagnosis
            self.othersignsandsymptoms = othersignsandsymptoms
            self.majorcomplaint = majorcomplaint
            self.patientage = patientage
            self.patientsex = patientsex
            self.finaldiagnosis = finaldiagnosis

    diagnoses = []



    for diagnum in range(len(diffdia)):

        if str(pertneg[diagnum]) == "0" or str(pertneg[diagnum]) == "nan":
            negs = []

        else:
            negs = txtfix(pertneg[diagnum])
        
        seve = severity[diagnum]
        prob = probdia[diagnum]
        natu = nature[diagnum]

        diagnoses.append(Diagnosis(diffdia[diagnum], negs, seve, prob, natu, [], majcomp, age, sex, final))

    othsignmapped = []

    for symptomnum in range(len(othsign)):
        if str(othsign[symptomnum]) != "nan":
            othsignmapped.append([txtfix(othsign[symptomnum])[0], symprob[symptomnum]]) #IMPORTANT!!! MIGHT HAVE TO BE SYMPTONUM + 1 IN ORDER TO ACCOUNT FOR EXTRA VALUE AT START OF COLUMN!!!


    for diag in diagnoses:
        diag.othersignsandsymptoms = othsignmapped

    dictdf = {}
    for diag in diagnoses:
        dictdf[diag.differentialdiagnosis] = [["Final Diagnosis", diag.finaldiagnosis], ["Major Complaint", diag.majorcomplaint], ["Probability of Diagnosis", diag.probabilityofdiagnosis], ["Severity", diag.severityofdiagnosis], ["Nature", diag.natureofdiagnosis]]
        pertinentnegativesfinal = []
        for negative in diag.pertinentnegatives:
            pertinentnegativesfinal.append([negative, .15])
        otherfinal = []
        for other in diag.othersignsandsymptoms:
            otherfinal.append(other)
        
        dictdf[diag.differentialdiagnosis] = dictdf[diag.differentialdiagnosis] + pertinentnegativesfinal + otherfinal

    # Write to Output

    new_df = pd.read_csv("diagnosisoutput.csv")

    row = {
        'Differential Diagnosis': "",
        'Severity': "",
        'Nature' : "",
        'Signs and Symptoms' : "", 
        'Category' : "", 
        'Weightage Base' : "", 
        'Rule Weightage' : "", 
        'Major Complaint' : "", 
        'Source' : "", 
        'Probability of Diagnosis' : "", 
        'Symptoms and Signs' : "",
    }

    for diag in diagnoses:
        row = {
            'Differential Diagnosis': diag.differentialdiagnosis,
            'Severity': diag.severityofdiagnosis,
            'Nature' : diag.natureofdiagnosis,
            'Signs and Symptoms' : "", 
            'Category' : "", 
            'Weightage Base' : "", 
            'Rule Weightage' : "", 
            'Major Complaint' : diag.majorcomplaint, 
            'Source' : diag.finaldiagnosis, 
            'Probability of Diagnosis' : diag.probabilityofdiagnosis, 
            'Symptoms and Signs' : "",
        }
        new_df = new_df.append(row, ignore_index = True)

        for symptom in diag.othersignsandsymptoms:
            row = {
                'Differential Diagnosis': "",
                'Severity': "",
                'Nature' : "",
                'Signs and Symptoms' : symptom[0], 
                'Category' : "", 
                'Weightage Base' : symptom[1], 
                'Rule Weightage' : symptom[1]*diag.probabilityofdiagnosis*1000, 
                'Major Complaint' : "", 
                'Source' : "", 
                'Probability of Diagnosis' : "", 
                'Symptoms and Signs' : "",
            }

            new_df = new_df.append(row, ignore_index = True)

        for symptom in diag.pertinentnegatives:
            row = {
                'Differential Diagnosis': "",
                'Severity': "",
                'Nature' : "",
                'Signs and Symptoms' : symptom, 
                'Category' : "", 
                'Weightage Base' : .15, 
                'Rule Weightage' : .15*diag.probabilityofdiagnosis*1000, 
                'Major Complaint' : "", 
                'Source' : "", 
                'Probability of Diagnosis' : "", 
                'Symptoms and Signs' : "",
            }

            new_df = new_df.append(row, ignore_index = True)


    #print(new_df)
    new_df.to_csv('diagnosisoutput.csv', index=False)
    print(f"Completed Sheet {sheet+1}")

#for i in range(13):
#    main(i)

for i in range(1):
    main(1)