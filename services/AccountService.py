import random
import string


class AccountService:
    @staticmethod
    def generate_random_email(domain='example.com', length=10) -> str:
        """
        Generate a random email address
        :param domain:
        :param length:
        :return:
        """
        letters = string.ascii_lowercase
        local_part = ''.join(random.choice(letters) for i in range(length))
        return f"{local_part}@{domain}"
