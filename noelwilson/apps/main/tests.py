from django.test import TestCase
"""
	simple tests needs expanding
"""

class MainViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        
    def test_technical(self):
        resp = self.client.get('/technical/')
        self.assertEqual(resp.status_code, 200)
        
    def test_artwork(self):
        resp = self.client.get('/artwork/')
        self.assertEqual(resp.status_code, 200)
        
    def test_training(self):
        resp = self.client.get('/training/')
        self.assertEqual(resp.status_code, 200)            
