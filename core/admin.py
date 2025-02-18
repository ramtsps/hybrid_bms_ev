from django.contrib import admin
from .models import Customer ,EVStation,VehicleData
import os
import json
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'vehicle_type', 'vehicle_number', 'fuel_type')
    search_fields = ('name', 'email', 'vehicle_number')


admin.site.register(EVStation)

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

@admin.register(VehicleData)
class VehicleDataAdmin(admin.ModelAdmin):
    list_display = ("battery_percentage", "battery_temperature", "cng_pressure", "cng_temperature", "gas_leak_detected")
    list_display_links = ("battery_temperature",)  # Setting a clickable field
    list_editable = ("battery_percentage", "cng_pressure", "cng_temperature", "gas_leak_detected")  # Editable fields

    def save_model(self, request, obj, form, change):
        """ Update the JSON file when data is saved in admin """
        super().save_model(request, obj, form, change)
        update_json_file_from_db()  # Update alerts.json

    def delete_model(self, request, obj):
        """ Update the JSON file when a record is deleted """
        super().delete_model(request, obj)
        update_json_file_from_db()