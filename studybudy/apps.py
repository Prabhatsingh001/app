from django.apps import AppConfig


class StudybudyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'studybudy'
    def ready(self):
        import studybudy.signals  # noqa: F401
