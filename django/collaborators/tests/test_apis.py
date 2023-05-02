import logging
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from collaborators.serializers import CollaboratorSignupEmailSerializer

logger = logging.getLogger(__name__)

class CollaboratorAPIsV1Test(APITestCase):
    """ Test class to sign up a collaborator to the collabshare.dev platform. """


    def test_collaborator_urls(self):
        """ Test to Ensure that the URLs for collaborator are correct. """
        self.assertEqual(reverse('collaborators:v1_signup'), '/api/v1/collaborators/signup/')

    def test_collaborator_signup_no_email_password(self):
        """ Test to ensure that the required fields (email and password) are set. """
        url = reverse('collaborators:v1_signup')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_collaborator_signup_invalid_email(self):
        """ Test to ensure that the email is valid. """
        url = reverse('collaborators:v1_signup')
        data = {
            'email': 'invalidemail',
            'password': 'pass!@#QAZ'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_collaborator_signup_invalid_password(self):
        """ Test to ensure that the password is valid. """
        url = reverse('collaborators:v1_signup')
        data = {
            'email': 'validmail@collabshare.dev',
            'password': 'a',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_collaborator_signup_successful_but_not_verified_email(self):
        """ Test to ensure that the collaborator signup is successful. """
        url = reverse('collaborators:v1_signup')
        data = {
            'email': 'validmail@collabshare.dev',
            'password': 'ValidPa$$w0rd',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['data']['email'], data['email'])
        collaborator = get_user_model().objects.get(email=data['email'])
        self.assertFalse(collaborator.is_email_verified)

    
    def test_collaborator_signup_email_serializer(self):
        """ Ensure collaborator signup by email serializer return expected JSON data.""" 
        collaborator = get_user_model().objects.create(
            email='test@collabshare.dev',
            password='Pas$W0rd'
        )
        serializer = CollaboratorSignupEmailSerializer(collaborator)
        expected_data = {
            'email': 'test@collabshare.dev',
        }
        self.assertEqual(serializer.data, expected_data)
        collaborator.delete()

    def test_duplicate_email_signup_returns_failure(self):
        """ Test to see if duplicate email is allowed."""
        data = { 
            "email":'test@collabshare.dev',
            "password":'PASSW0rd$'
        }
        url = reverse('collaborators:v1_signup')
        response = self.client.post(url, data, format='json')
        # first signup is allowed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # second signup with the same email is not allowed
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
