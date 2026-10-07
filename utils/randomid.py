import random
import string

characters = string.ascii_lowercase + string.digits

random_string = ''.join(random.choices(characters, k=8))

print(random_string)
