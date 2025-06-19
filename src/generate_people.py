import csv
from pathlib import Path
import pickle
import json
from typing import Dict, List

from person import Person

with open("data/FamiliaGenealogias.csv", "r", newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    people_rows: List[Dict[str, str]] = list(csv_reader)


people: List[Person] = []
duplicate_ids = []
for person_dict in people_rows:
    for key in person_dict:
        if person_dict[key] == "":
            person_dict[key] = None
        else:
            try:
                person_dict[key] = person_dict[key].strip() if person_dict[key] else ""
            except AttributeError as ae:
                print(person_dict)
                print(f"Attribute error: Key: {key} -> value: {person_dict[key]}")
                print(ae)
                raise

            if person_dict[key] == "":
                person_dict[key] = None
        if key == "ExSpouse_ID" and person_dict["ExSpouse_ID"]:
            ex_spouse_id = person_dict["ExSpouse_ID"]
            exes = str(person_dict["ExSpouse_ID"]).split()
            person_dict["ExSpouse_ID"] = exes

    person = Person(**person_dict)
    person.ID = person.ID.upper()
    if person.ID in people:
        duplicate_ids.append(person)
        continue

    people.append(person)
    print(person.CsvRow())

with open(Path("data/people.pkl"), "bw") as db:
    pickle.dump(people, db)

with open(Path("data/people.json"), "w", encoding="utf-8") as outfile:
    json.dump(
        [someone.JsonSerializer() for someone in people],
        outfile,
        indent=4,
        ensure_ascii=False,
    )

with open(Path("data/people.csv"), "w", encoding="utf-8", newline="") as outcsv:
    csvwriter = csv.writer(outcsv, dialect=csv.unix_dialect)
    csvwriter.writerow(Person.CsvHeaders())
    csvwriter.writerows([someone.CsvRow() for someone in people])


if duplicate_ids:
    for dup in duplicate_ids:
        print(dup)
        print(f"\n{" -°-"*40}\n")

    with open(Path("data/people_dup_ids.pkl"), "bw") as db:
        pickle.dump(duplicate_ids, db)
