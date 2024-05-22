import random
import string

'''
    Exception handling for invalid input
'''

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
    def get_random_segment(self,characters, segment_length):
        return ''.join(random.choice(characters) for _ in range(segment_length))
    

    # Generates password with keyword
    def keyword_password(self, keyword):
        if len(keyword) > self.length:
            raise ValueError("Keyword length cannot be greater than the desired password length")
        
        # Minimum one number check
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
        #random.shuffle(password)
        
        return ''.join(password)
    
    # Generates password without keyword
    def without_keyword_password(self):
    
        # Combine all character sets
        all_chars = self.lowercase + self.uppercase + self.digits + self.special
        password = self.get_random_segment(all_chars, self.length)
        
        return password

# User input
keyword = input("Enter a keyword or -(for no keyword): ")
include_upper = input("Include uppercase letters? (y/n): ")
include_lower = input("Include lowercase letters? (y/n): ")
include_numbers = input("Include numbers? (y/n): ")
include_special = input("Include special characters? (y/n): ")
length = int(input("Enter the desired password length: "))

# Instantiate the Password class
p1 = Password(include_upper, include_lower, include_numbers, include_special, length)

# Generate password based on user input
if keyword == "-":
    print("Generated Password:", p1.without_keyword_password())
else:
    print("Generated Password:", p1.keyword_password(keyword))