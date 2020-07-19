class Storage:
    def __init__(self, initial_data=None):
        if initial_data is None:
            initial_data = {}
        self.s = initial_data

    def add(self, key, value):
        self.s[key] = value

    def delete(self, key):
        self.s.pop(key)

    def get_all(self):
        return self.s


class Server:
    def __init__(self, storage):
        self.storage = storage

    def add_user(self, name, ip_port):
        return self.storage.add(name, ip_port)

    def delete_user(self, name):
        return self.storage.delete(name)

    def get_all_users(self):
        return self.storage.get_all()
