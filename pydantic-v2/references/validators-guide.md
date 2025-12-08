# Pydantic v2 Validators Guide

Complete reference for field and model validators.

## Validator Modes

### After Validators (Default)

Run after Pydantic's built-in validation. Receive validated, typed data.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    age: int

    @field_validator('age', mode='after')
    @classmethod
    def check_adult(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Must be 18 or older')
        return v
```

### Before Validators

Run before type coercion. Receive raw input data.

```python
from pydantic import BaseModel, field_validator
from typing import Any

class User(BaseModel):
    tags: list[str]

    @field_validator('tags', mode='before')
    @classmethod
    def split_tags(cls, v: Any) -> Any:
        if isinstance(v, str):
            return v.split(',')
        return v

# Works with both:
User(tags=['a', 'b'])       # list input
User(tags='a,b,c')          # string input
```

### Plain Validators

Completely replace Pydantic's validation. No coercion happens.

```python
from pydantic import BaseModel
from pydantic.functional_validators import PlainValidator
from typing import Annotated, Any

def validate_positive(v: Any) -> int:
    val = int(v)
    if val <= 0:
        raise ValueError('Must be positive')
    return val

PositiveInt = Annotated[int, PlainValidator(validate_positive)]

class Item(BaseModel):
    quantity: PositiveInt
```

### Wrap Validators

Most flexible. Wrap around Pydantic's validation with access to handler.

```python
from pydantic import BaseModel, WrapValidator
from pydantic_core import PydanticUseDefault
from typing import Annotated, Any, Callable

def use_default_on_error(
    v: Any,
    handler: Callable[[Any], str]
) -> str:
    try:
        return handler(v)
    except Exception:
        raise PydanticUseDefault()

SafeStr = Annotated[str, WrapValidator(use_default_on_error)]

class Config(BaseModel):
    name: SafeStr = 'default'
```

## Annotated Validators (Reusable)

```python
from typing import Annotated
from pydantic import AfterValidator, BeforeValidator, BaseModel

# Reusable type definitions
def validate_email(v: str) -> str:
    if '@' not in v:
        raise ValueError('Invalid email format')
    return v.lower()

def strip_whitespace(v: Any) -> Any:
    return v.strip() if isinstance(v, str) else v

Email = Annotated[str, AfterValidator(validate_email)]
CleanStr = Annotated[str, BeforeValidator(strip_whitespace)]

class User(BaseModel):
    email: Email
    name: CleanStr
```

## Multiple Validators

Validators execute in order: before/wrap right-to-left, after left-to-right.

```python
from typing import Annotated
from pydantic import AfterValidator, BeforeValidator, BaseModel

def strip(v):
    return v.strip() if isinstance(v, str) else v

def lower(v: str) -> str:
    return v.lower()

def validate_length(v: str) -> str:
    if len(v) < 2:
        raise ValueError('Too short')
    return v

# Execution order: strip -> coerce to str -> lower -> validate_length
CleanName = Annotated[str,
    BeforeValidator(strip),
    AfterValidator(lower),
    AfterValidator(validate_length)
]
```

## Field Validator Decorator

```python
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    name: str
    price: float
    quantity: int

    # Single field
    @field_validator('name')
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    # Multiple fields
    @field_validator('price', 'quantity')
    @classmethod
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Must be positive')
        return v

    # All fields
    @field_validator('*')
    @classmethod
    def not_none(cls, v):
        if v is None:
            raise ValueError('Cannot be None')
        return v
```

## Model Validators

### After Mode

Access fully validated model instance.

```python
from pydantic import BaseModel, model_validator
from typing_extensions import Self

class Order(BaseModel):
    subtotal: float
    tax: float
    discount: float = 0

    @model_validator(mode='after')
    def validate_totals(self) -> Self:
        if self.discount > self.subtotal:
            raise ValueError('Discount cannot exceed subtotal')
        return self
```

### Before Mode

Access raw input data before field validation.

```python
from pydantic import BaseModel, model_validator
from typing import Any

class User(BaseModel):
    first_name: str
    last_name: str

    @model_validator(mode='before')
    @classmethod
    def split_name(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'full_name' in data:
            full = data.pop('full_name')
            parts = full.split(' ', 1)
            data['first_name'] = parts[0]
            data['last_name'] = parts[1] if len(parts) > 1 else ''
        return data

# Works with:
User(first_name='John', last_name='Doe')
User.model_validate({'full_name': 'John Doe'})
```

### Wrap Mode

Control flow around validation.

```python
from pydantic import BaseModel, model_validator
from typing import Any
from typing_extensions import Self

class Transaction(BaseModel):
    amount: float
    currency: str

    @model_validator(mode='wrap')
    @classmethod
    def log_validation(cls, data: Any, handler) -> Self:
        print(f'Validating: {data}')
        try:
            result = handler(data)
            print(f'Success: {result}')
            return result
        except Exception as e:
            print(f'Failed: {e}')
            raise
```

## Validation Info

Access context during validation.

```python
from pydantic import BaseModel, ValidationInfo, field_validator

class User(BaseModel):
    password: str
    password_confirm: str

    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        # Access already validated fields
        password = info.data.get('password')
        if password and v != password:
            raise ValueError('Passwords do not match')
        return v
```

### Using Context

Pass custom context during validation.

```python
from pydantic import BaseModel, ValidationInfo, field_validator

class Document(BaseModel):
    content: str

    @field_validator('content')
    @classmethod
    def filter_content(cls, v: str, info: ValidationInfo) -> str:
        if info.context:
            banned = info.context.get('banned_words', [])
            for word in banned:
                v = v.replace(word, '***')
        return v

# Usage
doc = Document.model_validate(
    {'content': 'Hello world'},
    context={'banned_words': ['world']}
)
print(doc.content)  # 'Hello ***'
```

## Custom Error Types

```python
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

class User(BaseModel):
    age: int

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise PydanticCustomError(
                'negative_age',
                'Age cannot be negative: {age}',
                {'age': v}
            )
        if v > 150:
            raise PydanticCustomError(
                'unrealistic_age',
                'Age {age} seems unrealistic',
                {'age': v}
            )
        return v
```

## Validation Utilities

### SkipValidation

Skip validation for specific fields.

```python
from pydantic import BaseModel
from pydantic.functional_validators import SkipValidation
from typing import Annotated

class Model(BaseModel):
    # Trust this value, no validation
    trusted_data: Annotated[dict, SkipValidation]
```

### InstanceOf

Validate that value is instance of type without coercion.

```python
from pydantic import BaseModel
from pydantic.functional_validators import InstanceOf
from typing import Annotated
from pathlib import Path

class Config(BaseModel):
    path: Annotated[Path, InstanceOf[Path]]

# Must pass actual Path object, not string
Config(path=Path('/home'))  # OK
Config(path='/home')        # ValidationError
```

## Best Practices

1. **Use `mode='after'` by default** - Type-safe, easier to implement
2. **Use `mode='before'` for data transformation** - Normalize input formats
3. **Use Annotated validators for reusability** - Define once, use everywhere
4. **Raise ValueError for validation failures** - Pydantic converts to ValidationError
5. **Access validated data via `info.data`** - For cross-field validation
6. **Always return a value** - Validators must return the (possibly modified) value
