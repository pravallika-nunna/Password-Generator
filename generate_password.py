import random
import string
from typing import Dict, Any, Optional

class Password:
    def __init__(self, options: Dict[str, Any]) -> None:
        self.include_upper = options.get('include_upper', False)
        self.include_lower = options.get('include_lower', False)
        self.include_numbers = options.get('include_numbers', False)
        self.include_special = options.get('include_special', False)
        self.exclude_char = options.get('exclude_char', '')
        self.length = options.get('length', 8)

        # Define character sets
        self.lowercase = ''.join(c for c in string.ascii_lowercase if c not in self.exclude_char) if self.include_lower else ""
        self.uppercase = ''.join(c for c in string.ascii_uppercase if c not in self.exclude_char) if self.include_upper else ""
        self.digits = ''.join(c for c in string.digits if c not in self.exclude_char) if self.include_numbers else ""
        self.special = ''.join(c for c in "-_.@#$?" if c not in self.exclude_char) if self.include_special else ""

        # Validate at least one character set is selected
        if not (self.lowercase or self.uppercase or self.digits or self.special):
            raise ValueError("At least one character set must be selected")

    def get_random_segment(self, characters: str, segment_length: int) -> str:
        return ''.join(random.choice(characters) for _ in range(segment_length))

    def static_random_part(self, keyword: str = "") -> str:
        # Ensure the keyword meets minimum complexity requirements
        if self.include_lower and self.lowercase and not any(char.islower() for char in keyword):
            keyword += random.choice(self.lowercase)
        if self.include_upper and self.uppercase and not any(char.isupper() for char in keyword):
            keyword += random.choice(self.uppercase)
        if self.include_special and self.special and not any(char in self.special for char in keyword):
            keyword += random.choice(self.special)
        if self.include_numbers and self.digits and not any(char.isdigit() for char in keyword):
            keyword += random.choice(self.digits)

        # Remaining length after adding keyword
        remaining_length = self.length - len(keyword)

        # Combine all character sets
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        random_segment = self.get_random_segment(all_chars, remaining_length)

        # Create password
        password = keyword + random_segment

        return password

    def password_generator(self, keyword: str = "") -> str:
        # Combine all character sets
        static_part = self.static_random_part(keyword)
        remaining_len = self.length - len(static_part)
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        password = static_part + self.get_random_segment(all_chars, remaining_len)

        return password

class PasswordGenerator:
    def __init__(self) -> None:
        self.options: Dict[str, Any] = {
            'include_upper': False,
            'include_lower': False,
            'include_numbers': False,
            'include_special': False,
            'exclude_char': '',
            'length': 8
        }
        self.keyword: Optional[str] = None

    def validate_input_length(self) -> bool:
        valid_len = len(self.keyword) + sum(1 for key in self.options if self.options[key] == 'y')

        if not isinstance(self.options['length'], int):
            print("Password length must be an integer.")
            return False

        if self.options['length'] < valid_len:
            print("Password length must be greater than or equal to the sum of the selected character sets and keyword length")
            print("Password must be greater than", valid_len)
            return False
        return True
    
    def validate(self) -> bool:
        # Validate at least one character set is selected
        if not any(self.options[key] for key in ['include_lower', 'include_upper', 'include_numbers', 'include_special']):
            print("At least one character set must be selected")
            return False
        return True

    def get_user_input(self) -> None:
        self.keyword = input("Enter a keyword (Optional): ")

        def validate_yes_no(prompt: str) -> bool:
            while True:
                try:
                    value = input(prompt).strip().lower()
                    if value not in ['y', 'n']:
                        raise ValueError("Invalid input. Please enter 'y' or 'n'.")
                    return value == 'y'
                except ValueError as ve:
                    print(ve)

        def validate_positive_int(prompt: str) -> int:
            while True:
                try:
                    value = int(input(prompt))
                    if value <= 0:
                        raise ValueError("Password length must be a positive integer.")
                    return value
                except ValueError as ve:
                    print(ve)

        self.options['include_upper'] = validate_yes_no("Include uppercase letters? (y/n): ")
        self.options['include_lower'] = validate_yes_no("Include lowercase letters? (y/n): ")
        self.options['include_numbers'] = validate_yes_no("Include numbers? (y/n): ")
        self.options['include_special'] = validate_yes_no("Include special characters? (y/n): ")
        self.options['exclude_char'] = input("Any characters to exclude? ")
        self.options['length'] = validate_positive_int("Enter the desired password length: ")

        if not self.validate():
            self.get_user_input()

    def generate_password(self) -> None:
        self.get_user_input()
        
        # Checking the password length
        if not self.validate_input_length():
            self.options['length'] = int(input("Enter desired password length"))
        
        # Instantiate the Password class - Create an object
        p1 = Password(self.options)
        
        # Generate password based on user input
        if self.keyword == "":
            print("Generated Password:", p1.password_generator())
        else:
            print("Generated Password:", p1.password_generator(keyword=self.keyword))

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.generate_password()