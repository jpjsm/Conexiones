from typing import Any, LiteralString
from datetime import datetime, date
from pathlib import Path
import csv
import pandas as pd
import pickle

import streamlit as st

from utils import FullName

with open(Path("data/paises.csv"), 'r', encoding='utf-8') as csv_input:
    reader = csv.reader(csv_input)
    paises = [ p for row in list(reader) for p in row]

with open(Path("data/people.pkl"), 'br') as db:
    people = pickle.load(db)

lastnames_picker = {}
for id, person in people.items():
    if  person["LastName_1"] not in lastnames_picker:
        lastnames_picker[person["LastName_1"]] = []

    lastnames_picker[person["LastName_1"]].append((FullName(person), id))


nombres = st.text_input("Nombres","").strip().title().split()
apellido_paterno = st.text_input("Apellido paterno","").strip().title()
apellido_materno = st.text_input("Apellido materno","").strip().title()
nacimiento = st.date_input("Fecha nacimiento",None)
fallecimiento = st.date_input("Fecha fallecimiento",None)
pais_nacimiento = st.selectbox("Pais de nacimiento", paises)
ciudad_nacimiento = st.text_input("Ciudad de nacimiento", "").strip().title()
sexo = st.radio("Sexo (al nacer)", ["Masculino", "Femenino"])
father = st.selectbox("Padre", lastnames_picker.get(apellido_paterno))
mother = st.selectbox("Madre", lastnames_picker.get(apellido_materno))

new_person = {
    "FirstName": "" if len(nombres) == 0 else nombres[0],
    "Middle_names": "" if len(nombres) <2 else nombres[1] if len(nombres) == 2 else ' '.join(nombres[1:]),
    "LastName_1": apellido_paterno,
    "LastName_2": apellido_materno,
    "Birthday": "" if nacimiento is None else nacimiento.isoformat(),
    "Deceased": "" if fallecimiento is None else fallecimiento.isoformat(),
    "Birth_Country": pais_nacimiento,
    "Birth_City": ciudad_nacimiento,
    "Sex": sexo[0],
    "Father": "" if father is None else father[1],
    "Mother": "" if mother is None else mother[1],
}

print(new_person)