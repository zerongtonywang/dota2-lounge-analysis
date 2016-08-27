from django.apps import apps
from django.contrib import admin

app = apps.get_app_config('app')

for model_name, model in app.models.items():
    exclude = ['baseuser_groups', 'baseuser_user_permissions']
    if model_name not in exclude:
        admin.site.register(model)
