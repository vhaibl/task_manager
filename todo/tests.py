from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from todo.models import Task
from todo.views import TaskViewSet


class SnippetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.bd_data = Task.objects.create(title="Create planner", description="test case", status="PLANNED",
                                           planned_by="2020-10-05T14:15:28Z", created="2020-09-29T14:15:32.653024Z",
                                           author=self.user)
    def test_create_post(self):
        response = self.client.post('/tasks/',
                                    {"title": "Create planner", "description": "test case", "status": "PLANNED",
                                     "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                     "author": 1}, format='json')

        self.assertEqual(response.status_code, 201)
        print('after create post', Task.objects.all())

    def test_get_post(self):
        print('before get post', Task.objects.filter(author=1))

        api_request = APIRequestFactory().get("", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        tasks_list = TaskViewSet.as_view({'get': 'retrieve'})
        response = tasks_list(api_request, pk=1)
        response.render()
        print('after get post', response.content)

    def test_update_post(self):
        response = self.client.put('/tasks/1/',
                                   {"title": "Create plannerUpdated", "description": "test case", "status": "PLANNED",
                                    "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                    "author": 1},
                                   format='json')
        print('after update', response.json())

        self.assertEqual(response.status_code, 200)
