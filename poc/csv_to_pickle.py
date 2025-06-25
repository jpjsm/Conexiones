from typing import Any, LiteralString

from pathlib import Path
import csv
import pandas as pd
import pickle

import streamlit as st
import graphviz


def FullName(person: Any) -> LiteralString:
    elements = []
    if person["FirstName"].strip():
        elements.append(person["FirstName"].strip().title())

    if person["MiddleNames"]:
        if isinstance(person["MiddleNames"], list):
            for mname in person["MiddleNames"]:
                if mname.strip():
                    elements.append(mname.strip().title())
        else:
            if str(person["MiddleNames"]).strip():
                elements.append(str(person["MiddleNames"]).strip().title())

    if person["LastName_Father"].strip():
        elements.append(person["LastName_Father"].strip().title())

    if person["LastName_MotherMaiden"].strip():
        elements.append(person["LastName_MotherMaiden"].strip().title())

    fn = " ".join(elements)
    return fn


with open(Path("data/FamiliaGenealogias.csv"), "r", encoding="utf-8") as csv_input:
    reader = csv.DictReader(csv_input)
    people_rows = list(reader)

people = {}
duplicate_ids = []
for person in people_rows:
    person_id = person["ID"].strip().upper()
    person["ID"] = person_id
    if person_id in people:
        duplicate_ids.append(person)
        continue
    people[person_id] = person

with open(Path("data/people.pkl"), "bw") as db:
    pickle.dump(people, db)

if duplicate_ids:
    for dup in duplicate_ids:
        print(dup)
        print(f"\n{" -°-"*40}\n")

with open(Path("data/people_dup_ids.pkl"), "bw") as db:
    pickle.dump(duplicate_ids, db)
