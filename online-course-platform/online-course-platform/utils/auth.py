# utils/auth.py
class Auth:
    def __init__(self):
        self.users = {"user@example.com": "password123"}

    def login(self, email, password):
        return self.users.get(email) == password

    def signup(self, email, password):
        if email in self.users:
            return False
        self.users[email] = password
        return True
