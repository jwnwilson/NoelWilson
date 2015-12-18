from django.test import TestCase
from noelwilson.apps.data.models import Project , ProjectLists

class ProjectTest(TestCase):
    
    def setUp(self):
        pl = ProjectLists.objects.create(projectName='test')
        p = Project.objects.create(projectList = pl,title = 'testTitle',text = 'testText',
                                    videoFile = '/test/test/video',imageFile = '/test/test/image')
        pl.save()
        p.save()
        
    def test_ProjectTest(self):
        p = Project.objects.get(title__exact='testTitle')
        self.assertEqual(p.title, 'testTitle')
        self.assertEqual(p.text, 'testText')
        self.assertEqual(p.videoFile, '/test/test/video')
        self.assertEqual(p.imageFile, '/test/test/image')
