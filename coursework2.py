import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

LOCAL_AUTHORITY = "Cambridgeshire"
TYPE_SCHOOL = "State-funded secondary"
YEAR = 202324

def getMainRatesData(): return pd.read_csv('data/1_absence_2term_main_rates2.csv')
def loadSchoolData(): return pd.read_csv('data/1_absence_2term_school.csv')

def filteredData() -> dict:
    data = getMainRatesData()
    filteredDataCambridgeshire = data[(data["la_name"] == LOCAL_AUTHORITY) & (data["education_phase"] == TYPE_SCHOOL) & (data["time_period"] == YEAR)]
    filteredDataSuffolk = data[(data["la_name"] == "Suffolk") & (data["education_phase"] == TYPE_SCHOOL) & (data["time_period"] == YEAR)]
    filteredDataAll = pd.DataFrame([data.iloc[2]]) 
    return {
        "Cambridgeshire": filteredDataCambridgeshire,
        "Suffolk": filteredDataSuffolk,
        "allSchools": filteredDataAll,
    }
    
def calculateAbsenceTypeDifferences() -> dict:
    data = filteredData()
    absenceRates = {
        "Illness": "sess_auth_illness_rate",
        "Appointments": "sess_auth_appointments_rate",
        "Religious": "sess_auth_religious_rate",
        "Study": "sess_auth_study_rate",
        "Traveler": "sess_auth_traveller_rate",
        "Holiday": "sess_auth_holiday_rate",
        "Other": "sess_auth_other_rate",
    }

    def getRates(regionData, absenceRates):
        return {key: regionData[column].iloc[0] for key, column in absenceRates.items()}

    cambsRates = getRates(data["Cambridgeshire"], absenceRates)
    suffolkRates = getRates(data["Suffolk"], absenceRates)
    allRates = getRates(data["allSchools"], absenceRates)

    differences = {
        key: {
            "vsSuffolk": cambsRates[key] - suffolkRates[key],
            "vsAllSchools": cambsRates[key] - allRates[key],
        }
        for key in absenceRates.keys()
    }

    return differences

    
def plotAbsenceTypeDifferences():
    differences = calculateAbsenceTypeDifferences()

    types = list(differences.keys())
    vsSuffolk = [differences[typ]["vsSuffolk"] for typ in types]
    vsAllSchools = [differences[typ]["vsAllSchools"] for typ in types]

    x = np.arange(len(types))
    barWidth = 0.4
        
    plt.axhline(0, color='gray', linewidth=1, linestyle='--')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.bar(x - barWidth / 2, vsSuffolk, barWidth, label='Cambridgeshire vs Suffolk')
    plt.bar(x + barWidth / 2, vsAllSchools, barWidth, label='Cambridgeshire vs All Schools')

    plt.xlabel('Types of Absence')
    plt.ylabel('Difference in Percentage Points')
    plt.title('Percentage Differences by Authorised Absence Types')
    plt.xticks(x, types)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.show() 

def plotScatterWithAverages():
    data = loadSchoolData()

    cambsSchools = data[
        (data["la_name"] == LOCAL_AUTHORITY) &
        (data["education_phase"] == TYPE_SCHOOL) &
        (data["time_period"] == YEAR)
    ]
    suffolkData = data[
        (data["la_name"] == "Suffolk") &
        (data["education_phase"] == TYPE_SCHOOL) &
        (data["time_period"] == YEAR)
    ]
    allSchoolsData = data[
        (data["education_phase"] == TYPE_SCHOOL) &
        (data["time_period"] == YEAR)
    ]

    avgAuthSuffolk = suffolkData["sess_authorised"].mean()
    avgAuthAllSchools = allSchoolsData["sess_authorised"].mean()

    plt.scatter(
        range(len(cambsSchools)), 
        cambsSchools["sess_authorised"],
        label='Cambridgeshire Schools',
        color='blue',
        marker='x',
        alpha=0.7
    )

    plt.axhline(avgAuthSuffolk, color='orange', linestyle='--', label='Suffolk Authorised Average')
    plt.axhline(avgAuthAllSchools, color='green', linestyle='--', label='All Schools Authorised Average')

    plt.xlabel('School Index')
    plt.ylabel('Authorised Absences')
    plt.title('Cambridgeshire Schools Authorised Absences againt Suffolk and All Schools Averages')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

def getAuthAbs(data) -> int:
    return data["sess_authorised"]

def getUnauthAbs(data) -> int:
    return data["sess_unauthorised"]

def getNumSchools(data) -> int:
    return data["num_schools"]

plotScatterWithAverages()
plotAbsenceTypeDifferences()