from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    bio = models.CharField(max_length=2024)
    avatar = models.ImageField(upload_to='avatars/')

    class Meta:
        db_table = "User"

