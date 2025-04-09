from flask_bcrypt import Bcrypt
from sys import argv

bcrypt = Bcrypt()

if __name__ == "__main__":
    if len(argv) != 2:
        print("Argument errors, need 2")
        exit()

    password = bcrypt.generate_password_hash(argv[1]).decode('utf-8')

    print(password)