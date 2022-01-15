from .views import (
    CustomAuthToken,
    interviewerAccountViewAdmin,
    interviewerregistrationViewAdmin,
    approveInterviewerViewAdmin,
    appointmentViewAdmin,
    cantidateRegistrationViewAdmin,
    cantidateAccountViewAdmin,
    approveCantidateViewAdmin,
    approveAppointmentViewAdmin,
)

from django.urls import path

app_name = 'hr'
urlpatterns = [
    # Admin login
    path('login/', CustomAuthToken.as_view(), name='api_admin_login'),

    # Approve interviewer
    path('approve/interviewer/', approveInterviewerViewAdmin.as_view(), name='api_interviewer_approve_admin'),
    path('approve/interviewer/<uuid:pk>/', approveInterviewerViewAdmin.as_view(), name='api_interviewer_detail_approve_admin'),

    # Approve Cantidate
    path('approve/cantidate/', approveCantidateViewAdmin.as_view(), name='api_cantidate_approve_admin'),
    path('approve/cantidate/<uuid:pk>/', approveCantidateViewAdmin.as_view(), name='api_cantidate_detail_approve_admin'),

    # Approve Appointment
    path('approve/appointments/', approveAppointmentViewAdmin.as_view(), name='api_appointment_approve_admin'),
    path('approve/appointment/<int:pk>', approveAppointmentViewAdmin.as_view(), name='api_appointment_approve_detail_admin'),

    # interviewer management
    path('interviewer/registration/', interviewerregistrationViewAdmin.as_view(), name='api_inetrviewerhr_registration_admin'),
    path('interviewer/', interviewerAccountViewAdmin.as_view(), name='api_interviewerhr_admin'),
    path('interviewer/<uuid:pk>/', interviewerAccountViewAdmin.as_view(), name='api_interviewerhr_detail_admin'),

    # Cantidate Management
    path('cantidate/registration/', cantidateRegistrationViewAdmin.as_view(), name='api_cantidate_registration_admin'),
    path('cantidate/', cantidateAccountViewAdmin.as_view(), name='api_Cantidate_admin'),
    path('cantidate/<uuid:pk>/', cantidateAccountViewAdmin.as_view(), name='api_cantidate_detail_admin'),

    # Appointment Management
    path('appointments/', appointmentViewAdmin.as_view(), name='api_appointments_admin'),
    path('appointment/<int:pk>/', appointmentViewAdmin.as_view(), name='api_appointment_detail_admin'),

]