# Pydantic v2 Serialization Guide

Complete reference for model serialization and custom serializers.

## Basic Serialization

```python
from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    name: str
    timestamp: datetime
    tags: list[str]

event = Event(name='Launch', timestamp=datetime.now(), tags=['release'])

# Dictionary output
data = event.model_dump()

# JSON string output
json_str = event.model_dump_json()
```

## Serialization Modes

### Python Mode (Default)

Preserves Python types.

```python
class Model(BaseModel):
    items: tuple[int, int]

m = Model(items=(1, 2))
m.model_dump()  # {'items': (1, 2)} - tuple preserved
```

### JSON Mode

Converts to JSON-compatible types.

```python
m.model_dump(mode='json')  # {'items': [1, 2]} - tuple becomes list
```

## Common Options

```python
class User(BaseModel):
    name: str
    email: str | None = None
    password: str
    internal_id: int

user = User(name='Alice', password='secret', internal_id=1)

# Exclude fields
user.model_dump(exclude={'password'})

# Include only specific fields
user.model_dump(include={'name', 'email'})

# Exclude unset fields
user.model_dump(exclude_unset=True)  # Omits 'email' if not provided

# Exclude None values
user.model_dump(exclude_none=True)

# Use aliases
user.model_dump(by_alias=True)

# Nested exclusion
class Order(BaseModel):
    user: User
    total: float

order = Order(user=user, total=100)
order.model_dump(exclude={'user': {'password', 'internal_id'}})
```

## Field-Level Serializers

### Plain Serializers

Completely replace default serialization.

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class Event(BaseModel):
    timestamp: datetime

    @field_serializer('timestamp', mode='plain')
    def serialize_timestamp(self, v: datetime) -> str:
        return v.strftime('%Y-%m-%d %H:%M')
```

### Wrap Serializers

Modify default behavior while keeping it.

```python
from pydantic import BaseModel, field_serializer
from decimal import Decimal

class Product(BaseModel):
    price: Decimal

    @field_serializer('price', mode='wrap')
    def round_price(self, v: Decimal, handler) -> str:
        # Get default serialization first
        default = handler(v)
        # Then modify
        return f'${default}'
```

### Annotated Serializers

Reusable serialization logic.

```python
from typing import Annotated
from pydantic import BaseModel, PlainSerializer
from datetime import datetime

def serialize_datetime(v: datetime) -> str:
    return v.isoformat()

ISODateTime = Annotated[datetime, PlainSerializer(serialize_datetime)]

class Event(BaseModel):
    created_at: ISODateTime
    updated_at: ISODateTime
```

## Model-Level Serializers

### Plain Model Serializer

Control entire model output.

```python
from pydantic import BaseModel, model_serializer

class Point(BaseModel):
    x: float
    y: float

    @model_serializer(mode='plain')
    def serialize(self) -> list[float]:
        return [self.x, self.y]

p = Point(x=1.0, y=2.0)
p.model_dump()  # [1.0, 2.0]
```

### Wrap Model Serializer

Modify default output.

```python
from pydantic import BaseModel, model_serializer

class User(BaseModel):
    name: str
    age: int

    @model_serializer(mode='wrap')
    def add_metadata(self, handler) -> dict:
        data = handler(self)
        data['_type'] = 'User'
        return data
```

## Computed Fields

Include computed values in serialization.

```python
from pydantic import BaseModel, computed_field

class Rectangle(BaseModel):
    width: float
    height: float

    @computed_field
    @property
    def area(self) -> float:
        return self.width * self.height

    @computed_field
    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

rect = Rectangle(width=10, height=5)
rect.model_dump()
# {'width': 10, 'height': 5, 'area': 50, 'perimeter': 30}
```

### Cached Computed Fields

For expensive computations.

```python
from functools import cached_property
from pydantic import BaseModel, computed_field

class Report(BaseModel):
    model_config = {'frozen': True}  # Required for cached_property

    data: list[int]

    @computed_field
    @cached_property
    def statistics(self) -> dict:
        # Expensive computation done once
        return {
            'sum': sum(self.data),
            'avg': sum(self.data) / len(self.data),
            'max': max(self.data),
        }
```

## Excluding Fields

### Field-Level Exclusion

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    password: str = Field(exclude=True)  # Never serialized

user = User(name='Alice', password='secret')
user.model_dump()  # {'name': 'Alice'}
```

### Dynamic Exclusion

```python
# At dump time
user.model_dump(exclude={'password'})

# Nested exclusion
class Order(BaseModel):
    user: User
    items: list[str]

order.model_dump(exclude={'user': {'internal_id'}})
```

## Aliasing in Serialization

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    user_id: int = Field(serialization_alias='id')
    user_name: str = Field(serialization_alias='name')

user = User(user_id=1, user_name='Alice')
user.model_dump()              # {'user_id': 1, 'user_name': 'Alice'}
user.model_dump(by_alias=True) # {'id': 1, 'name': 'Alice'}
```

## JSON Schema in Serialization

Control how fields appear in JSON schema.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(
        description='Product name',
        examples=['Widget', 'Gadget'],
        json_schema_extra={'format': 'product-name'}
    )
```

## Round-Trip Serialization

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# Serialize
user = User(name='Alice', age=30)
data = user.model_dump()
json_str = user.model_dump_json()

# Deserialize
user2 = User.model_validate(data)
user3 = User.model_validate_json(json_str)
```

## TypeAdapter Serialization

```python
from pydantic import TypeAdapter
from datetime import datetime

# Note: dump_json returns bytes, not str!
adapter = TypeAdapter(list[datetime])
dates = [datetime.now(), datetime.now()]

json_bytes = adapter.dump_json(dates)  # bytes
json_str = json_bytes.decode()         # str
```

## Best Practices

1. **Use `exclude_unset=True`** for partial updates
2. **Use `by_alias=True`** for API responses
3. **Use `mode='json'`** when output goes to JSON
4. **Prefer `@field_serializer`** over `@model_serializer` for field-specific logic
5. **Use `computed_field`** for derived values that should be serialized
6. **Use `Field(exclude=True)`** for sensitive data
