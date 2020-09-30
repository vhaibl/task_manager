from rest_framework import mixins, request, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from todo.models import Task
from todo.serializers import TaskSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    Tasks
    """

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(author=self.request.user)
