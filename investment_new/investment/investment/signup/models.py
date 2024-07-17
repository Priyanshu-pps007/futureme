from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

# Create your models here.

class UserCopy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=25, null=True, blank=True)
    phone_number = models.IntegerField(unique=True, null=True, blank=True)
    upi_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    username = models.CharField(max_length=25, unique=True)
    deposit= models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    withdraw=models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00, blank=True)
    coin = models.IntegerField(default=0, null=True, blank=True)
    invitational_code = models.CharField(max_length=20, null=True, blank=True)

    ifsc = models.CharField(max_length=50, unique=True, null=True, blank=True)
    account_holder = models.CharField(max_length=50, null=True, blank=True)
    account_number = models.IntegerField(null=True,blank=True)

    # email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username
    
class Plan(models.Model):
    PLANS = [
        ('D', 'Daily'),
        ('W', 'Weekly'),
        ('M', 'Monthly')
    ]
    name = models.CharField(max_length=30, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    daily = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True, choices=PLANS)

    def __str__(self):
        return self.name
    
class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposits', null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    upi_id = models.CharField(max_length=50)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    daily = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default = False)

    def __str__(self):
        return f"Deposit of {self.amount} from {self.user.username}"

    class Meta:
        ordering = ['-timestamp']


class QRCode(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    upi_id = models.CharField(max_length=50)
    coin = models.IntegerField(null=True, blank=True)
    amount = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default = False)

    def __str__(self):
        if(self.amount is not None):
            return f"Withdrawal of ₹{self.amount} for {self.user.username}"
        else:
            return f"Withdrawal of {self.coin} coins for {self.user.username}"
        