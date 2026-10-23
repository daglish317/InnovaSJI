from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'apps.projects'
    label = 'projects'

    def ready(self):
        import apps.projects.signals
