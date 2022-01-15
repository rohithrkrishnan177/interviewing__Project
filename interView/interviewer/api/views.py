from rest_framework.views import APIView
from .serializers import interviewerRegistrationSerializer, interviewerProfileSerializer, interviewerAppointmentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
# from interviewer.models import inter_viewer
# from cantidate.models import Appointment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# from rest_framework.permissions import BasePermission
from interviewer.models import inter_viewer
from cantidate.models import Appointment


# class IsInterviewer(BasePermission):
#     """custom Permission class for Interviewer"""
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.groups.filter(name='interviewer').exists())

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='interviewer').exists()
        if user.status==False:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif account_approval==False:
            return Response(
                {
                    'message': "You are not authorised to login as a Interviewer"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            },status=status.HTTP_200_OK)

class registrationView(APIView):

    def post(self, request, format=None):
        registrationSerializer = interviewerRegistrationSerializer(
            data=request.data.get('user_data'))
        profileSerializer = interviewerProfileSerializer(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            interviewer = registrationSerializer.save()
            profileSerializer.save(user=interviewer)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class interviewerProfileView(APIView):
    def get(self, request, format=None):
        user = request.user
        profile = inter_viewer.objects.filter(user=user).get()
        userSerializer=interviewerRegistrationSerializer(user)
        profileSerializer = interviewerProfileSerializer(profile)
        return Response({
            'user_data':userSerializer.data,
            'profile_data':profileSerializer.data

        }, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = request.user
        profile = inter_viewer.objects.filter(user=user).get()
        profileSerializer = interviewerProfileSerializer(
            instance=profile, data=request.data.get('profile_data'), partial=True)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({
                'profile_data':profileSerializer.data
            }, status=status.HTTP_200_OK)
        return Response({
                'profile_data':profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

class interviewerAppointmentView(APIView):
    # permission_classes = [IsInterviewer]

    def get(self, request, format=None):
        user = request.user
        user_interviewer = inter_viewer.objects.filter(user=user).get()
        appointments=Appointment.objects.filter(interviewer=user_interviewer, status=True).order_by('appointment_date', 'appointment_time')
        appointmentSerializer=interviewerAppointmentSerializer(appointments, many=True)
        return Response(appointmentSerializer.data, status=status.HTTP_200_OK)