from zxcvbn import zxcvbn

class PasswordStrengthChecker:
    def check_strength(self, password):
        result = zxcvbn(password)
        score = result['score']  # 0 (weak) to 4 (strong)
        strength = 'weak' if score in [0, 1] else 'medium' if score in [2, 3] else 'strong'
        return strength