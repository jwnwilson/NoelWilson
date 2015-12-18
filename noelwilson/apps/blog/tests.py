"""
    simple tests needs expanding
    need to cover post results
"""
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from noelwilson.apps.accounts.models import UserProfile

class MainViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        p = UserProfile.objects.create(user = u)
        u.save()
        p.save()
        
    def test_blogEntry(self):
        user = self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/myBlog/blogEntry/')
        self.assertEqual(resp.status_code, 200)
        
    def test_myBlog(self):
        resp = self.client.get('/myBlog/')
        self.assertEqual(resp.status_code, 200)
        
    def test_blogManager(self):
        user = self.client.login(username='john', password='johnpassword')
        resp = self.client.get('/myBlog/blogManager/')
        self.assertEqual(resp.status_code, 200)
        
    """def test_postView(self):
        resp = self.client.get('/myBlog/postView/')
        self.assertEqual(resp.status_code, 200)"""
        
    def test_newCategory(self):
        resp = self.client.get('/myBlog/newCategory/')
        self.assertEqual(resp.status_code, 200) 
