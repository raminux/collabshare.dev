from django.core.validators import EmailValidator, validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class CollaboratorSignupEmailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'password', )
        extra_kwargs = {'password': {'write_only': True}}
    
    # def validate_email(self, email):
    #     """ Ensure the email is valid """
    #     msg = _('Please enter a valid email address')
    #     try:
    #         validate_email(email)
    #     except ValidationError:
    #         raise serializers.ValidationError(msg)
    #     return email 

    def validate_password(self, password):
        """ Validate the password using Django's password validators """
        validate_password(password)
        return password
    
    def create(self, validated_data):
        password = validated_data['password']
        # validated_data['password'] = make_password(password)
        collaborator = get_user_model().objects.create(**validated_data)
        return collaborator
    

    



    