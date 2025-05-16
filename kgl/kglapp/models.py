
from django.db import models
from datetime import datetime


# Borrowing the functionality of extending in built django user from django.
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


##################################################
# List of tables.
# User table ( name, email, address, gender, phone, number; roles(salesagent, manager and owner))
# Sales table (Product_name, price, quantity, category, customer_name, date, salesagent)
# Stock table (product_name, product_quantity, cost, type_of_stock, supplier_name, date)
# Usertable called userprofile using Abstructuser on line 3 above.
# This model is used to check who you a so as to redirect you.
class Userprofile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    username = models.CharField(max_length=100, unique=True)
    email =  models.EmailField(unique=True)
    address = models.CharField(max_length=100, blank=True)
    phonenumber = models.CharField(max_length=20, blank=False)
    gender = models.CharField(max_length=100, blank=True)
    
    
    # Override default reverse accessors to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="userprofile_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userprofile_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )
# This calls the obejects of the model by there names.
    def __str__(self):
        return self.username
    






######################################
## The Category model.
# This will determine the category of product that is entered.
# This will be inherited by the product model.

class Category(models.Model):
    category_name = models.CharField(max_length=255, blank=True)

# The model properties will be called by there name. using this function.
    def __str__(self):
        return self.category_name





######################################
## The product model.
# This will be for tracking what sales and reorder levels of every branch. 
# This will have a relationship with,
# Inventory
# Stock
# Creditsales. That will be inheriting from it.

class Product(models.Model):
    cat_name = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier_name = models.CharField(max_length=100, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    sku = models.CharField( max_length=255, blank=True, unique=True)
    buying_price = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True, blank=True)
    unit_price = models.IntegerField(blank=True, null=True, default=0,)
    type_of_stock = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    expiry_date = models.DateField()

# This will call the properties of the model by there names.
    def __str__(self):
        return self.product_name





#######################################
## The Branch model.
# This will be for tracking what happens in the different branchs
# This will have a relationship with,
# Inventory
# Stock
# Creditsales. That will be inheriting from it.

class Branch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    branch_name = models.CharField(max_length=50, null=True)
    contact = models.IntegerField(default=0, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

# This will call the properties of the model by there names.
    def __str__(self):
        return self.branch_name
    




#################################
## The inventory model, 
# This will be for real time tracking for the availability of a product at every branch.
# The inventory model will inheritance from.
# Product
# Branch.

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)    
    buying_price = models.IntegerField(blank=True, null=True, default=0,)
    unit_price = models.IntegerField(blank=True, null=True, default=0,)
    unite_of_measure = models.IntegerField(blank=True, null=True, default=0,)
    description = models.TextField(blank=True, null=True, default=0,)
    expiry_date = models.DateField()
    stock_quantity = models.IntegerField(blank=True, null=True, default=0,)
    reorder_level = models.PositiveIntegerField(blank=True, null=True, default=0,)

# This will prevent repetition of product and branch entry and only allow updates of the two.
    class Meta:
        unique_together = ('product', 'branch')

# Calling the model properties by there names and not default name of django. like numbers 1. using this function.
    def __str__(self):
        return self.product.product_name 




######################################
## The Customer model.
# This will be used to track the sales conducted on credit.
# This model will be inherited by by credit sales only. 
# Creditsale

class Customer(models.Model):
    full_names = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)

# Calling the data in the database there names.
    def __str__(self):
        return self.full_names
    




########################################
## The Creditsale model.
# This will be used to track the brach that transact a creditsale.
# This will have an inheritance from the.
# Customer
# Product
# Branch
# These a the choices that will be selected in the payment choices as you enter objects in the credisale module.

class Creditsale(models.Model):
    payment_choices = [
        ('Pending', 'Pending '),
        ('Patial', 'Patial payment'),
        ('Paid', 'Fully paid'),
        ('Overdue', 'Overdue'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.IntegerField(blank=True, null=True, default=0)
    total_price = models.IntegerField(blank=True, null=True, default=0)
    amount_paid = models.IntegerField(blank=True, null=True, default=0)
    balance_due = models.IntegerField(blank=True, null=True, default=0)
    
    sales_agent = models.ForeignKey(Userprofile, on_delete=models.SET_NULL, null=True)
    date_of_sale = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=payment_choices, default="Pending")

# Calling the data in the database there names.
    def __str__(self):
        return self.payment_status



##################################################################
## A class for the receipt to handle in pos sales. 
class Receipt(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.IntegerField(blank=True, null=True, default=0)
    total_price = models.IntegerField(blank=True, null=True, default=0)
    amount_paid = models.FloatField(default=10)  # Add this field
    balance = models.FloatField(default=10) 
    date_of_sale = models.DateField(default=datetime.now)

    # Calling the data in the database there names.
    def __str__(self):
        return self.product.product_name
