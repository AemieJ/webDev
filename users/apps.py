from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    #When user created
    def ready(self) : 
        import users.signals