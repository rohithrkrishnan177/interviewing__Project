from rest_framework.exceptions import ValidationError
from cantidate.models import (Appointment,
                            cantidate_history)
from rest_framework import serializers
from account.models import User
from interviewer.models import inter_viewer
from django.contrib.auth.models import Group
from cantidate.models import cantidate


class interviewerRegistrationSerializerAdmin(serializers.Serializer):
    username = serializers.CharField(label='Username:')
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:', style={'input_type': 'password'}, write_only=True, min_length=8,
                                     help_text="Your password must contain at least 8 characters and should not be entirely numeric."
                                     )
    password2 = serializers.CharField(label='Confirm password:', style={'input_type': 'password'}, write_only=True)

    def validate_username(self, username):
        username_exists = User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username': 'This username already exists'})
        return username

    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        group_interviewer, created = Group.objects.get_or_create(name='interviewer')
        group_interviewer.user_set.add(user)
        return user


class interviewerRegistrationProfileSerializerAdmin(serializers.Serializer):
    Team_Lead = 'TL'
    Senior_Developer = 'DL'
    Manager = 'MC'
    department = serializers.ChoiceField(label='Department:', choices=[(Team_Lead, 'Team_Lead'),
                                                                       (Senior_Developer, 'Senior_Developer'),
                                                                       (Manager,
                                                                        'Manager')
                                                                       ])
    address = serializers.CharField(label="Address:")
    mobile = serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit() == False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile

    def create(self, validated_data):
        interviewer = inter_viewer.objects.create(
            department=validated_data['department'],
            address=validated_data['address'],
            mobile=validated_data['mobile'],
            user=validated_data['user']
        )
        return interviewer


class interviewerProfileSerializerAdmin(serializers.Serializer):
    Team_Lead = 'TL'
    Senior_Developer = 'DL'
    Manager = 'MC'
    department = serializers.ChoiceField(label='Department:', choices=[(Team_Lead, 'Team_Lead'),
                                                                       (Senior_Developer, 'Senior_Developer'),
                                                                       (Manager,
                                                                        'Manager')
                                                                       ])
    address = serializers.CharField(label="Address:")
    mobile = serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit() == False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile


class interviewerAccountSerializerAdmin(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(label='Username:', read_only=True)
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    status = serializers.BooleanField(label='status')
    interviewer = interviewerProfileSerializerAdmin(label='User')

    def update(self, instance, validated_data):
        try:
            interviewer_profile = validated_data.pop('interviewer')
        except:
            raise serializers.ValidationError("Please enter data related to interviewer's profile")

        profile_data = instance.interviewer

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        profile_data.department = interviewer_profile.get('department', profile_data.department)
        profile_data.address = interviewer_profile.get('address', profile_data.address)
        profile_data.mobile = interviewer_profile.get('mobile', profile_data.mobile)
        profile_data.save()
        return instance

class appointmentSerializerAdmin(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    appointment_date = serializers.DateField(label='Appointment date')
    appointment_time = serializers.TimeField(label='Appointement time')
    status = serializers.BooleanField(required=False)
    interviewer = serializers.PrimaryKeyRelatedField(queryset=inter_viewer.objects.all())

    def create(self, validated_data):
        new_appointment = Appointment.objects.create(
            appointment_date=validated_data['appointment_date'],
            appointment_time=validated_data['appointment_time'],
            status=True,
            interviewer=validated_data['interviewer']
        )
        return new_appointment

    def update(self, instance, validated_data):
        instance.appointment_date = validated_data.get('appointment_date', instance.appointment_date)
        instance.appointment_time = validated_data.get('appointment_time', instance.appointment_time)
        instance.status = validated_data.get('status', instance.status)
        instance.interviewer = validated_data.get('interviewer', instance.doctor)
        instance.save()
        return instance


class cantidateRegistrationSerializerAdmin(serializers.Serializer):
    username = serializers.CharField(label='Username:')
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    password = serializers.CharField(label='Password:', style={'input_type': 'password'}, write_only=True, min_length=8,
                                     help_text="Your password must contain at least 8 characters and should not be entirely numeric."
                                     )
    password2 = serializers.CharField(label='Confirm password:', style={'input_type': 'password'}, write_only=True)

    def validate_username(self, username):
        username_exists = User.objects.filter(username__iexact=username)
        if username_exists:
            raise serializers.ValidationError({'username': 'This username already exists'})
        return username

    def validate_password(self, password):
        if password.isdigit():
            raise serializers.ValidationError('Your password should contain letters!')
        return password

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError({'password': 'password must match'})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            status=True
        )
        user.set_password(validated_data['password'])
        user.save()
        group_cantidate, created = Group.objects.get_or_create(name='cantidate')
        group_cantidate.user_set.add(user)
        return user


class cantidateRegistrationProfileSerializerAdmin(serializers.Serializer):
    age = serializers.DecimalField(label="Age:", max_digits=4, decimal_places=1)
    address = serializers.CharField(label="Address:")
    mobile = serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit() == False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile

    def create(self, validated_data):
        new_patient = cantidate.objects.create(
            age=validated_data['age'],
            address=validated_data['address'],
            mobile=validated_data['mobile'],
            user=validated_data['user']
        )
        return new_cantidate


class cantidateProfileSerializerAdmin(serializers.Serializer):
    age = serializers.DecimalField(label="Age:", max_digits=4, decimal_places=1)
    address = serializers.CharField(label="Address:")
    mobile = serializers.CharField(label="Mobile Number:", max_length=20)

    def validate_mobile(self, mobile):
        if mobile.isdigit() == False:
            raise serializers.ValidationError('Please Enter a valid mobile number!')
        return mobile


class cantidateAccountSerializerAdmin(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(label='Username:', read_only=True)
    first_name = serializers.CharField(label='First name:')
    last_name = serializers.CharField(label='Last name:', required=False)
    status = serializers.BooleanField(label='status')
    cantidate = cantidateProfileSerializerAdmin(label='User')

    def update(self, instance, validated_data):
        try:
            cantidate_profile = validated_data.pop('cantidate')
        except:
            raise serializers.ValidationError("Please enter data related to cantidate's profile")

        profile_data = instance.cantidate

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        profile_data.age = cantidate_profile.get('age', profile_data.age)
        profile_data.address = cantidate_profile.get('address', profile_data.address)
        profile_data.mobile = cantidate_profile.get('mobile', profile_data.mobile)
        profile_data.save()

        return instance


