from pathlib import Path
import pickle
from typing import List, Set, Dict

import streamlit as st
import graphviz

from person import Person


spouses_edges = set()
exspouses_edges = set()
with open(Path("data/people.pkl"), "br") as db:
    people: List[Person] = pickle.load(db)

generation_groups: Dict[str, Set[str]] = {}

graph = graphviz.Digraph(format="pdf")
graph.graph_attr["rankdir"] = "LR"
## graph.graph_attr["layout"] = "neato"
for person in people:
    graph.node(person.ID, label=person.FullName())
    if person.Father_ID:
        graph.edge(person.Father_ID, person.ID)
    if person.Mother_ID:
        graph.edge(person.Mother_ID, person.ID)
    if person.Spouse_ID:
        if f"{person.ID}-{person.Spouse_ID}" not in spouses_edges:
            spouses_edges.add(f"{person.ID}-{person.Spouse_ID}")
            spouses_edges.add(f"{person.Spouse_ID}-{person.ID}")
            with graph.subgraph(
                name=f"spouses_{person.ID}-{person.Spouse_ID}",
            ) as sg:
                sg.attr(style="invis", rank="same")
                sg.node(person.ID)
                sg.node(person.Spouse_ID)
                sg.edge(person.Spouse_ID, person.ID, dir="none")

    if person.ExSpouse_ID:
        for ex in person.ExSpouse_ID:
            if f"{person.ID}-{ex}" not in exspouses_edges:
                exspouses_edges.add(f"{person.ID}-{ex}")
                exspouses_edges.add(f"{ex}-{person.ID}")
                with graph.subgraph(
                    name=f"exspouses_{person.ID}-{ex}",
                ) as sg:
                    sg.attr(style="invis", rank="same")
                    sg.node(person.ID)
                    sg.node(ex)
                    sg.edge(ex, person.ID, dir="none", style="dotted")

    if person.Generation not in generation_groups:
        generation_groups[person.Generation] = set()

    generation_groups[person.Generation].add(person.ID)

for gen_group in generation_groups:
    with graph.subgraph(name=f"gen_{gen_group}") as sg:
        sg.attr(style="invis", rank="same")
        for id in generation_groups[gen_group]:
            sg.node(id)

graph.render("./data/ÁrbolGenealógico")
st.graphviz_chart(graph)
