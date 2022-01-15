from .views import registrationView, CustomAuthToken, interviewerProfileView, interviewerAppointmentView
from django.urls import path


app_name='doctor'
urlpatterns = [
    path('registration/', registrationView.as_view(), name='api_interviewer_registration'),
    path('login/', CustomAuthToken.as_view(), name='api_interviewer_login'),
    path('profile/', interviewerProfileView.as_view(), name='api_interviewer_profile'),
    path('appointments/', interviewerAppointmentView.as_view(), name='api_interviewer_profile'),
]