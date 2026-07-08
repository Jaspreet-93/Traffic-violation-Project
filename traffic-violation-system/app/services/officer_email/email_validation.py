import re

class EmailValidation:
    @staticmethod
    def is_valid(email: str) -> bool:
        """
        Validates email address syntax structure.
        """
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
