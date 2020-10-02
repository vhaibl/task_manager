from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from todo.models import Task
from todo.views import TaskViewSet


class SnippetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.user_low = User.objects.create_user('user', 'user@admin.com', 'user123')
        self.token = Token.objects.create(user=self.user)
        self.token_low = Token.objects.create(user=self.user_low)
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))
        self.bd_data = Task.objects.create(title="Create planner", description="test case", status="PLANNED",
                                           planned_by="2020-10-05T14:15:28Z", created="2020-09-29T14:15:32.653024Z",
                                           author=self.user_low)

    def test_create_post(self):
        response = self.client.post('/tasks/',
                                    {"title": "Create planner", "description": "test case", "status": "PLANNED",
                                     "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                     "author": 1}, format='json')

        self.assertEqual(response.status_code, 201)

    def test_get_list(self):
        api_request = APIRequestFactory().get("", HTTP_AUTHORIZATION='Token {}'.format(self.token_low))
        tasks_list = TaskViewSet.as_view({'get': 'list'})
        response = tasks_list(api_request)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_get_post(self):
        api_request = APIRequestFactory().get("", HTTP_AUTHORIZATION='Token {}'.format(self.token))
        tasks_list = TaskViewSet.as_view({'get': 'retrieve'})
        response = tasks_list(api_request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        response = self.client.put('/tasks/1/',
                                   {"title": "Create plannerUpdated", "description": "test case", "status": "PLANNED",
                                    "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                    "author": 2},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_update_post_wrong_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_low))
        response = self.client.put('/tasks/1/',
                                   {"title": "Create plannerUpdated", "description": "test case", "status": "PLANNED",
                                    "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                    "author": 1},
                                   format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_post_and_get_history_as_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token_low))

        update = self.client.put('/tasks/1/',
                                 {"title": "POST_________UPDATE", "description": "test case", "status": "PLANNED",
                                  "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                  "author": 2},
                                 format='json')

        api_request = APIRequestFactory().get(path="", HTTP_AUTHORIZATION='Token {}'.format(self.token_low))
        tasks_list = TaskViewSet.as_view({'get': 'history'})
        response = tasks_list(api_request, pk=1)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_update_post_and_get_history_as_admin(self):
            self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(self.token))

            update = self.client.put('/tasks/1/',
                                     {"title": "POST_________UPDATE", "description": "test case", "status": "PLANNED",
                                      "planned_by": "2020-10-05T14:15:28Z", "created": "2020-09-29T14:15:32.653024Z",
                                      "author": 1}, format='json')

            api_request = APIRequestFactory().get(path="", HTTP_AUTHORIZATION='Token {}'.format(self.token))
            tasks_list = TaskViewSet.as_view({'get': 'history'})
            response = tasks_list(api_request, pk=1)
            response.render()
            self.assertEqual(response.status_code, 200)

    def test_get_name(self):
        rororo = Task.objects.get(id=1)
        self.assertIn('Create planner', str(rororo))