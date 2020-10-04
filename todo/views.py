from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from todo.models import Task
from todo.serializers import TaskSerializer, FieldSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    """
    Filters usage:
    FILTER BY STATUS
    status=[PLANNED, NEW, INPROGRESS, COMPLETED]
    example:
    GET /tasks/?status=INPROGRESS
    will return tasks with in 'In progress' status

    FILTER BY PLANNED DATE
    planned_by__date__gte=YYYY-MM-DD  - date from
    planned_by__date__lte=YYYY-MM-DD  - date to
    examples:
    GET /tasks/?status=&planned_by__date__gte=2020-03-21 -
    will return all tasks with planned completion time starting from 2020 March 21
    GET /tasks/?status=&planned_by__date__lte=2021-01-31 -
    will return all tasks with planned completion date by 2021 January 31
    GET /tasks/?status=&planned_by__date__gte=2020-03-21&planned_by__date__lte=2021-01-31 will return all tasks with
    planned completion in range 2020 March 21 - 2021 January 31


    """

    class Meta:
        model = Task.history.model

    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = {'status': ['exact'],
                        'planned_by': ['date__gte', 'date__lte']}

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Task.objects.filter()
        else:
            return Task.objects.filter(author=self.request.user)

    @action(methods=['get'], detail=True)
    def history(self, request, pk, *args, **kwargs):
        if self.request.user.is_superuser:
            queryset = Task.objects.filter(pk=pk)
        else:
            queryset = Task.objects.filter(pk=pk, author=self.request.user)

        serializer = FieldSerializer(queryset, many=True)
        return Response(serializer.data)
