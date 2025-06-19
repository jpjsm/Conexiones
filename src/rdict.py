from typing import Any, LiteralString, Union, List, Optional, Tuple, Dict

from pydantic import BaseModel, field_validator


class RecursiveDict(BaseModel):
    d: dict[str, Union[str, "RecursiveDict"]]
