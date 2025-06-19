from datetime import datetime, date

from typing import Any, LiteralString, Union, List, Optional, Tuple, Dict

from pydantic import BaseModel, field_validator

from sex import Sex
from rdict import RecursiveDict


def try_parse_us_date(value: str) -> Tuple[bool, date | None]:
    try:
        _date = datetime.strptime(value, "%m/%d/%Y").date()
        return (True, _date)
    except ValueError:
        return (False, None)


def try_parse_iso_date(value: str) -> Tuple[bool, date | None]:
    try:
        _date = datetime.fromisoformat(
            value
        ).date()  ##.strptime(value, "%m/%d/%Y").date()
        return (True, _date)
    except ValueError:
        return (False, None)


class Person(BaseModel):
    ID: str
    FirstName: str
    MiddleNames: Optional[Union[str, List[str]]] = ""
    LastName_Father: str
    LastName_MotherMaiden: Optional[str] = ""
    PreferredName: Optional[str] = ""
    Nickname: Optional[str] = ""
    Birthday: Optional[date | None] = None
    Deceased: Optional[date | None] = None
    Birth_Country: Optional[str] = ""
    Birth_Province: Optional[str] = ""
    Birth_City: Optional[str] = ""
    Sex_at_birth: Optional[Sex | None] = None
    Father_ID: Optional[str] = ""
    Mother_ID: Optional[str] = ""
    Spouse_ID: Optional[str] = ""
    ExSpouse_ID: Optional[Union[str, List[str]]] = ""
    Generation: Optional[str] = ""

    @field_validator("Birthday", "Deceased", mode="before")
    def validate_date(cls, value):
        if value is None:
            return None

        isvalid, date_value = try_parse_iso_date(value)
        if isvalid:
            return date_value

        isvalid, date_value = try_parse_us_date(value)
        if isvalid:
            return date_value

        raise ValueError(f"Invalid date format for: {value}")

    def FullName(self) -> LiteralString:
        elements = []
        if self.FirstName:
            fname = self.FirstName.strip()
            if fname:
                elements.append(fname.title())

        if self.MiddleNames:
            if isinstance(self.MiddleNames, list):
                for mname in self.MiddleNames:
                    if mname:
                        _mname = mname.strip()
                        if _mname:
                            elements.append(_mname.title())
            else:
                mname = self.MiddleNames.strip()
                if mname:
                    elements.append(mname.title())

        if self.LastName_Father:
            lname_father = self.LastName_Father.strip()
            if lname_father:
                elements.append(lname_father.title())

        if self.LastName_MotherMaiden:
            lname_mother = self.LastName_MotherMaiden.strip()
            if lname_mother:
                elements.append(lname_mother.title())

        if self.Deceased:
            # ⚘ | &#x2698;
            elements.append("⚘")

        fn = " ".join(elements)
        return fn

    def JsonSerializer(self) -> Dict[str, str | Any]:
        result = {}
        result["ID"] = self.ID
        result["FirstName"] = self.FirstName
        result["MiddleNames"] = (
            " ".join(self.MiddleNames)
            if isinstance(self.MiddleNames, list)
            else self.MiddleNames
        )
        result["LastName_Father"] = self.LastName_Father
        result["LastName_MotherMaiden"] = self.LastName_MotherMaiden
        result["PreferredName"] = self.PreferredName
        result["Nickname"] = self.Nickname
        result["Birthday"] = (
            self.Birthday.isoformat() if isinstance(self.Birthday, date) else ""
        )
        result["Deceased"] = (
            self.Deceased.isoformat() if isinstance(self.Deceased, date) else ""
        )
        result["Birth_Country"] = self.Birth_Country
        result["Birth_Province"] = self.Birth_Province
        result["Birth_City"] = self.Birth_City
        result["FirstName"] = self.FirstName
        result["Sex_at_birth"] = (
            self.Sex_at_birth.value if isinstance(self.Sex_at_birth, Sex) else ""
        )
        result["Father_ID"] = self.Father_ID if self.Father_ID else ""
        result["Mother_ID"] = self.Mother_ID if self.Mother_ID else ""
        result["Spouse_ID"] = self.Spouse_ID if self.Spouse_ID else ""
        result["ExSpouse_ID"] = (
            " ".join(self.ExSpouse_ID)
            if isinstance(self.ExSpouse_ID, list)
            else self.ExSpouse_ID if self.ExSpouse_ID else ""
        )
        result["Generation"] = self.Generation if self.Generation else ""

        return result

    @classmethod
    def CsvHeaders(cls) -> List[str]:
        return [
            "ID",
            "FirstName",
            "MiddleNames",
            "LastName_Father",
            "LastName_MotherMaiden",
            "PreferredName",
            "Nickname",
            "Birthday",
            "Deceased",
            "Birth_Country",
            "Birth_Province",
            "Birth_City",
            "Sex_at_birth",
            "Father_ID",
            "Mother_ID",
            "Spouse_ID",
            "ExSpouse_ID",
            "Generation",
        ]

    def CsvRow(self) -> List[str]:
        row = []
        _dir = self.JsonSerializer()
        for key in Person.CsvHeaders():
            v = _dir[key]
            if v is None:
                v = ""
            row.append(v)

        return row
