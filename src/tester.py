'''
Testing script
requires lorem-text to run
please install it before run
# pip install lorem-text
'''

import random
import requests
import configparser
try:
    from lorem_text import lorem
except ImportError:
    print('please install lorem-text: pip install lorem-text')
    exit(1)

host = 'http://localhost:5000'


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('test_config.ini')

    number_of_users = int(config['default']['number_of_users'])
    max_posts_per_user = int(config['default']['max_posts_per_user'])
    max_likes_per_user = int(config['default']['max_likes_per_user'])

    users = []
    posts = []
    for i in range(number_of_users):
        response = requests.post(
            f'{host}/users/signup',
            data={
                'email': f'email_{i}@email.com',
                'login': f'login_{i}',
                'password': 'password',
            }
        )
        user_id = response.json()['id']
        response = requests.post(
            f'{host}/users/login',
            data={
                'login': f'login_{i}',
                'password': 'password',
            }
        )
        users.append({'token': response.json()['token'], 'id': user_id})

    for user in users:
        number_of_posts = random.randint(1, max_posts_per_user)
        headers = {'Authorization': user['token']}
        for i in range(number_of_posts):
            response = requests.post(
                f'{host}/posts/',
                data={
                    'title': 'Post {i} by user {user[id]}',
                    'content': lorem.paragraph(),
                },
                headers=headers,
            )
            post = response.json()
            posts.append(post)

    for user in users:
        number_of_likes = random.randint(1, max_likes_per_user)
        headers = {'Authorization': user['token']}
        for i in range(number_of_likes):
            post_id = random.choice(posts)['id']
            requests.post(
                f'{host}/posts/{post_id}/like/',
                headers=headers,
            )
