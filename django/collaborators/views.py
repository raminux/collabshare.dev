from django.core.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CollaboratorSignupEmailSerializer

import logging

logger = logging.getLogger(__name__)


class CollaboratorSignupView(CreateAPIView):
    """ A class-based view to handle collaborator sign up."""

    serializer_class = CollaboratorSignupEmailSerializer

    def create(self, request, *args, **kwargs):
        """ Override create method of CreateAPIView to create a new collaborator instance, 
            generate JWT token, and store it in HttpOnly cookies. """
        # Check if email and password are provided
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Please provide both email and password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            collaborator = serializer.save()
            response = Response({'message': 'An email has been sent to verify your email address.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return response
        
        
        return Response({'error': 'Invalid serializer.'}, status=status.HTTP_400_BAD_REQUEST)