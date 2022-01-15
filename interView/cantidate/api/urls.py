from .views import (registrationView,
CustomAuthToken,
 cantidateProfileView,
 appointmentViewPatient)
from django.urls import path


app_name='cantidate'
urlpatterns = [
    path('registration/', registrationView.as_view(), name='api_cantidate_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_cantidate_login'),
    path('profile/', cantidateProfileView.as_view(), name='api_cantidate_profile'),
    path('appointment/', appointmentViewPatient.as_view(), name='api_cantidate_appointment')

]