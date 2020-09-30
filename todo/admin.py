from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from todo.models import Task

admin.site.register(Task, SimpleHistoryAdmin)
