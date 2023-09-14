# Copyright 2023 Wonder Dynamics

# This source code is licensed under the GNU GPLv3
# found in the LICENSE file in the root directory of this source tree.

"""Module for the validator class."""

class Validator:
    """Base class for defining validators. Methods need to be reimplemented be child class."""

    def __init__(self) -> None:
        self.message = 'Unique error message.'
        self.key = 'unique_check'

    def __call__(self) -> dict:
        data = self.get()
        check = self.check(data)
        return {'check': check, 'message': self.message}

    def get(self) -> type:
        """Returns the data to be checked."""
        data = None
        return data

    def check(self, data: type) -> bool:
        """Checks the data and returns True if validation passed and False otherwise"""
        if data:
            return True
        else:
            return False

    def expand_message(self, expansion_message: str) -> str:
        """Extends the message by appending a new line with the expansion_message."""
        self.message += f'\n{expansion_message}'
