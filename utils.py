import random
import string


class Utils:
    def generate_url(self, length):
        return 'p'.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
