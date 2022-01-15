from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cantidate.models import Appointment
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from account.models import User
from .serializers import (interviewerAccountSerializerAdmin,
                          interviewerRegistrationSerializerAdmin,
                          interviewerRegistrationProfileSerializerAdmin,
                          appointmentSerializerAdmin,
                          cantidateRegistrationSerializerAdmin,
                          cantidateRegistrationProfileSerializerAdmin,
                          cantidateAccountSerializerAdmin)

from interviewer.models import inter_viewer


# class IsAdmin(BasePermission):
#     """custom Permission class for Admin"""
#
#     def has_permission(self, request, view):
#         return bool(request.user and request.user.groups.filter(name='admin').exists())


# Custom Auth token for Admin
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='HR').exists()
        if account_approval == False:
            return Response(
                {
                    'message': "You are not authorised to login as an admin"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)


class interviewerregistrationViewAdmin(APIView):
    def post(self, request, format=None):
        registrationSerializer = interviewerRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profileSerializer = interviewerRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            inter_viewer = registrationSerializer.save()
            profileSerializer.save(user=inter_viewer)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class interviewerAccountViewAdmin(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            interviewer_detail = self.get_object(pk)
            serializer = interviewerAccountSerializerAdmin(interviewer_detail)
            return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)
        all_interviewer = User.objects.filter(groups=1, status=True)
        serializer = interviewerAccountSerializerAdmin(all_interviewer, many=True)
        return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = interviewerAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('interviewer'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'interviewer': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class approveInterviewerViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            interviewer_detail = self.get_object(pk)
            serializer = interviewerAccountSerializerAdmin(interviewer_detail)
            return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)
        interviewer_detail = User.objects.filter(groups=1, status=False)
        serializer = interviewerAccountSerializerAdmin(interviewer_detail, many=True)
        return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = interviewerAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('interviewer'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'interviewer': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'interviewer': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Interviewer approval request with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class approveCantidateViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            interviewer_detail = self.get_object(pk)
            serializer = cantidateAccountSerializerAdmin(interviewer_detail)
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        all_patient = User.objects.filter(groups=2, status=False)
        serializer = cantidateAccountSerializerAdmin(all_patient, many=True)
        return Response({'cantidate': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = cantidateAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('cantidate'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'cantidate': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'cantidate': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "Cantidate approval request with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class appointmentViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = appointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=True)
        serializer = appointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = appointmentSerializerAdmin(
            data=request.data.get('appointments'))
        if serializer.is_valid():
            serializer.save()
            return Response({
                'appointments': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response({
            'appointments': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        saved_appointment = self.get_object(pk)
        serializer = appointmentSerializerAdmin(
            instance=saved_appointment, data=request.data.get('appointments'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'appointments': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_appointment = self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class approveAppointmentViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            appointment_detail = self.get_object(pk)
            serializer = appointmentSerializerAdmin(appointment_detail)
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        all_appointment = Appointment.objects.filter(status=False)
        serializer = appointmentSerializerAdmin(all_appointment, many=True)
        return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_appointment = self.get_object(pk)
        serializer = appointmentSerializerAdmin(
            instance=saved_appointment, data=request.data.get('appointments'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'appointments': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'appointments': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_appointment = self.get_object(pk)
        saved_appointment.delete()
        return Response({"message": "Appointment with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)


class cantidateRegistrationViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def post(self, request, format=None):
        registrationSerializer = cantidateRegistrationSerializerAdmin(
            data=request.data.get('user_data'))
        profileSerializer = cantidateRegistrationProfileSerializerAdmin(
            data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            cantidate = registrationSerializer.save()
            profileSerializer.save(user=cantidate)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class cantidateAccountViewAdmin(APIView):
    # permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):

        if pk:
            patient_detail = self.get_object(pk)
            serializer = cantidateAccountSerializerAdmin(patient_detail)
            return Response({'patients': serializer.data}, status=status.HTTP_200_OK)
        all_cantidate = User.objects.filter(groups=2, status=True)
        serializer = cantidateAccountSerializerAdmin(all_cantidate, many=True)
        return Response({'cantidate': serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        saved_user = self.get_object(pk)
        serializer = cantidateAccountSerializerAdmin(
            instance=saved_user, data=request.data.get('cantidate'), partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'cantidate': serializer.data}, status=status.HTTP_200_OK)
        return Response({
            'cantidate': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        saved_user = self.get_object(pk)
        saved_user.delete()
        return Response({"message": "User with id `{}` has been deleted.".format(pk)},
                        status=status.HTTP_204_NO_CONTENT)
