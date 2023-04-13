from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CollaboratorManager(BaseUserManager):
    def create_user(self, email=None, mobile=None, password=None, **extra_fields):
        if not (email or mobile):
            raise ValueError("Collaborators must have an email address or mobile number")

        email = self.normalize_email(email) if email else None
        mobile = self.normalize_mobile(mobile) if mobile else None
        collaborator = self.model(email=email, mobile=mobile, **extra_fields)
        collaborator.set_password(password)
        collaborator.save(using=self._db)
        return collaborator

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
    email = models.EmailField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True) 
    is_staff = models.BooleanField(default=False)


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

    class Meta:
        verbose_name = "Collaborator"
        verbose_name_plural = "Collaborators"

