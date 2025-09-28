users = []

def register(first_name, last_name, email, password):
    for user in users:
        if user['email'] == email and user['password'] == password:
            return False

    users.append({"first_name": first_name, "last_name": last_name, "email": email, "password": password})
    print(f"We sent you confirmation email to {email}")
    return True


def login(email, password):
    for user in users:
        if user['email'] == email and user['password'] == password:
            return True

    return False

