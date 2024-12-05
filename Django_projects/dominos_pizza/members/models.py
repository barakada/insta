from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)




class User(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255,blank=True)
    bio = models.CharField(max_length=2024,blank=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = "users"

class Post(models.Model):
    pass


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    preview = models.ImageField(upload_to='previews/', null=True, blank=True)
