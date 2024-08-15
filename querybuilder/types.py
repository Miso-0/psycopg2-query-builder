from typing import Optional, List
from querybuilder import QueryErrors


class Table:
    schema: str
    name: str

    def __init__(self, name: str, schema: Optional[str] = "public"):
        self.name = name
        self.schema = schema

    def __str__(self):
        return f"{self.schema}.{self.name}"

    def __eq__(self, other):
        if isinstance(other, Table):
            return self.name == other.name and self.schema == other.schema
        return False


class Column:
    name: str
    table: Optional[str]
    alies: Optional[str]

    def __init__(self, name: str, alies: Optional[str], table: Optional[str] = None):
        self.name = name
        self.table = table
        self.alies = alies

    def __str__(self):
        if self.table:
            return f"{self.table}.{self.name}"
        return self.name

    def alies_str(self):
        if not self.alies:
            raise QueryErrors("the alies str should only be called when an alies name of a column is called")
        if self.table:
            return f"{self.table}.{self.name} as {self.alies}"
        return self.name

    def __eq__(self, other):
        if isinstance(other, Column):
            return self.name == other.name and self.table == other.table
        return False


class Function:
    name: str
    schema: str
    parameters: Optional[List[any]]

    def __init__(self, name: str, schema: Optional[str] = "public", parameters: Optional[List[any]] = None):
        self.name = name
        self.schema = schema
        self.parameters = parameters if parameters is not None else []

    def __str__(self):
        params = ", ".join(self.parameters) if self.parameters else ""
        return f"{self.schema}.{self.name}({params})"

    def __eq__(self, other):
        if isinstance(other, Function):
            return (
                    self.name == other.name
                    and self.schema == other.schema
                    and self.parameters == other.parameters
            )
        return False
