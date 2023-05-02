import logging
import pytz 
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import connections, DEFAULT_DB_ALIAS
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)



class CollaboratorModelTest(TestCase):

    def setUp(self):
        self.email = "test@collabshare.dev"
        self.mobile = "5179802142"
        self.password = "password123"
        self.first_name = "Ramin"
        self.last_name = "Esmzad"
        self.login_method = 'email'
        self.collaborator = get_user_model().objects.create(
            email=self.email,
            mobile=self.mobile,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            login_method=self.login_method
        )
        logger.info(self.collaborator.password)
        
    
    def tearDown(self):
        self.collaborator.delete()
    
    def test_create_collaborator(self):
        """
        Tests that default fields of collaborator are set correctly
        """
        self.assertTrue(isinstance(self.collaborator, get_user_model()))
        self.assertEqual(self.collaborator.email, self.email)
        self.assertEqual(self.collaborator.mobile, self.mobile)
        self.assertEqual(self.collaborator.first_name, self.first_name)
        self.assertEqual(self.collaborator.last_name, self.last_name)
        self.assertFalse(self.collaborator.is_staff)
        self.assertFalse(self.collaborator.is_active)
        self.assertFalse(self.collaborator.is_superuser)
        self.assertTrue(self.collaborator.date_joined)
        self.assertFalse(self.collaborator.is_mobile_verified)
        self.assertFalse(self.collaborator.is_email_verified)
        self.assertEqual(self.collaborator.get_full_name(), self.first_name + ' ' + self.last_name)
        self.assertEqual(self.collaborator.get_short_name(), self.first_name)
        self.assertEqual(self.collaborator.get_collabname(), self.email)
        self.assertEqual(f'{self.collaborator}', self.email)
        logger.info(f'password is {self.password}')

    def test_password_is_hashed(self):
        """ Test to ensure that the password is saved securely. """
        self.assertTrue(self.collaborator.check_password(self.password))

    def test_login_method_choices(self):
        """
        Tests that login_method only allows the defined choices
        """
        self.assertEqual(self.collaborator.login_method, get_user_model().LOGIN_EMAIL)
        self.collaborator.login_method = get_user_model().LOGIN_MOBILE
        self.collaborator.save()
        self.assertEqual(self.collaborator.login_method, get_user_model().LOGIN_MOBILE)
        self.collaborator.login_method = get_user_model().LOGIN_GOOGLE
        self.collaborator.save()
        self.assertEqual(self.collaborator.login_method, get_user_model().LOGIN_GOOGLE)
        self.collaborator.login_method = get_user_model().LOGIN_APPLE
        self.collaborator.save()
        self.assertEqual(self.collaborator.login_method, get_user_model().LOGIN_APPLE)

    def test_set_oauth2_credentials(self):
        """
        Tests the oauth2 credentials if Singup or Signin By Google or Apple
        """
        oaut2_id = "12345"
        access_token = "1234567890qwertyuioasdfggh"
        refresh_token = "1234567890qwertyuioasdfsdfsdf"
        tz = pytz.timezone('America/New_York')
        expires_in = tz.localize(datetime(2023, 4, 1))
        self.collaborator.set_oauth2_credentials(oaut2_id, access_token, refresh_token, expires_in)
        self.assertEqual(self.collaborator.oauth2_id, oaut2_id)
        self.assertEqual(self.collaborator.oauth2_access_token, access_token)
        self.assertEqual(self.collaborator.oauth2_refresh_token, refresh_token)
        self.assertEqual(self.collaborator.oauth2_expires_in, expires_in)


    def test_create_superuser(self):
        """
        Tests the creation of an admin collaborator
        """
        admin_ollaborator = get_user_model().objects.create_superuser(
            email="admin@collabshare.dev",
            password=self.password
        )
        self.assertTrue(admin_ollaborator.is_staff)
        

    