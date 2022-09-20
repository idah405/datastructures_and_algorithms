from django.urls import path

from .views import IndexView, AboutView, ContactView, ProfileView, clientLoginView, \
    clientSignUpView, VerifyEmail, log_out, Appointment_payment, appointment, faq, change_password, \
    success_page, receipts, FeedbackView, Appointment_api, cancel_Appointment, ClientServiceListView

urlpatterns = [
    path('logout/', log_out, name="logout"),
    path('verify/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify'),
    path('sign-up/', clientSignUpView.as_view(), name="sign_up"),
    path('login/', clientLoginView.as_view(), name="login"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('feedback/', FeedbackView.as_view(), name="feedback"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about_us"),
    path('cancel_appointment/<slug>/', cancel_Appointment, name="cancel_Appointment"),
    path('payment/<slug>/', Appointment_payment, name="payment"),
    path('Appointment_api/', Appointment_api, name="Appointment_api"),
    path('Appointment/', appointment, name="Appointment"),
    path('log_out/', log_out, name="log_out"),
    path('faq/', faq, name="faq"),
    path('ClientService/', ClientServiceListView.as_view(), name="ClientService"),
    path('change_password/', change_password, name="change_password"),
    path('success_page/<slug>/', success_page, name="success_page"),
    path('receipts/', receipts, name="receipts"),
    path('', IndexView.as_view(), name="index"),
]
