import logging
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password 

logger = logging.getLogger(__name__)


class CollaboratorManager(BaseUserManager):
    """ Manager for Collaborators. """
    def create_user(self, email=None, mobile=None, password=None, **extra_fields):
        if not (email or mobile):
            raise ValueError("Collaborators must have an email address or mobile number")

        email = self.normalize_email(email) if email else None
        mobile = self.normalize_mobile(mobile) if mobile else None
        collaborator = self.model(email=email, mobile=mobile, **extra_fields)
        logger.info(collaborator.password)
        logger.info(password)
        collaborator.set_password(password)
        logger.info(collaborator.password)
        collaborator.save()
        return collaborator
    
    def create(self, email=None, mobile=None, password=None, **extra_fields):
        """ Creates and saves a new Collaborator with the given email, mobile and password. """
        return self.create_user(email, mobile, password, **extra_fields)

    def normalize_mobile(self, mobile):
        """
        Remove any non-digit characters from the mobile
        """
        return ''.join(filter(str.isdigit, mobile))

    def create_superuser(self, email=None, mobile=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email=email, mobile=mobile, password=password, **extra_fields)

class Collaborator(AbstractBaseUser, PermissionsMixin):
#     # It is recommended to store email addresses in encrypted
#     # TO DO: Check email encryption when saving Apple id or email?
    mobile = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_mobile_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True) 
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)


    LOGIN_EMAIL = "email"
    LOGIN_MOBILE = "mobile"
    LOGIN_GOOGLE = "google"
    LOGIN_APPLE = "apple"

    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_MOBILE, "Mobile"),
        (LOGIN_GOOGLE, "Google"),
        (LOGIN_APPLE, "Apple"),
    )

    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    # OAuth2 credentials (For Google or Apple Sign in)
    oauth2_id = models.CharField(max_length=100, null=True, blank=True)
    oauth2_access_token = models.CharField(max_length=200, null=True, blank=True)
    oauth2_refresh_token = models.CharField(max_length=200, null=True, blank=True)
    oauth2_expires_in = models.DateTimeField(null=True, blank=True)

    def set_oauth2_credentials(self, oauth2_id, access_token, refresh_token, expires_in):
        self.oauth2_id = oauth2_id
        self.oauth2_access_token = access_token
        self.oauth2_refresh_token = refresh_token
        self.oauth2_expires_in = expires_in
        self.save()

    objects = CollaboratorManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email or self.mobile

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_collabname(self): # collabname replaces username in traditional web 
        return self.email or self.mobile
    
    def create(self, email=None, mobile=None, password=None, **extra_fields):
        """ Creates and saves a new Collaborator with the given email, mobile and password. """
        return self.objects.create_user(email=email, mobile=mobile, password=password, **extra_fields)

    class Meta:
        verbose_name = "Collaborator"
        verbose_name_plural = "Collaborators"
    

