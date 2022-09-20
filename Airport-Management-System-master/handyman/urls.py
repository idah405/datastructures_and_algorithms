from django.urls import path
#from django.contrib import admin
from .reports import Appointment_report, ClientService_report
from .views import IndexView, handymanLoginView, handymanSignUpView, LogoutView, ProfileView, \
    ChangePasswordView, FeedBackView,ClientServiceListView, AppointmentListView, ElectricianListView

urlpatterns = [
    path('ClientService-pdf/', ClientService_report, name="ClientService-pdf"),
    path('Appointment-pdf/', Appointment_report, name="Appointment-pdf"),
    path('ClientService/', ClientServiceListView.as_view(), name="ClientService"),
    path('Electrician/', ElectricianListView.as_view(), name="Electrician"),
    path('Appointment/', AppointmentListView.as_view(), name="Appointment"),
    path('login/', handymanLoginView.as_view(), name="login"),
    path('register/', handymanSignUpView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', IndexView.as_view(), name="index"),
]
