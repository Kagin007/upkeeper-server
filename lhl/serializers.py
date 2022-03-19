from rest_framework import serializers
from .models import Member


class GetAllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model: Member
        fields = ['id', 'first_name', 'last_name', 'password', 'email', 'picture_url']

# class GetAllCleanersSerializer(serializers.ModelSerializer):


class GetMemberDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'role', 'pay_rate', 'location', 'user']


class PostMemberDataSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    location = serializers.PrimaryKeyRelatedField(many=False, queryset=Location.objects.all())

    class Meta:
        model = Member
        fields = ['id', 'role', 'pay_rate', 'location', 'user']


class GetPropertiesSerializer(serializers.ModelSerializer):
    member_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Member.objects.all())

    class Meta:
        model = Properties
        fields = ['address', 'city', 'country', 'longitude', 'latitude', 'member_id']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        # front end validates password
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

# user stories
# All Users
# should a user choose to be a owner or a cleaner at profile creation?
# As a user I want to create a profile
# As a user I would like to be see/write messages between cleaners and owners
# As a user (owners & cleaners) I can cancel appointments
# As a user I want to change appointment to different times

# Owner
# As a user want to book cleaners
# As an owner I would like to see list of cleaners without signing up
# As an owner I would like to rank cleaners that I have used (rate the cleaner just once per reservation)
# As an owner I would like to write reviews about cleaners I have used
# As an owner I would like to filter the available services provided by cleaners
# As a user I would like to book cleaners through the application and pay for services through their availability

# Cleaner
# As a cleaner I want to be able to post a profile with:
# Availabilities
# Rates$$
# Particular services
# Location (city)
# Photo
