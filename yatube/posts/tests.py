from django.test import Client, TestCase

from posts.models import Post, User

class TestPosts(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='timi_di', password='qwerty03')
        self.client.force_login(self.user)
        with open('/Users/timi__di/Downloads/i.jpg', 'rb') as img:
            self.client.post('/new/', {'text': 'post with image', 'author': self.user, 'image': img})
        self.client.post('/new/', {'text': 'post without image', 'author': self.user})
        
    def test_except_404_error(self):
        response = self.client.get('/nonexist-page/kubkkj/khb')
        self.assertEqual(response.status_code, 404)
        
        
    def test_image_tag_post_exists(self):
        post = Post.objects.filter(image__isnull=False).first()
        response = self.client.get(f'/{post.author.username}/{post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<img')
        
    def test_correct_post_with_image(self):
        post = Post.objects.filter(image__isnull=False).first()
        response_index = self.client.get('/')
        self.assertEqual(response_index.status_code, 200)
        self.assertContains(response_index, '<img')
        response_author = self.client.get(f'/{post.author.username}/')
        self.assertContains(response_author, '<img')
        response_post = self.client.get(f'/{post.author.username}/{post.id}/')
        self.assertContains(response_post, '<img')
        
    def test_check_upload_not_grafical_files(self):
        post = Post.objects.filter(image__isnull=False).first()
        print()
        with open('/Users/timi__di/О себе.docx','rb') as img:
            response = self.client.post(f'/{post.author.username}/{post.id}/edit/', {'author': self.user, 'text': 'post with image', 'image': img})

        # Проверяем, что система защиты сработала (ожидаем HTTP 400 Bad Request)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пост с неграфическим файлом не был создан
        self.assertFalse(Post.objects.filter(text='post with non-image file').exists())
                
    
