from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have an password")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_manager = False
        user.is_admin = False
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have an password")
        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_manager = False
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = 'email'  # username equals to email
    REQUIRED_FIELDS = []

    objects = UserManager()  # now can create user without username


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oem_part_number = models.CharField(max_length=12, db_index=True)
    brand = models.CharField(max_length=255) #reikes itraukti kategorijas
    manufacturer = models.CharField(max_length=255) #reikes itraukti kategorijas
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)  # can be nullable
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=150, blank=True, null=True)
    diameter = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    height = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    width = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    #attributes = models.JsonField(blank=True, null=True) #papildomi atributai


class Link(models.Model):
    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # on delete cascade
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
