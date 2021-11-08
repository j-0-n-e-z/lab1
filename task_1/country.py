class Country:
    name = ''
    users_count = 1

    def __init__(self, name):
        self.name = name

    def increase_users_count(self):
        self.users_count += 1
