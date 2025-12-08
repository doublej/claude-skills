# Pydantic v2 Types Guide

Complete reference for built-in, constrained, and custom types.

## Built-in Types

Pydantic supports all standard Python types:

```python
from pydantic import BaseModel
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import UUID
from typing import Any

class Model(BaseModel):
    # Primitives
    integer: int
    floating: float
    text: str
    flag: bool
    raw: bytes

    # Date/Time
    timestamp: datetime
    day: date
    clock: time
    duration: timedelta

    # Other stdlib
    amount: Decimal
    file_path: Path
    identifier: UUID
    anything: Any
```

## Constrained Types

### Using Field()

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    # Numeric constraints
    price: float = Field(gt=0, le=10000)
    quantity: int = Field(ge=0, lt=1000)
    discount: float = Field(ge=0, le=1, multiple_of=0.05)

    # String constraints
    name: str = Field(min_length=1, max_length=100)
    sku: str = Field(pattern=r'^[A-Z]{2}-\d{4}$')

    # Decimal constraints
    tax_rate: Decimal = Field(max_digits=5, decimal_places=4)
```

### Using Annotated (Reusable)

```python
from typing import Annotated
from pydantic import BaseModel, Field

# Define reusable types
PositiveInt = Annotated[int, Field(gt=0)]
PositiveFloat = Annotated[float, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]
Percentage = Annotated[float, Field(ge=0, le=100)]
Email = Annotated[str, Field(pattern=r'^[\w.-]+@[\w.-]+\.\w+$')]

class User(BaseModel):
    id: PositiveInt
    name: NonEmptyStr
    email: Email
    score: Percentage
```

### Strict Variants

```python
from pydantic import StrictInt, StrictFloat, StrictStr, StrictBool, StrictBytes

class StrictModel(BaseModel):
    count: StrictInt      # No coercion from "123"
    value: StrictFloat    # No coercion from 123
    name: StrictStr       # No coercion from 123
    flag: StrictBool      # No coercion from 1/0
    data: StrictBytes     # No coercion from str
```

## Collection Types

```python
from pydantic import BaseModel
from typing import Literal

class Model(BaseModel):
    # Lists
    items: list[str]
    numbers: list[int] = []

    # Sets
    tags: set[str]
    unique_ids: frozenset[int]

    # Tuples
    point: tuple[float, float]           # Exactly 2 floats
    flexible: tuple[int, ...]            # Variable length
    mixed: tuple[str, int, bool]         # Fixed types

    # Dicts
    metadata: dict[str, str]
    config: dict[str, int | str | bool]

    # Literals
    status: Literal['active', 'inactive', 'pending']
```

## Union Types

```python
from pydantic import BaseModel, Field
from typing import Literal, Union

# Simple union
class Model(BaseModel):
    value: int | str | None

# Discriminated union (better performance)
class Cat(BaseModel):
    type: Literal['cat']
    meows: int

class Dog(BaseModel):
    type: Literal['dog']
    barks: float

class Pet(BaseModel):
    animal: Cat | Dog = Field(discriminator='type')

# Tagged union
Pet.model_validate({'animal': {'type': 'cat', 'meows': 5}})
```

## Optional Types

```python
from pydantic import BaseModel

class Model(BaseModel):
    # Required field
    required: str

    # Optional with None default
    optional: str | None = None

    # Optional with value default
    with_default: str = 'default'

    # Required but can be None (unusual)
    required_nullable: str | None
```

## Special Pydantic Types

```python
from pydantic import (
    BaseModel,
    SecretStr,
    SecretBytes,
    EmailStr,
    HttpUrl,
    AnyUrl,
    FilePath,
    DirectoryPath,
    NewPath,
    Json,
    ImportString,
    PositiveInt,
    NegativeInt,
    NonNegativeInt,
    NonPositiveInt,
    PositiveFloat,
    NegativeFloat,
    NonNegativeFloat,
    NonPositiveFloat,
    conint,
    confloat,
    constr,
    conbytes,
    conlist,
    conset,
)

class SecureModel(BaseModel):
    # Secrets (masked in repr/str)
    password: SecretStr
    api_key: SecretBytes

    # Network
    email: EmailStr              # Requires email-validator package
    website: HttpUrl
    any_url: AnyUrl

    # Filesystem
    config_file: FilePath        # Must exist
    data_dir: DirectoryPath      # Must exist and be dir
    output_file: NewPath         # Must NOT exist

    # JSON
    json_data: Json[dict]        # Parse JSON string to dict

    # Import
    handler: ImportString        # 'module.submodule.function'
```

## Constrained Type Functions

```python
from pydantic import BaseModel, conint, confloat, constr, conlist

class Constrained(BaseModel):
    # Integer with constraints
    age: conint(ge=0, le=150)

    # Float with constraints
    score: confloat(ge=0, le=100, multiple_of=0.5)

    # String with constraints
    code: constr(min_length=4, max_length=10, pattern=r'^[A-Z]+$')

    # List with constraints
    tags: conlist(str, min_length=1, max_length=10)
```

## Custom Types with Annotated

### Using AfterValidator

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator

def validate_even(v: int) -> int:
    if v % 2 != 0:
        raise ValueError('Must be even')
    return v

EvenInt = Annotated[int, AfterValidator(validate_even)]

class Model(BaseModel):
    value: EvenInt
```

### Using BeforeValidator

```python
from typing import Annotated, Any
from pydantic import BaseModel, BeforeValidator

def parse_list(v: Any) -> Any:
    if isinstance(v, str):
        return v.split(',')
    return v

CommaSeparated = Annotated[list[str], BeforeValidator(parse_list)]

class Model(BaseModel):
    items: CommaSeparated

Model(items='a,b,c')  # -> items=['a', 'b', 'c']
```

## Custom Types with __get_pydantic_core_schema__

For complete control over validation:

```python
from typing import Any
from pydantic import BaseModel, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

class Color:
    def __init__(self, value: str):
        self.value = value.upper()

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(pattern=r'^#[0-9A-Fa-f]{6}$'),
        )

class Design(BaseModel):
    background: Color
```

## Generic Types

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    success: bool = True
    message: str = ''

class Paginated(BaseModel, Generic[T]):
    items: list[T]
    page: int = 1
    per_page: int = 20
    total: int

# Usage
IntResponse = Response[int]
UserList = Paginated[User]

response = Response[int](data=42)
users = Paginated[User](items=[...], total=100)
```

## TypedDict

```python
from typing import TypedDict
from pydantic import TypeAdapter

class UserDict(TypedDict):
    name: str
    age: int

class UserDictPartial(TypedDict, total=False):
    name: str
    age: int

adapter = TypeAdapter(UserDict)
user = adapter.validate_python({'name': 'Alice', 'age': 30})
```

## Recursive Types

```python
from __future__ import annotations
from pydantic import BaseModel

class TreeNode(BaseModel):
    value: str
    children: list[TreeNode] = []

# Usage
tree = TreeNode(
    value='root',
    children=[
        TreeNode(value='child1'),
        TreeNode(value='child2', children=[TreeNode(value='grandchild')])
    ]
)
```

## Enum Types

```python
from enum import Enum, IntEnum
from pydantic import BaseModel, ConfigDict

class Status(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    PENDING = 'pending'

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Task(BaseModel):
    status: Status
    priority: Priority

# Keep enum values instead of members
class TaskValues(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    status: Status
    priority: Priority
```

## Type Coercion Reference

| Input Type | Target Type | Coercion |
|------------|-------------|----------|
| `"123"` | `int` | `123` |
| `123` | `str` | `"123"` |
| `1.5` | `int` | `1` (truncates) |
| `"true"` | `bool` | `True` |
| `1` / `0` | `bool` | `True` / `False` |
| `"2024-01-01"` | `date` | `date(2024, 1, 1)` |
| `dict` | `Model` | Nested validation |
| `list` | `set` | Set conversion |
| `tuple` | `list` | List conversion |

Use `strict=True` to disable coercion.
