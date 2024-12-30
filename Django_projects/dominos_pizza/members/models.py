from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.conf import settings

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
    full_name = models.CharField(max_length=255,blank=True)
    bio = models.CharField(max_length=2024,blank=True)
    avatar = models.ImageField(upload_to='avatars/',blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __repr__(self):
        return f"<User_email={self.email},User_FName={self.full_name}>"
    class Meta:
        db_table = "users"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    caption = models.CharField(max_length=1024,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]

    def __repr__(self):
        return (f"<author={self.author}\n"
                f"images={self.images}\n"
                f"caption={self.caption[:30]}>")

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __repr__(self):
        return f"<Image_id={self.image}>"

class Like(models.Model):
    liked_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name= 'likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= 'likes')

    def __repr__(self):
        return  f"<Like user={self.user.email},post_id={self.post.primary_key},liked_at={self.liked_at}>"

class Tag(models.Model):
    title = models.CharField(max_length=100)
    def __repr__(self):
        return f"<Tag_title={self.title}>"

class PostTag(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post_tags')
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE,related_name='post_tags')
