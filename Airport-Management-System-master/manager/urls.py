from django.urls import path

#from manager.reports import served_report
from manager.views import managerLoginView, LogoutView, FeedBackView, ChangePasswordView, ProfileView, \
    managerSignUpView, HomeView, servedListView 

urlpatterns = [
   # path('served-pdf/', served_report, name="served-pdf"),
    path('served/', servedListView.as_view(), name="served"),
    path('login/', managerLoginView.as_view(), name="login"),
    path('register/', managerSignUpView.as_view(), name="register"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
    path('feedback/', FeedBackView.as_view(), name="feedback"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('', HomeView.as_view(), name="index"),

]
