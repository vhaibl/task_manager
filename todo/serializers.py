from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'planned_by', 'created', 'author')

    def validate_author(self, value):
        print(self.context['request'].user)
        if not self.context['request'].user.is_superuser:
            if value != self.context['request'].user:
                raise ValidationError('Wrong author')
        return value

