from django.test import Client, TestCase

from posts.models import Post, User

class TestAccessRights(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='auth', password='1234')
        self.post = Post.objects.create(author=self.user, text='Test Post')

        
    def test_create_profile_page_after_registration(self):
        self.client.post('/auth/signup/', {'username': self.user.username, 'password1': self.user.password, 'password2': self.user.password})
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)
        
    def test_public_post_if_authorized(self):
        self.client.force_login(self.user)
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)
        
    
    def test_public_post_if_not_authorized(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)
        
    def test_check_post_after_publication_on_all_pages(self):
        self.client.force_login(self.user)
        self.client.post('/new/', {'text': 'Test Post'})
        response_index = self.client.get('/')
        self.assertContains(response_index, 'Test Post')
        response_profile = self.client.get(f'/{self.user.username}/')
        self.assertContains(response_profile, 'Test Post')
        response_post = self.client.get(f'/{self.user.username}/{self.post.id}/')
        self.assertContains(response_post, 'Test Post')
        
    def test_check_post_after_updating_on_all_pages(self):
        self.client.force_login(self.user)
        self.client.post(f'/{self.user.username}/{self.post.id}/edit/', {'text': 'Test Post Upadated'})
        response_index = self.client.get('/')
        self.assertContains(response_index, 'Test Post Upadated')
        response_profile = self.client.get(f'/{self.user.username}/')
        self.assertContains(response_profile, 'Test Post Upadated')
        response_post = self.client.get(f'/{self.user.username}/{self.post.id}/')
        self.assertContains(response_post, 'Test Post Upadated')
        
        
        
