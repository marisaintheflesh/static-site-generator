import random
import string

def random_name():
    size = 8
    name = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(size)])

    return name

def main():
    name = random_name()
    print(name)
    exit()

if __name__ == "__main__":
    main()

