from typing import Any, LiteralString

from pathlib import Path
import csv
import pandas as pd
import pickle

import streamlit as st
import graphviz

from utils import FullName


with open(Path("data/people.pkl"), "br") as db:
    people = pickle.load(db)

graph = graphviz.Digraph()
graph.graph_attr["rankdir"] = "LR"

for person_id, person in people.items():
    graph.node(person["ID"], label=FullName(person))
    if person["Father_ID"]:
        graph.edge(person["Father_ID"], person["ID"])

    if person["Mother_ID"]:
        graph.edge(person["Mother_ID"], person["ID"])

st.graphviz_chart(graph)
# graph.view()
