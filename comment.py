from dataclasses import dataclass


@dataclass
class Comment:
    video: str
    text: str
    id: str = None


class InvalidCommentException(Exception):
    """Exception raised if one of the Comment fields is missing"""

    def __init__(self, comment: dict):
        self.message = 'One or more of comment fields are missing: '
        for key, value in comment.items():
            if not value:
                self.message += f'{key} '

        super().__init__(self.message)
