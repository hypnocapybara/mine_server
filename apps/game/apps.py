from django.apps import AppConfig


class GameConfig(AppConfig):
    name = 'apps.game'

    def ready(self):
        import apps.game.signals
