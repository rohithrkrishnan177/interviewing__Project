from cantidate.models import Appointment
from rest_framework import serializers
from account.models import User
from interviewer.models import inter_viewer
from django.contrib.auth.models import Group


class interviewerRegistrationSerializer(serializers.Serializer):
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
            status=False
        )
        user.set_password(validated_data['password'])
        user.save()
        group_interview, created = Group.objects.get_or_create(name='inter_viewer')
        group_interview.user_set.add(user)
        return user


class  interviewerProfileSerializer(serializers.Serializer):
    Team_Lead = 'TL'
    Senior_Developer = 'SD'
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

    def update(self, instance, validated_data):
        instance.department = validated_data.get('department', instance.department)
        instance.address = validated_data.get('address', instance.address)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.save()
        return instance

class interviewerAppointmentSerializer(serializers.Serializer):
    cantidate_name = serializers.SerializerMethodField('related_patient_name')
    cantidate_age = serializers.SerializerMethodField('related_patient_age')
    appointment_date = serializers.DateField(label="Appointment Date:", )
    appointment_time = serializers.TimeField(label="Appointment Time:")

    def related_cantidate_name(self, obj):
        return obj.cantidate_history.cantidate.get_name

    def related_cantidate_age(self, obj):
        return obj.cantidate_history.cantidate.age
