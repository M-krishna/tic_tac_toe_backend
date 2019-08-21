from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    unique_name = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        db_table = 'User'


class ActivationLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=500)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        db_table = 'activation_link'
