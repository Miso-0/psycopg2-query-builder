from typing import Optional, List, Any


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

    def __hash__(self):
        return hash((self.schema, self.name))


class Column:
    name: str
    table: Optional[Table]
    alies: Optional[str]

    def __init__(self, name: str, alies: Optional[str] = None, table: Optional[str] = None):
        self.name = name
        self.table = table
        self.alies = alies

    def __str__(self):
        if self.table:
            if self.alies is not None:
                return f"{self.table}.{self.name} as {self.alies}"
            else:
                return f"{self.table}.{self.name}"
        elif self.alies is not None:
            return f"{self.name} as {self.alies}"
        return self.name

    def alies_str(self):
        if not self.alies:
            raise ValueError("The alias_str should only be called when an alias name of a column is provided.")
        if self.table:
            return f"{self.table}.{self.name} as {self.alies}"
        return f"{self.name} as {self.alies}"

    def __eq__(self, other):
        if isinstance(other, Column):
            return (
                    self.name == other.name and
                    self.table == other.table and
                    self.alies == other.alies
            )
        return False

    def __hash__(self):
        return hash((self.name, self.table, self.alies))


class Function:
    name: str
    schema: str
    parameters: Optional[List[Any]]

    def __init__(self, name: str, schema: Optional[str] = "public", parameters: Optional[List[Any]] = None):
        self.name = name
        self.schema = schema
        self.parameters = parameters if parameters is not None else []

    def __str__(self):
        params = ", ".join(str(p) for p in self.parameters) if self.parameters else ""
        return f"{self.schema}.{self.name}({params})"

    def __eq__(self, other):
        if isinstance(other, Function):
            return (
                    self.name == other.name and
                    self.schema == other.schema and
                    self.parameters == other.parameters
            )
        return False

    def __hash__(self):
        return hash((self.name, self.schema, tuple(self.parameters)))
