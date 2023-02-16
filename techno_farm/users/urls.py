from django.urls import path
from django.contrib.auth import views as auth_views

from .views import SignupView, LoginView, LogoutView, AddFarmerView, UpdateFarmerView, MyProfileView, SearchFarmerView, DeleteFarmerView

urlpatterns = [
    path('signup', SignupView.as_view(), name='signup-view'),
    path('login', LoginView.as_view(), name='login-view'),
    path('logout', LogoutView.as_view(), name='logout-view'),
    path('new/farmer', AddFarmerView.as_view(), name='new-farmer-view'),
    path('update/profile', UpdateFarmerView.as_view(), name='update-profile-view'),
    path('my/profile', MyProfileView.as_view(), name='my-profile-view'),
    path('get/farmer', SearchFarmerView.as_view(), name='search-farmer-view'),
    path('delete/farmer/<int:farmer_id>', DeleteFarmerView.as_view(), name='Delete-farmer-view'),
]