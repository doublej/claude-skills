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

## When to Use

- Creating data models with validation
- Building API request/response schemas
- Validating configuration or user input
- Generating JSON Schema for documentation

## Installation

```bash
uv add pydantic
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

user = User(id='123', name='Alice', email='ALICE@example.com')
print(user.id)     # 123 (coerced to int)
print(user.email)  # alice@example.com
```

## BaseModel Methods

```python
# Creation
item = Item(name='Widget', price=9.99)
item = Item.model_validate({'name': 'Widget', 'price': 9.99})
item = Item.model_validate_json('{"name": "Widget", "price": 9.99}')

# Serialization
data = item.model_dump()           # dict
json_str = item.model_dump_json()  # JSON string
schema = Item.model_json_schema()  # JSON Schema

# Copying
new_item = item.model_copy(update={'price': 14.99})
```

## Field Configuration

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description='Price in USD')
    product_id: str = Field(alias='id')
    secret: str = Field(exclude=True)
```

| Numeric | String | Description |
|---------|--------|-------------|
| `gt`, `ge` | `min_length` | Greater than, min length |
| `lt`, `le` | `max_length` | Less than, max length |
| `multiple_of` | `pattern` | Multiple of, regex |

## Validators

```python
from pydantic import BaseModel, field_validator, model_validator

class User(BaseModel):
    username: str

    @field_validator('username', mode='after')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Must be alphanumeric')
        return v

class Order(BaseModel):
    total: float
    discount: float = 0

    @model_validator(mode='after')
    def validate_discount(self):
        if self.discount > self.total:
            raise ValueError('Discount exceeds total')
        return self
```

## Reusable Annotated Validators

```python
from typing import Annotated
from pydantic import AfterValidator

def to_lowercase(v: str) -> str:
    return v.lower()

LowerStr = Annotated[str, AfterValidator(to_lowercase)]
```

## Model Configuration

```python
from pydantic import BaseModel, ConfigDict

class StrictUser(BaseModel):
    model_config = ConfigDict(
        strict=True,               # No type coercion
        frozen=True,               # Immutable
        extra='forbid',            # Error on extra fields
        validate_assignment=True,  # Validate on set
    )
    name: str
```

## TypeAdapter

Validate types without a model:

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(list[int])
result = adapter.validate_python(['1', '2', '3'])  # [1, 2, 3]
```

## Error Handling

```python
from pydantic import ValidationError

try:
    User(name=123, age='not-a-number')
except ValidationError as e:
    print(e.errors())  # List of error dicts
```

## V1 to V2 Migration

| V1 | V2 |
|----|-----|
| `class Config:` | `model_config = ConfigDict()` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |

## Reference Files

- [validators-guide.md](references/validators-guide.md) - Complete validator patterns
- [serialization-guide.md](references/serialization-guide.md) - Serialization customization
- [types-guide.md](references/types-guide.md) - Custom and constrained types

## Documentation

- [Official Documentation](https://docs.pydantic.dev/latest/)
- [Migration Guide](https://docs.pydantic.dev/latest/migration/)
