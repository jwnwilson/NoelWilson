from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from noelwilson.apps.accounts.models import UserProfile
from hashlib import md5

class UserProfileTest(TestCase):
    def setUp(self):
        u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        p = UserProfile.objects.create(user = u)
        u.save()
        p.save()
    def test_UserProfile(self):
        u = User.objects.get(username__exact='john')
        p = u.get_profile()
        password = 'johnpassword'
        _, salt, hashpw = p.user.password.split('$')
        self.assertEqual(p.user.username, 'john')
        self.assertEqual(p.user.email, 'lennon@thebeatles.com')
        self.assertEqual(md5(salt+password).hexdigest(), hashpw)

class ProfileViewsTestCase(TestCase):
    def setUp(self):
    	self.client = Client()
        u = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        p = UserProfile.objects.create(user = u)
        u.save()
        p.save()
        
    def test_profile(self):
        resp = self.client.post('/login/', {})
        self.assertEqual(resp.status_code, 200)
        # regular login
        user = self.client.login(username='john', password='johnpassword')
        resp = self.client.post('/login/', {})
        self.assertEqual(resp.status_code, 200)
