from zxcvbn import zxcvbn

class PasswordStrengthChecker:
    def check_strength(self, password):
        result = zxcvbn(password)
        
        score = result['score']  # 0 (very weak) to 4 (very strong)
        strength = {
            0: 'Very Weak',
            1: 'Weak',
            2: 'Fair',
            3: 'Strong',
            4: 'Very Strong'
        }.get(score, 'Unknown')

        feedback = {
            0: 'Password is guessable in a fraction of a second.',
            1: 'Password is easily guessable.',
            2: 'Strength can be increased with additional complexity.',
            3: 'Strong enough for most purposes.',
            4: 'Very strong, enough to bother even a hacker.'
        }.get(score, 'No feedback available.')

        crack_time_seconds = result.get('crack_times_seconds', {}).get('online_no_throttling_10_per_second', 'N/A')
        crack_time_display = result.get('crack_times_display', {}).get('online_no_throttling_10_per_second', 'N/A')
        
        return {
            'strength': strength,
            'feedback': feedback,
            'crack_time_seconds': crack_time_seconds,
            'crack_time_display': crack_time_display
        }