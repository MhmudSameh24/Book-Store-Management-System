class User:
    def __init__(self):
        self.user_id = None
        self.email = None
    def set_id(self, user_id):
        self.user_id = user_id
    def set_email(self, email):
        self.email = email
    def get_id(self):
        return self.user_id
    def get_email(self):
        return self.email