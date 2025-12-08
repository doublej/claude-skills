---
name: pydantic-v2
description: Build robust data validation with Pydantic v2. Use when creating models, validators, serialization logic, API schemas, or migrating from v1. Covers BaseModel, Field, validators, TypeAdapter, strict mode, and JSON Schema generation.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
metadata:
  category: "python-validation"
  version: "1.0"
  pydantic_version: "2.12+"
---

# Pydantic v2

Data validation using Python type hints. Fast, extensible, IDE-friendly.

## When to Use This Skill

- Creating data models with validation
- Building API request/response schemas
- Validating configuration or user input
- Generating JSON Schema for documentation
- Migrating from Pydantic v1 to v2

## Installation

```bash
uv add pydantic
# or
pip install pydantic
```

## Quick Start

```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=50)
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()

# Validation happens automatically
user = User(id='123', name='Alice', email='ALICE@example.com')
print(user.id)     # 123 (coerced to int)
print(user.email)  # alice@example.com (lowercased)
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **BaseModel** | Base class for all Pydantic models |
| **Field()** | Configure field constraints, defaults, aliases |
| **Validators** | Custom validation via decorators |
| **ConfigDict** | Model-level configuration |
| **TypeAdapter** | Validate non-model types |

## BaseModel Essential Methods

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

# Creation & Validation
item = Item(name='Widget', price=9.99)
item = Item.model_validate({'name': 'Widget', 'price': 9.99})
item = Item.model_validate_json('{"name": "Widget", "price": 9.99}')

# Serialization
data = item.model_dump()                    # -> dict
json_str = item.model_dump_json()           # -> JSON string
schema = Item.model_json_schema()           # -> JSON Schema dict

# Copying
new_item = item.model_copy(update={'price': 14.99})

# Without validation (use sparingly)
item = Item.model_construct(name='Widget', price=9.99)
```

## Field Configuration

```python
from pydantic import BaseModel, Field
from typing import Annotated

class Product(BaseModel):
    # Basic constraints
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description='Price in USD')
    quantity: int = Field(default=0, ge=0)

    # Aliases for JSON keys
    product_id: str = Field(alias='id')

    # Separate validation/serialization aliases
    internal_code: str = Field(
        validation_alias='code',
        serialization_alias='productCode'
    )

    # Exclude from serialization
    secret: str = Field(exclude=True)

    # Frozen (immutable)
    sku: str = Field(frozen=True)

# Reusable constrained types
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]
```

### Numeric Constraints

| Constraint | Description |
|------------|-------------|
| `gt` | Greater than |
| `ge` | Greater than or equal |
| `lt` | Less than |
| `le` | Less than or equal |
| `multiple_of` | Must be multiple of value |

### String Constraints

| Constraint | Description |
|------------|-------------|
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `pattern` | Regex pattern to match |

### Decimal Constraints

| Constraint | Description |
|------------|-------------|
| `max_digits` | Total max digits |
| `decimal_places` | Max decimal places |

## Validators

### Field Validators

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    username: str
    password: str

    # After validation (type-safe, most common)
    @field_validator('username', mode='after')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v

    # Before validation (raw input)
    @field_validator('password', mode='before')
    @classmethod
    def password_strip(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v

    # Validate multiple fields
    @field_validator('username', 'password', mode='after')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v:
            raise ValueError('Cannot be empty')
        return v
```

### Annotated Validators (Reusable)

```python
from typing import Annotated
from pydantic import BaseModel, AfterValidator, BeforeValidator

def to_lowercase(v: str) -> str:
    return v.lower()

def strip_whitespace(v):
    return v.strip() if isinstance(v, str) else v

LowerStr = Annotated[str, AfterValidator(to_lowercase)]
CleanStr = Annotated[str, BeforeValidator(strip_whitespace)]

class User(BaseModel):
    email: LowerStr
    name: CleanStr
```

### Model Validators

```python
from pydantic import BaseModel, model_validator
from typing import Any
from typing_extensions import Self

class Order(BaseModel):
    items: list[str]
    total: float
    discount: float = 0

    # After: access validated instance
    @model_validator(mode='after')
    def validate_discount(self) -> Self:
        if self.discount > self.total:
            raise ValueError('Discount exceeds total')
        return self

    # Before: access raw input data
    @model_validator(mode='before')
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'item' in data:
            data['items'] = [data.pop('item')]
        return data
```

### Wrap Validators

```python
from pydantic import BaseModel, WrapValidator, ValidationError
from pydantic_core import ValidationInfo
from typing import Any, Callable

def truncate_string(
    v: Any,
    handler: Callable[[Any], str],
    info: ValidationInfo
) -> str:
    try:
        return handler(v)
    except ValidationError:
        if isinstance(v, str) and len(v) > 100:
            return handler(v[:100])
        raise

from typing import Annotated
TruncatedStr = Annotated[str, WrapValidator(truncate_string)]
```

## Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(
        strict=True,               # No type coercion
        frozen=True,               # Immutable instances
        extra='forbid',            # Error on extra fields
        validate_assignment=True,  # Validate on attribute set
        str_strip_whitespace=True, # Strip string fields
        str_min_length=1,          # Min length for all strings
        populate_by_name=True,     # Allow field name or alias
        use_enum_values=True,      # Store enum values, not members
    )

    name: str
    age: int
```

### Extra Fields Handling

```python
class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')  # Raises error

class Flexible(BaseModel):
    model_config = ConfigDict(extra='allow')   # Stores in __pydantic_extra__

class Default(BaseModel):
    model_config = ConfigDict(extra='ignore')  # Silently discards (default)
```

## Strict Mode

Disable automatic type coercion:

```python
from pydantic import BaseModel, ConfigDict, Field

# Model-level strict mode
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    value: int  # Must be int, not "123"

# Field-level strict mode
class MixedModel(BaseModel):
    strict_value: int = Field(strict=True)
    flexible_value: int  # Allows coercion

# Validation-time strict mode
data = {"value": "123"}
Model.model_validate(data, strict=True)  # Raises ValidationError
```

## Nested Models

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str = 'USA'

class Company(BaseModel):
    name: str
    address: Address

class User(BaseModel):
    name: str
    company: Company
    addresses: list[Address] = []

# Nested validation
user = User.model_validate({
    'name': 'Alice',
    'company': {
        'name': 'Acme',
        'address': {'street': '123 Main', 'city': 'NYC'}
    }
})
```

## Generic Models

```python
from pydantic import BaseModel
from typing import Generic, TypeVar

T = TypeVar('T')

class Response(BaseModel, Generic[T]):
    data: T
    success: bool = True

class Paginated(BaseModel, Generic[T]):
    items: list[T]
    page: int
    total: int

# Usage
UserResponse = Response[User]
UserList = Paginated[User]
```

## TypeAdapter

Validate types without creating a model:

```python
from pydantic import TypeAdapter

# Simple types
int_adapter = TypeAdapter(int)
result = int_adapter.validate_python('42')  # -> 42

# Collections
list_adapter = TypeAdapter(list[int])
result = list_adapter.validate_python(['1', '2', '3'])  # -> [1, 2, 3]

# TypedDict
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    age: int

adapter = TypeAdapter(list[UserDict])
users = adapter.validate_python([{'name': 'Alice', 'age': '30'}])

# Serialization (returns bytes, not str!)
json_bytes = adapter.dump_json(users)

# JSON Schema
schema = adapter.json_schema()
```

## Serialization

```python
from pydantic import BaseModel, field_serializer, model_serializer
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime

    # Field serializer
    @field_serializer('timestamp')
    def serialize_timestamp(self, v: datetime) -> str:
        return v.isoformat()

# Serialization options
event = Event(name='Launch', timestamp=datetime.now())

event.model_dump()                          # Python dict
event.model_dump(mode='json')               # JSON-compatible dict
event.model_dump_json()                     # JSON string
event.model_dump(exclude={'timestamp'})     # Exclude fields
event.model_dump(include={'name'})          # Include only
event.model_dump(by_alias=True)             # Use aliases
event.model_dump(exclude_unset=True)        # Only explicitly set
event.model_dump(exclude_none=True)         # Skip None values
```

## Computed Fields

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

rect = Rectangle(width=10, height=5)
print(rect.area)              # 50.0
print(rect.model_dump())      # {'width': 10, 'height': 5, 'area': 50.0}
```

## JSON Schema Generation

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(description='Full name', examples=['John Doe'])
    age: int = Field(ge=0, le=150, description='Age in years')

# Generate schema
schema = User.model_json_schema()

# Modes
validation_schema = User.model_json_schema(mode='validation')
serialization_schema = User.model_json_schema(mode='serialization')
```

## Common Patterns

### Optional vs Required

```python
from pydantic import BaseModel

class User(BaseModel):
    required: str                    # Must be provided
    optional: str | None = None      # Can be None
    with_default: str = 'default'    # Has default value
```

### Union Types

```python
from pydantic import BaseModel, Field
from typing import Literal

class Cat(BaseModel):
    pet_type: Literal['cat']
    meows: int

class Dog(BaseModel):
    pet_type: Literal['dog']
    barks: float

class Pet(BaseModel):
    # Discriminated union for better performance
    pet: Cat | Dog = Field(discriminator='pet_type')
```

### Private Attributes

```python
from pydantic import BaseModel, PrivateAttr

class User(BaseModel):
    name: str
    _internal: str = PrivateAttr(default='secret')

    def __init__(self, **data):
        super().__init__(**data)
        self._internal = 'initialized'
```

### Custom Root Types

```python
from pydantic import RootModel

class Tags(RootModel[list[str]]):
    pass

tags = Tags.model_validate(['python', 'pydantic'])
print(tags.root)  # ['python', 'pydantic']
```

## Error Handling

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

try:
    User(name=123, age='not-a-number')
except ValidationError as e:
    print(e.error_count())        # Number of errors
    print(e.errors())             # List of error dicts
    print(e.json())               # JSON representation

    for error in e.errors():
        print(f"{error['loc']}: {error['msg']}")
```

## V1 to V2 Migration Highlights

| V1 | V2 |
|----|-----|
| `class Config:` | `model_config = ConfigDict()` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `.parse_obj()` | `.model_validate()` |
| `.parse_raw()` | `.model_validate_json()` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `schema()` | `model_json_schema()` |
| `__fields__` | `model_fields` |

## Reference Files

See `references/` for detailed guides:

- **[validators-guide.md](references/validators-guide.md)** - Complete validator patterns
- **[serialization-guide.md](references/serialization-guide.md)** - Serialization customization
- **[types-guide.md](references/types-guide.md)** - Custom and constrained types

## External Resources

- [Official Documentation](https://docs.pydantic.dev/latest/)
- [Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [GitHub Repository](https://github.com/pydantic/pydantic)
