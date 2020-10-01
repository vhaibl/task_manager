from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'planned_by', 'created', 'author', 'id', 'history')
        read_only_fields = ('history',)

    def get_history(self, obj):
        return obj.history.all().values('title', 'description', 'status', 'planned_by', 'created', 'author')[1:]

    def validate_author(self, value):
        if not self.context['request'].user.is_superuser:
            if value != self.context['request'].user:
                raise ValidationError('Wrong author')
        return value


class FieldSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('history',)
        read_only_fields = ('history',)

    def get_history(self, obj):
        return obj.history.all().values('title', 'description', 'status', 'planned_by', 'created', 'author')[1:]
