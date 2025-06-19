from typing import Any, LiteralString


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
