from rest_framework.views import APIView
from .serializers import (cantidateRegistrationSerializer,
                          cantidateProfileSerializer,
                          appointmentSerializerPatient)

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from cantidate.models import cantidate,Appointment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission


# class IsCantidate(BasePermission):
#     """custom Permission class for cantidate"""
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.groups.filter(name='cantidate').exists())


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='cantidate').exists()
        if user.status == False:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif account_approval == False:
            return Response(
                {
                    'message': "You are not authorised to login as a Cantidate"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            }, status=status.HTTP_200_OK)


class registrationView(APIView):
    def post(self, request, format=None):
        registrationSerializer = cantidateRegistrationSerializer(
            data=request.data.get('user_data'))
        profileSerializer = cantidateProfileSerializer(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            patient = registrationSerializer.save()
            profileSerializer.save(user=patient)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class cantidateProfileView(APIView):
    def get(self, request, format=None):
        user = request.user
        profile = cantidate.objects.filter(user=user).get()
        userSerializer = cantidateRegistrationSerializer(user)
        profileSerializer = cantidateProfileSerializer(profile)
        return Response({
            'user_data': userSerializer.data,
            'profile_data': profileSerializer.data

        }, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = request.user
        profile = cantidate.objects.filter(user=user).get()
        profileSerializer = cantidateProfileSerializer(
            instance=profile, data=request.data.get('profile_data'), partial=True)
        if profileSerializer.is_valid():
            profileSerializer.save()
            return Response({
                'profile_data': profileSerializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'profile_data': profileSerializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)




class appointmentViewPatient(APIView):
    def get(self, request, pk=None, format=None):
        user = request.user
        user_cantidate = cantidate.objects.filter(user=user).get()
        history = user_cantidate.objects.filter(cantidate=user_cantidate).latest('admit_date')
        appointment = Appointment.objects.filter(status=True, cantidate_history=history)
        historySerializer = appointmentSerializerPatient(appointment, many=True)
        return Response(historySerializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        user_cantidate = cantidate.objects.filter(user=user).get()
        history = user_cantidate.objects.filter(cantidate=user_cantidate).latest('admit_date')
        serializer = appointmentSerializerPatient(
            data=request.data)
        if serializer.is_valid():
            serializer.save(cantidate_history=history)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors
                        , status=status.HTTP_400_BAD_REQUEST)
