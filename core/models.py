from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os
import json
def update_json_file_from_db():
    """Fetch latest vehicle data from the database and update alerts.json"""
    json_file_path = os.path.join(os.path.dirname(__file__), "alerts.json")

    # Get the latest vehicle data (assuming only one row exists)
    vehicle_data = VehicleData.objects.first()
    if vehicle_data:
        data = {
            "battery_percentage": vehicle_data.battery_percentage,
            "battery_temperature": vehicle_data.battery_temperature,
            "cng_pressure": vehicle_data.cng_pressure,
            "cng_temperature": vehicle_data.cng_temperature,
            "gas_leak_detected": vehicle_data.gas_leak_detected,
        }

        # Write to JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

# 🚀 Custom User Manager
class CustomerManager(BaseUserManager):
    def create_user(self, name, mobile, email, vehicle_type, vehicle_number, fuel_type, password=None):
        """Creates and saves a regular customer"""
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        customer = self.model(
            name=name,
            mobile=mobile,
            email=email,
            vehicle_type=vehicle_type,
            vehicle_number=vehicle_number,
            fuel_type=fuel_type
        )

        if password:
            customer.set_password(password)  # ✅ Hash Password
        customer.save(using=self._db)
        return customer

    def create_superuser(self, name, mobile, email, vehicle_type, vehicle_number, fuel_type, password):
        """Creates and saves a superuser"""
        customer = self.create_user(name, mobile, email, vehicle_type, vehicle_number, fuel_type, password)
        customer.is_admin = True
        customer.is_staff = True
        customer.is_superuser = True
        customer.save(using=self._db)
        return customer

# 🚗 Customer Model
class Customer(AbstractBaseUser):
    FUEL_CHOICES = [
        ('CNG', 'CNG'),
        ('Battery', 'Battery')
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)  # Removed `unique=True`
    email = models.EmailField(unique=True)
    vehicle_type = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)  # Removed `unique=True`
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # ✅ Required for admin access
    is_superuser = models.BooleanField(default=False)  # ✅ Required for superuser access

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'vehicle_type', 'vehicle_number', 'fuel_type']

    def __str__(self):
        return self.name

    # ✅ Required Permissions for Admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class EVStation(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    slots = models.IntegerField(default=0)
class VehicleData(models.Model):
    battery_percentage = models.IntegerField(default=100)
    battery_temperature = models.FloatField(default=30.0)
    cng_pressure = models.FloatField(default=10.0)
    cng_temperature = models.FloatField(default=40.0)
    gas_leak_detected = models.BooleanField(default=False)

    def __str__(self):
        return f"Vehicle Data - Battery: {self.battery_percentage}% | CNG Pressure: {self.cng_pressure} bar"

    def save(self, *args, **kwargs):
        """ Save data to the database and update alerts.json file """
        super().save(*args, **kwargs)
        update_json_file_from_db()  # Update the JSON file