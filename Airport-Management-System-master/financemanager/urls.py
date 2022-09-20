from django.urls import path

from financemanager.reports import payments_report
from financemanager.views import financemanagerLoginView, LogoutView, FeedBackView, ChangePasswordView, ProfileView, \
    financemanagerSignUpView, HomeView, PaymentListView

urlpatterns = [
    path('payments-pdf/', payments_report, name="payments-pdf"),
    path('payments/', PaymentListView.as_view(), name="payments"),
    path('login/', financemanagerLoginView.as_view(), name="login"),
    path('register/', financemanagerSignUpView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name="index"),

]
