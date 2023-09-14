# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module where the TypeValidator class is defined."""

from dataclasses import dataclass
from dataclasses import is_dataclass
from typing import get_args
from typing import Union
from typing import Any


@dataclass
class TypeValidator:
    """Class that is able to check the type of its annotated data members."""

    def __post_init__(self):
        for field_name, field_type in self.__annotations__.items():  # pylint: disable=no-member
            value = getattr(self, field_name)
            self._check_type(field_name, value, field_type)

    def _check_type(self, field_name: str, value: str, field_type: Any):
        origin = getattr(field_type, '__origin__', None)
        if origin is not None:
            if origin is Union:
                union_types = get_args(field_type)
                new_value = None
                for type_ in union_types:
                    try:
                        new_value = self._check_type(field_name, value, type_)
                        break
                    except TypeError:
                        pass
                if new_value is None and value is not None:
                    raise TypeError(f'Expected one of {union_types}, got {type(value)} for field {field_name}')
                setattr(self, field_name, new_value)
            elif issubclass(origin, list):
                if not isinstance(value, origin):
                    raise TypeError(f'Expected {str(field_type)}, got {type(value)} for field {field_name}')
                element_type = get_args(field_type)[0]
                new_value = []
                for item in value:
                    self._check_type(field_name, item, element_type)
                    new_value.append(item)
                setattr(self, field_name, new_value)
            return value
        elif is_dataclass(field_type):
            if not isinstance(value, field_type):
                if isinstance(value, dict):
                    value = field_type(**value)
                setattr(self, field_name, value)
            for sub_field_name, sub_field_type in field_type.__annotations__.items():
                if isinstance(value, field_type):
                    sub_value = getattr(value, sub_field_name)
                    self._check_type(f'{field_name}.{sub_field_name}', sub_value, sub_field_type)
            return value
        else:
            if not isinstance(value, field_type):
                raise TypeError(f'Expected {str(field_type)}, got {type(value)} for field {field_name}')
            return value
