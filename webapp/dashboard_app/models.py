from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10) 
    email_id = models.CharField(max_length=100, unique=True) #add @something check
    password = models.CharField(max_length=100) # hashed value
    description = models.CharField(max_length = 100)
    active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)