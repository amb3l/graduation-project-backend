class FileManagerUser:
    def __init__(self, name, folder):
        self.name = name
        self._folder = folder

    def get_folder(self):
        return self._folder

    def upload_to(self, instance, filename):
        return f'{self.get_folder()}/{filename}'


class FileManager:
    def __init__(self, root_folder):
        self._root_folder = root_folder
        self._users = []

    def get_users(self):
        return self._users

    def get_root_folder(self):
        return self._root_folder

    def init_user(self, name, folder):
        user = FileManagerUser(name, folder)
        self._users.append(user)
        return user
