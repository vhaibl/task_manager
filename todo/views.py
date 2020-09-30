from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from todo.models import Task
from todo.serializers import TaskSerializer, FieldSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    Tasks
    """

    class Meta:
        model = Task.history.model

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()
        else:
            return Task.objects.filter(author=self.request.user)

    @action(methods=['get'], detail=True)
    def me(self, request, pk, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = Task.objects.filter(pk=pk)
        else:
            queryset = Task.objects.filter(pk=pk, author=self.request.user)

        serializer = FieldSerializer(queryset, many=True)
        return Response(serializer.data)
