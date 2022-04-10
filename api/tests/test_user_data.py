

from unittest.mock import MagicMock
from django.core.files import File

from rest_framework.test import APITestCase



from api.models import UserData


class UserDataTest(APITestCase):

    def setUp(self):
        file_mock = MagicMock(spec=File)
        file_mock.name = 'photo.jpg'
        test_user1 = UserData.objects.create_user(first_name='Test1',last_name='Test12',image=file_mock,
                                                email='asdsadsa@asds.ds',password='test1')
        test_user1.save()
        test_user2 = UserData.objects.create_user(first_name='Test2',last_name='Test22',image=file_mock,
                                                email='asdsadsa@ass.ds',password='test2')
        test_user2.save()
    
    def test_user_is_no_staff(self):
        ss = UserData.objects.get(pk=1)
        ss2 = UserData.objects.get(pk=2)
        self.assertEqual(ss.first_name,'Test1')
        self.assertEqual(ss2.first_name, 'Test2')
        self.assertFalse(ss.is_staff)
        self.assertFalse(ss2.is_staff)
    

    
    
        