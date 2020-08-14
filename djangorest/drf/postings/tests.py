from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings

from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from .models import BlogPost

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(username='testhexuser', email='hex@hex.com')
        user_obj.set_password('asd')
        user_obj.save()
        blog_post = BlogPost.objects.create(user=user_obj,
                                            title='new title', content='some content')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEquals(user_count, 1)

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEquals(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('postings:post-listblogs')
        response = self.client.get(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        data = {'title': 'Some title', 'content': 'some content'}
        url = api_reverse('postings:post-listblogs')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title': 'Some rando title', 'content': 'some rando content'}
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title': 'Some rando title', 'content': 'some rando content'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        data = {'title': 'Some title', 'content': 'some content'}
        url = api_reverse('postings:post-listblogs')
        response = self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='tester')
        blog_post = BlogPost.objects.create(
            user=owner,
            title='very new title',
            content='some other content')

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        data = {'title': 'Some title', 'content': 'some content'}
        url = blog_post.get_api_url()
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login(self):
        data = {
            'username': 'testhexuser',
            'password': 'asd'
        }
        url = api_reverse('login')
        response = self.client.post(url, data)
        print(response.data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)