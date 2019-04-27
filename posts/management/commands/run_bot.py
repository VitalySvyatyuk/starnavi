import json
from random import choice, randrange

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from posts.models import CustomUser, Post


class Command(BaseCommand):
    help = 'Creates users, posts, votes through api'
    headers = {'content-type': 'application/json'}

    def handle(self, *args, **options):
        # Create users
        for user_number in range(settings.NUMBER_OF_USERS):
            requests.post(
                f'{settings.TEST_DOMAIN}api/v1/createuser/',
                data={
                    'username': f'TestUser{user_number}',
                    'email': f'test{user_number}@gmail.com',
                    'password': f'TestUser{user_number}'})

        users = CustomUser.objects.all()
        # Create of posts from different users
        for user in users:
            if user.username.startswith('TestUser'):
                token = self.get_token(user.username, user.username)
                for post_number in range(randrange(settings.MAX_POSTS_PER_USER)):
                    data = {'title': f'Post {post_number} by {user.username}',
                            'text': f'Text {post_number} by {user.username}',
                            'user': user.id}
                    requests.post(
                        f'{settings.TEST_DOMAIN}api/v1/posts/',
                        data=json.dumps(data),
                        headers={**self.headers, 'Authorization': f'Bearer {token}'})

        # Set votes from authorized users
        for user in users:
            if user.username.startswith('TestUser'):
                token = self.get_token(user.username, user.username)
                posts = Post.objects.all().exclude(user=user).order_by('?')
                for post in posts[:randrange(settings.MAX_LIKES_PER_USER)]:
                    data = {'like': choice([1, -1])}
                    requests.post(
                        f'{settings.TEST_DOMAIN}api/v1/posts/{post.id}/set_like/',
                        data=json.dumps(data),
                        headers={**self.headers, 'Authorization': f'Bearer {token}'})

        self.stdout.write(self.style.SUCCESS('Success'))

    @staticmethod
    def get_token(username, password):
        # Obtain new token for the user
        response = requests.post(
            f'{settings.TEST_DOMAIN}api/v1/token/',
            data={'username': f'{username}', 'password': f'{password}'})
        token = response.json()['access']
        return token
