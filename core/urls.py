from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('monitoring/', views.dashboard, name='dashboard'),
    path('stations/', views.stations, name='stations'),
    path('alerts/', views.alerts, name='alerts'),
    path("register/", views.register_customer, name="register"),
    path("login/", views.customer_login, name="login"),
    path("logout/", views.customer_logout, name="logout"),
     path("contact/", views.contact, name="contact"),
     path("test/", views.set_vehicle_session, name="test"),
    path('api/vehicle-data/', views.get_vehicle_data, name='get_vehicle_data'),
    path('api/alerts/', views.api_alerts, name="api_alerts"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
