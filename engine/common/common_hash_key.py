import random
import string


def secret_key(default_str, length=30):
    """
    Generate secret key from alpha and digit.
    :param length: length of secret key.
    :return: [length] long secret key.
    """
    key_str = default_str.replace(' ', '').strip()
    key = ''
    while length:
        key += random.choice(string.ascii_letters + string.digits + key_str)
        length -= 1

    return key



if __name__ == "__main__":
    print(secret_key('admin@torro.ai', 32))

