import random
import string
from typing import Dict, Any, Optional
import re
from zxcvbn import zxcvbn

class Password:
    def __init__(self, options: Dict[str, Any]) -> None:
        self.include_upper = options.get('include_upper', False)
        self.include_lower = options.get('include_lower', False)
        self.include_numbers = options.get('include_numbers', False)
        self.include_special = options.get('include_special', False)
        self.exclude_char = options.get('exclude_char', '')
        self.length = options.get('length', 8)

        # Escape special characters for inclusion in regex
        if self.exclude_char:
            escaped_exclude_char = re.escape(self.exclude_char)
        else:
            escaped_exclude_char = ""

        # Define character sets
        self.lowercase = re.sub(f"[{escaped_exclude_char}]", '', string.ascii_lowercase) if self.exclude_char else string.ascii_lowercase
        self.uppercase = re.sub(f"[{escaped_exclude_char}]", '', string.ascii_uppercase) if self.exclude_char else string.ascii_uppercase
        self.digits = re.sub(f"[{escaped_exclude_char}]", '', string.digits) if self.exclude_char else string.digits
        self.special = re.sub(f"[{escaped_exclude_char}]", '', "-_.@#$?") if self.exclude_char else "-_.@#$?"

    def get_random_segment(self, characters: str, segment_length: int) -> str:
        return ''.join(random.choice(characters) for _ in range(segment_length))

    def static_random_part(self, keyword: str = "") -> str:
        # Ensure the keyword meets minimum complexity requirements
        if self.include_lower and not re.search('[a-z]', keyword):
            keyword += random.choice(self.lowercase)
        if self.include_upper and not re.search('[A-Z]', keyword):
            keyword += random.choice(self.uppercase)
        if self.include_special and not re.search(r'[-_.@#$?]', keyword):
            keyword += random.choice(self.special)
        if self.include_numbers and not re.search(r'[0-9]', keyword):
            keyword += random.choice(self.digits)

        # Remaining length after adding keyword
        remaining_length = self.length - len(keyword)

        # Combine all character sets
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        if remaining_length > 0:
            random_segment = self.get_random_segment(all_chars, remaining_length)
            # Create password
            password = keyword + random_segment
        else:
            password = keyword[:self.length]

        return password

    def password_generator(self, keyword: str = "") -> str:
        static_part = self.static_random_part(keyword)
        remaining_len = self.length - len(static_part)
        if remaining_len > 0:
            all_chars = self.lowercase + self.uppercase + self.digits + self.special
            password = static_part + self.get_random_segment(all_chars, remaining_len)
        else:
            password = static_part[:self.length]

        return password

class PasswordStrengthChecker:
    def check_strength(self, password: str) -> Dict[str, Any]:
        result = zxcvbn(password)
        
        score = result['score']  # 0 (very weak) to 4 (very strong)
        
        # Strength mapping
        strength = {
            0: 'Very Weak',
            1: 'Weak',
            2: 'Fair',
            3: 'Strong',
            4: 'Very Strong'
        }.get(score, 'Unknown')

        # Feedback mapping
        feedback = {
            0: 'Password is guessable in a fraction of a second.',
            1: 'Password is easily guessable.',
            2: 'Strength can be increased with additional complexity.',
            3: 'Strong enough for most purposes.',
            4: 'Very strong, enough to bother even a hacker.'
        }.get(score, 'No feedback available.')

        # Crack time information
        crack_time_seconds = result.get('crack_times_seconds', {}).get('online_no_throttling_10_per_second', 'N/A')
        crack_time_display = result.get('crack_times_display', {}).get('online_no_throttling_10_per_second', 'N/A')
        
        return {
            'password_strength_value': strength,
            'feedback': feedback,
            'crack_time_seconds': crack_time_seconds,
            'crack_time_display': crack_time_display
        }

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
        self.strength_checker = PasswordStrengthChecker()

    def validate_input_length(self) -> bool:
        # Check if 'length' is an integer and within acceptable bounds
        length = self.options.get('length', None)
        
        if length is None:
            raise ValueError("Password length not provided")
        if not isinstance(length, int):
            raise ValueError(f"Password length must be an integer, got {type(length).__name__}")
        if length <= 0:
            raise ValueError("Password length must be greater than zero")
        if length > 256:  # Set a sensible upper bound
            raise ValueError("Password length exceeds maximum allowed length of 256 characters")
        
        return True


    def set_options(self, options: Dict[str, Any]) -> None:
        # Ensure that the length is an integer, even if passed as a string
        if 'length' in options:
            try:
                options['length'] = int(options['length'])  # Convert to integer
            except ValueError:
                raise ValueError("Password length must be a valid integer")
        
        self.options = options


    def set_keyword(self, keyword: Optional[str]) -> None:
        self.keyword = keyword

    def generate_password(self) -> Dict[str, Any]:
        if not self.validate_input_length():
            raise ValueError("Invalid input length")

        p1 = Password(self.options)
        password = p1.password_generator(keyword=self.keyword if self.keyword else "")
        strength_info = self.strength_checker.check_strength(password)
        
        return {
            'password': password,
            'strength': strength_info['password_strength_value'],
            'feedback': strength_info['feedback'],
            'crack_time_seconds': strength_info['crack_time_seconds'],
            'crack_time_display': strength_info['crack_time_display']
        }

# Example Usage
'''if __name__ == "__main__":
    # Create a PasswordGenerator instance
    generator = PasswordGenerator()

    # Set options for the generator
    generator.set_options({
        'include_upper': True,
        'include_lower': True,
        'include_numbers': True,
        'include_special': True,
        'exclude_char': 'trdgfh',  # Exclude certain characters
        'length': 200
    })

    # Set an optional keyword for the generator
    generator.set_keyword("")

    # Generate a password
    result = generator.generate_password()

    # Display the generated password and its strength information
    print("Generated Password:", result['password'])
    print("Password Strength:", result['strength'])
    print("Feedback:", result['feedback'])
    print("Crack Time (seconds):", result['crack_time_seconds'])
    print("Crack Time (display):", result['crack_time_display'])'''