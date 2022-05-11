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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    is_manager = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = 'email'  # username equals to email
    REQUIRED_FIELDS = []

    objects = UserManager()  # now can create user without username

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def revenue(self):
        orders = Order.objects.filter(user_id=self.pk, complete=True)
        return sum(o.manager_revenue for o in orders)


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    oem_part_number = models.CharField(max_length=12, db_index=True)

    # brand = models.CharField(max_length=50)  # reikes itraukti kategorijas
    # manufacturer = models.CharField(max_length=50)  # reikes itraukti kategorijas
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)  # SET_NULL blank=True,
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)  # SET_NULL
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)  # SET_NULL
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, null=True)  # can be nullable
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=150, blank=True, null=True)
    diameter = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    height = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    width = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    weight = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    # attributes = models.JsonField(blank=True, null=True) #papildomi atributai
    @property
    def manufacturer_name(self):
        if self.manufacturer:
            return Manufacturer.objects.filter(pk=self.manufacturer.id).first().name
        else:
            return ""

    @property
    def brand_name(self):
        if self.brand:
            return Brand.objects.filter(pk=self.brand.id).first().name
        else:
            return ""

    @property
    def category_name(self):
        if self.category:
            return Category.objects.filter(pk=self.category.id).first().name
        else:
            return ""

 #   @property
 #   def category_name(self):
   #     return Category.objects.filter(pk=self.category_new.id).first().name


class Link(models.Model):
    code = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # on delete CASCADE
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    transaction_id = models.CharField(max_length=255, null=True)  # stripe payment id
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True)  # connection with a user (ORDER SHOULDNT BE REMOVED)
    code = models.CharField(max_length=100)
    manager_email = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    zip = models.CharField(max_length=10, null=True)
    complete = models.BooleanField(default=False)  # default order is not complete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def manager_revenue(self):
        items = OrderItem.objects.filter(order_id=self.pk)
        return sum(i.manager_revenue for i in items)

    @property
    def order_price(self):
        items = OrderItem.objects.filter(order_id=self.pk)
        return sum(i.price for i in items)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    admin_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    manager_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
