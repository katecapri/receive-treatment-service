import pandas as pd
from src.treatment.repository import TreatmentRepository
import logging
logging.basicConfig(level=logging.INFO)


def save_new_treatment(treatment):
    TreatmentRepository().save_new_treatment(treatment)


def save_treatments_to_file():
    all_treatments = TreatmentRepository().get_all_treatments()
    first_names, last_names, patronymics, phones, treatments, creation_dates = [list() for _ in range(6)]
    rows = 0
    for row in all_treatments:
        treatment = row[0]
        last_names.append(treatment.last_name)
        first_names.append(treatment.first_name)
        patronymics.append(treatment.patronymic)
        phones.append(treatment.phone)
        treatments.append(treatment.treatment)
        creation_dates.append(treatment.creation_date)
        rows += 1

    df = pd.DataFrame({
        'Last_name': last_names,
        'First_name': first_names,
        'Patronymic': patronymics,
        'Phone': phones,
        'Treatments': treatments,
        'Date': creation_dates,
    })
    df.index += 1
    df.to_excel(f'/media/{rows}_treatments.xlsx')

