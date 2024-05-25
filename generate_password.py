import random
import string

class Password:
    def __init__(self, include_upper, include_lower, include_numbers, include_special, length):
        self.include_upper = include_upper.lower() == 'y'
        self.include_lower = include_lower.lower() == 'y'
        self.include_numbers = include_numbers.lower() == 'y'
        self.include_special = include_special.lower() == 'y'
        self.length = length

        # Define character sets
        self.lowercase = string.ascii_lowercase if self.include_lower else ""
        self.uppercase = string.ascii_uppercase if self.include_upper else ""
        self.digits = string.digits if self.include_numbers else ""
        self.special = "-_.@#$?" if self.include_special else ""

        # Validate at least one character set is selected
        if not (self.lowercase or self.uppercase or self.digits or self.special):
            raise ValueError("At least one character set must be selected")

    # Get a random segment from the combined character sets
    def get_random_segment(self, characters, segment_length):
        return ''.join(random.choice(characters) for _ in range(segment_length))
    
    def static_random_part(self,keyword = ""):
         # Ensure the keyword meets minimum complexity requirements
        if not any(char.isdigit() for char in keyword):
            keyword += random.choice(string.digits)
        if not any(char.isupper() for char in keyword):
            keyword += random.choice(string.ascii_uppercase)
        if not any(char in self.special for char in keyword):
            keyword += random.choice(self.special)
        if not any(char.islower() for char in keyword):
            keyword += random.choice(string.ascii_lowercase)

        # Remaining length after adding keyword
        remaining_length = self.length - len(keyword)

        # Combine all character sets
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        random_segment = self.get_random_segment(all_chars, remaining_length)

        # Create password and shuffle
        password = keyword + random_segment
        #random.shuffle(list(password))
        
        return ''.join(password)

    # Generates password with keyword
    def keyword_password(self, keyword):
        if len(keyword) > self.length:
            raise ValueError("Keyword length cannot be greater than the desired password length")
        
        return self.static_random_part(keyword)


    # Generates password without keyword
    def without_keyword_password(self):
        # Combine all character sets
        password = self.static_random_part()
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        password = self.get_random_segment(all_chars, self.length)

        return password

class PasswordGenerator:
    def __init__(self):
        self.keyword = None
        self.include_upper = None
        self.include_lower = None
        self.include_numbers = None
        self.include_special = None
        self.length = None

    def validate_input_length(self):
        valid_len = len(self.keyword) + (self.include_upper == 'y') + (self.include_lower == 'y') + (self.include_numbers == 'y') + (self.include_special == 'y')
        if self.length < valid_len:
            print("Password length must be greater than or equal to the sum of the selected character sets")
            return False
        return True

    def get_user_input(self):
        self.keyword = input("Enter a keyword (Optional): ")
        self.include_upper = input("Include uppercase letters? (y/n): ")
        self.include_lower = input("Include lowercase letters? (y/n): ")
        self.include_numbers = input("Include numbers? (y/n): ")
        self.include_special = input("Include special characters? (y/n): ")
        self.length = int(input("Enter the desired password length: "))

    def generate_password(self):
        self.get_user_input()
        
        if not self.validate_input_length():
            self.generate_password()
        
        # Instantiate the Password class
        p1 = Password(self.include_upper, self.include_lower, self.include_numbers, self.include_special, self.length)
        
        # Generate password based on user input
        if self.keyword == "":
            print("Generated Password:", p1.without_keyword_password())
        else:
            print("Generated Password:", p1.keyword_password(self.keyword))

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.generate_password()