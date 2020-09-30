from django.urls import path
from rest_framework.routers import DefaultRouter

from todo.views import TaskViewSet

app_name = "tasks"

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')
urlpatterns = router.urls

# app_name will help us do a reverse look-up latter.

# urlpatterns = [
#     path('tasks/', TaskView.as_view({'get': 'list'})),
#     path('tasks/<int:pk>', TaskView.as_view({'get': 'retrieve'})),
# ]
