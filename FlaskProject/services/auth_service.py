from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, first_name, last_name, email, password, check_password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = password
        self.check_password = check_password
        self.is_admin = is_admin

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(password, self.__password)


users = {}

admin_user = User("Admin", "User", "admin@gmail.com", "admin123", "admin123", is_admin=True)
users["admin@gmail.com"] = admin_user

def register(first_name, last_name, email, password, check_password):
    new_user = User(first_name, last_name, email, password, check_password, is_admin=False)
    if email in users:
        return False
    users[email] = new_user
    print(f"We sent you confirmation email to {email}")
    return True


def login(email, password):
    if email in users:
        user = users[email]
        if password == user.password:
            return user
    return None

def get_user(email):
    return users.get(email)

