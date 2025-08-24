"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    # PROVIDE KEYWORD ARGUMENT "**extra_field" WHICH
    # REALLY HELPS US TO CREATE NEW OTHER FIELDS  so not required to list as argument!
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # THIS ENABLES US TO ADDING MULTIPLE DATABASES

        return user

# FUNCTIONALITY FOR THE AUTHENTICATION SYSTEM = 'AbstractBaseUser'
# FUNCTIONALITY FOR THE PERMISSIONS & FIELDS = 'PermissionsMixin'
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() # ASSIGNING USER TO USERMANAGER

    USERNAME_FIELD = 'email'