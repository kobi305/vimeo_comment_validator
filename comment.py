from dataclasses import dataclass, fields, Field
from typing import Tuple


class InvalidCommentException(Exception):
    """Exception raised if one of the Comment fields is missing"""

    def __init__(self, comment: dict):
        self.message = 'One or more of comment fields are missing: '
        for key, value in comment.items():
            if not value:
                self.message += f'{key} '

        super().__init__(self.message)


@dataclass
class Comment:
    video: str = None
    text: str = None
    id: str = None
    is_verified: bool = False

    def validate(self):
        cls_fields: Tuple[Field, ...] = fields(self.__class__)

        for field in cls_fields:
            if not getattr(self, field.name) and field.name != 'is_verified':
                raise InvalidCommentException(self.__dict__)
