from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Customer,EVStation
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import json
import os
from django.http import JsonResponse
from .models import VehicleData
from django.views.decorators.csrf import csrf_exempt


# request.session["battery_percentage"] = 10
# request.session["battery_temperature"] = 30
# request.session["cng_pressure"] = 9
# request.session["cng_temperature"] = 51
# request.session["gas_leak_detected"] = True



def update_json_file_from_db():
    """ Update alerts.json with the latest values from the database """
    json_file_path = os.path.join(settings.BASE_DIR, "alerts.json")

    # Fetch latest data from the database (assuming only one record exists)
    vehicle_data = VehicleData.objects.first()
    if vehicle_data:
        data = {
            "battery_percentage": vehicle_data.battery_percentage,
            "battery_temperature": vehicle_data.battery_temperature,
            "cng_pressure": vehicle_data.cng_pressure,
            "cng_temperature": vehicle_data.cng_temperature,
            "gas_leak_detected": vehicle_data.gas_leak_detected
        }

        # Write to alerts.json
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

def update_session_from_json(request):
    """ Update session data from alerts.json file """
    json_file_path = os.path.join(os.path.dirname(__file__), "alerts.json")
    
    # Check if the file exists
    if os.path.exists(json_file_path):
        # Read the JSON file
        with open(json_file_path, "r") as file:
            vehicle_data = json.load(file)

        # Update session with the values from the JSON file
        request.session["battery_percentage"] = vehicle_data.get("battery_percentage", 50)
        request.session["battery_temperature"] = vehicle_data.get("battery_temperature", 30)
        request.session["cng_pressure"] = vehicle_data.get("cng_pressure", 10)
        request.session["cng_temperature"] = vehicle_data.get("cng_temperature", 40)
        request.session["gas_leak_detected"] = vehicle_data.get("gas_leak_detected", False)

        request.session.modified = True  # Mark session as updated
        request.session.save()  




def set_vehicle_session(request):
    # Call the function to update session values based on alerts.json
    update_session_from_json(request)

    # Now the session is updated with the latest values from the JSON file
    return render(request, "core/new.html")

@csrf_exempt
def get_vehicle_data(request):
    """ API endpoint to return real-time vehicle data from alerts.json """

    # Update session from alerts.json file
    update_session_from_json(request)

    # Fetch session data and return it as a response
    vehicle_data = {
        "battery_percentage": request.session.get("battery_percentage", 50),
        "battery_temperature": request.session.get("battery_temperature", 30),
        "cng_pressure": request.session.get("cng_pressure", 10),
        "cng_temperature": request.session.get("cng_temperature", 40),
        "gas_leak_detected": request.session.get("gas_leak_detected", False),
    }

    return JsonResponse(vehicle_data)
# Home Page
def home(request):
    return render(request, 'core/home.html')
def dashboard(request):
    if "customer_id" not in request.session:
        messages.error(request, "❌ Please log in first!")
        return redirect("login")

    # Retrieve customer details from session
    customer_name = request.session.get("customer_name", "User")
    customer_email = request.session.get("customer_email", "")
    customer_mobile = request.session.get("customer_mobile", "")
    customer_vehicle_type = request.session.get("customer_vehicle_type", "")
    customer_vehicle_number = request.session.get("customer_vehicle_number", "")
    customer_fuel_type = request.session.get("customer_fuel_type", "")

 
    update_session_from_json(request)   
    battery_percentage = request.session.get("battery_percentage" )  # Default value for battery percentage
    battery_temperature = request.session.get("battery_temperature") 
    cng_level = request.session.get("cng_pressure")  # Default value for CNG level
    cng_efficiency = request.session.get("cng_temperature") 
    gas_leakage = request.session.get("gas_leak_detected", False) 
    # Assign chart data based on fuel type
    if customer_fuel_type == "Battery":
        fuel_chart_labels = ["Battery Usage", "Temperature Stability"]
        fuel_chart_data = [battery_percentage, battery_temperature]
        fuel_chart_colors = ["rgba(75, 192, 192, 0.7)", "rgba(255, 99, 132, 0.7)"]
        performance_label = "Battery Performance"
        performance_data = [80, 85, 78, 90, 75, 88]
    else:  # CNG Vehicle
        fuel_chart_labels = ["CNG Usage", "Efficiency"]
        fuel_chart_data = [cng_level, cng_efficiency]
        fuel_chart_colors = ["rgba(255, 159, 64, 0.7)", "rgba(54, 162, 235, 0.7)"]
        performance_label = "CNG Efficiency"
        performance_data = [60, 65, 70, 75, 78, 80]

    return render(
        request,
        "core/dashboard.html",
        {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_mobile": customer_mobile,
            "customer_vehicle_type": customer_vehicle_type,
            "customer_vehicle_number": customer_vehicle_number,
            "customer_fuel_type": customer_fuel_type,
            "battery_percentage": battery_percentage,
            "battery_usage": 100-battery_percentage,
            "battery_temperature": battery_temperature,
            "cng_level": cng_level,
            "cng_efficiency": cng_efficiency,
            "gas_leakage": gas_leakage,
            "fuel_chart_labels": fuel_chart_labels,
            "fuel_chart_data": fuel_chart_data,
            "fuel_chart_colors": fuel_chart_colors,
            "performance_label": performance_label,
            "performance_data": performance_data,
        },
    )

def stations(request):
    # Get the search term from the request
    search_term = request.GET.get('search', '').lower()

    # Query the database for stations
    if search_term:
        filtered_stations = EVStation.objects.filter(
            name__icontains=search_term
        ) | EVStation.objects.filter(location__icontains=search_term)
    else:
        filtered_stations = EVStation.objects.all()

    # Pagination (Show 4 stations per page)
    paginator = Paginator(filtered_stations, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/stations.html', {'page_obj': page_obj, 'search_term': search_term})
def alerts(request):
    update_session_from_json(request)
    fuel_type = request.session.get("customer_fuel_type", "Battery")  # Default to Battery
    print("🚗 Detected Fuel Type:", fuel_type)  # Debug print

    # Mock data for battery percentage, temperature, and CNG pressure and temperature
    battery_percentage = request.session.get("battery_percentage", 25)  # Set battery percentage
    battery_temperature = request.session.get("battery_temperature", 45)  # Set battery temperature
    cng_pressure = request.session.get("cng_pressure", 5)  # Set CNG pressure (in bar)
    cng_temperature = request.session.get("cng_temperature", 55)  # Set CNG temperature (in °C)
    gas_leak_detected = request.session.get("gas_leak_detected", True)  # Gas leak detection status

    print("⚡ Battery Percentage:", battery_percentage)
    print("🔥 Battery Temperature:", battery_temperature)
    print("⛽ CNG Pressure:", cng_pressure)
    print("🔥 CNG Temperature:", cng_temperature)
    print("🚨 Gas Leak Detected:", gas_leak_detected)

    # Fetch alerts from JSON file
    alert_messages = []

    # Ensure alerts are not duplicated
    alert_titles = set()  # A set to track alert titles that have already been added

    # Check and trigger alerts based on battery conditions
    if fuel_type == "Battery":
        if battery_percentage < 30 and "Low Battery Alert!" not in alert_titles:
            alert_messages.append({
                "type": "warning",
                "icon": "⚡",
                "title": "Low Battery Alert!",
                "message": f"Your vehicle’s battery is below {battery_percentage}%. Please charge soon."
            })
            alert_titles.add("Low Battery Alert!")

        if battery_temperature > 40 and "Overheating Detected!" not in alert_titles:
            alert_messages.append({
                "type": "danger",
                "icon": "🔥",
                "title": "Overheating Detected!",
                "message": f"Your battery temperature is {battery_temperature}°C. Please cool it down."
            })
            alert_titles.add("Overheating Detected!")

        if battery_percentage == 100 and "Battery Fully Charged!" not in alert_titles:
            alert_messages.append({
                "type": "info",
                "icon": "🔋",
                "title": "Battery Fully Charged!",
                "message": "Your battery is now 100% charged. Unplug to prevent overcharging."
            })
            alert_titles.add("Battery Fully Charged!")

    # Check and trigger alerts based on CNG conditions
    if fuel_type == "CNG":
        if gas_leak_detected and "Gas Leak Detected!" not in alert_titles:
            alert_messages.append({
                "type": "danger",
                "icon": "🚨",
                "title": "Gas Leak Detected!",
                "message": "Immediate action required. There is a detected gas leak."
            })
            alert_titles.add("Gas Leak Detected!")

        if cng_pressure < 10 and "Low CNG Pressure!" not in alert_titles:
            alert_messages.append({
                "type": "warning",
                "icon": "⛽",
                "title": "Low CNG Pressure!",
                "message": f"CNG pressure is below {cng_pressure} bar. Pressure levels are below recommended limits."
            })
            alert_titles.add("Low CNG Pressure!")

        if cng_temperature > 50 and "High Temperature in CNG Tank!" not in alert_titles:
            alert_messages.append({
                "type": "warning",
                "icon": "🔥",
                "title": "High Temperature in CNG Tank!",
                "message": f"CNG tank temperature is {cng_temperature}°C. Please inspect."
            })
            alert_titles.add("High Temperature in CNG Tank!")

    # Store alerts in session
    request.session["vehicle_alerts"] = alert_messages

    print("🚨 Retrieved Alerts:", alert_messages)  # Debug print
    return render(request, "core/alerts.html", {"fuel_type": fuel_type, "alert_messages": alert_messages})

def api_alerts(request):
    update_session_from_json(request)

    fuel_type = request.session.get("customer_fuel_type", "Battery")  
    battery_percentage = request.session.get("battery_percentage", 25)  
    battery_temperature = request.session.get("battery_temperature", 45)  
    cng_pressure = request.session.get("cng_pressure", 5)  
    cng_temperature = request.session.get("cng_temperature", 55)  
    gas_leak_detected = request.session.get("gas_leak_detected", True)  

    alert_messages = []

    if fuel_type == "Battery":
        if battery_percentage < 30:
            alert_messages.append({
                "type": "warning",
                "icon": "⚡",
                "title": "Low Battery Alert!",
                "message": f"Your vehicle’s battery is below {battery_percentage}%. Please charge soon."
            })

        if battery_temperature > 40:
            alert_messages.append({
                "type": "danger",
                "icon": "🔥",
                "title": "Overheating Detected!",
                "message": f"Your battery temperature is {battery_temperature}°C. Please cool it down."
            })

    if fuel_type == "CNG":
        if gas_leak_detected:
            alert_messages.append({
                "type": "danger",
                "icon": "🚨",
                "title": "Gas Leak Detected!",
                "message": "Immediate action required. There is a detected gas leak."
            })

        if cng_pressure < 10:
            alert_messages.append({
                "type": "warning",
                "icon": "⛽",
                "title": "Low CNG Pressure!",
                "message": f"CNG pressure is below {cng_pressure} bar. Please refill."
            })
        if cng_temperature > 50:
            alert_messages.append({
                "type": "warning",
                "icon": "🔥",
                "title": "High Temperature in CNG Tank!",
                "message": f"CNG tank temperature is {cng_temperature}°C. Please inspect."
            })
           
    return JsonResponse({"alerts": alert_messages})

def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]
        subject = f"New Contact Message from {name}"

        try:
            send_mail(subject, message, email, [settings.ADMIN_EMAIL])
            messages.success(request, "✅ Message sent successfully! We will get back to you soon.")
        except Exception as e:
            messages.error(request, "❌ Failed to send message. Please try again later.")

        return redirect("contact")

    return render(request, "core/contact.html")

def register_customer(request):
    if request.method == "POST":
        name = request.POST["name"]
        mobile = request.POST["mobile"]
        email = request.POST["email"]
        vehicle_type = request.POST["vehicle_type"]
        vehicle_number = request.POST["vehicle_number"]
        fuel_type = request.POST["fuel_type"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "❌ Passwords do not match!")
            return redirect("register")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "⚠️ Email is already registered!")
            return redirect("register")

        # ✅ Save customer with hashed password
        customer = Customer.objects.create_user(name, mobile, email, vehicle_type, vehicle_number, fuel_type, password1)

        messages.success(request, "✅ Registration successful! You can now log in.")
        return redirect("login")

    return render(request, "core/register.html")
from django.contrib.auth.hashers import check_password
def customer_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            customer = Customer.objects.get(email=email)

            # ✅ Check if password is correct
            if check_password(password, customer.password):
                request.session["customer_id"] = customer.id
                request.session["customer_name"] = customer.name
                request.session["customer_email"] = customer.email
                request.session["customer_mobile"] = customer.mobile
                request.session["customer_vehicle_type"] = customer.vehicle_type
                request.session["customer_vehicle_number"] = customer.vehicle_number
                request.session["customer_fuel_type"] = customer.fuel_type


                messages.success(request, "✅ Login successful!")
                return redirect("dashboard")  # Redirect to dashboard
            else:
                messages.error(request, "❌ Invalid email or password!")

        except Customer.DoesNotExist:
            messages.error(request, "❌ Email not found!")

    return render(request, "core/login.html")
# 🚪 Customer Logout
def customer_logout(request):
    request.session.flush()  # ✅ Clears all session data
    messages.success(request, "👋 Logged out successfully!")
    return redirect("login")
