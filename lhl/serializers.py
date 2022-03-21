from rest_framework import serializers
from django.contrib.auth.models import User
from lhl.models import Location, Member, Properties, Reservations, Ratings
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db.models import Avg, Count, Max


class GetUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class GetLocationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'address', 'city', 'province', 'longitude', 'latitude']


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


class GetReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['member_id', 'property_id', 'booking_date']


class GetReservationsByMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Member.objects.all())
    property_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Properties.objects.all())

    class Meta:
        model = Reservations
        fields = ['member_id', 'property_id', 'booking_date']


class GetRatings(serializers.ModelSerializer):
    member_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Member.objects.all())

    class Meta:
        model = Ratings
        fields = ['member_id', 'reservation_id', 'message', 'rating']


class GetRatingsByMemberSerializer(serializers.ModelSerializer):
    member_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Member.objects.all())
    reservation_id = serializers.PrimaryKeyRelatedField(many=False, queryset=Reservations.objects.all())
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()

    class Meta:
        model = Ratings
        fields = ['member_id', 'reservation_id', 'message', 'rating', 'average_rating', 'rating_count']

    def get_average_rating(self, obj):
        avg_rating = Ratings.objects.filter(member_id=obj.member_id).aggregate(Avg('rating'))
        return avg_rating

    def get_rating_count(self, obj):
        rating_count = Ratings.objects.filter(member_id=obj.member_id).count()
        return rating_count


class GetMemberDataSerializer(serializers.ModelSerializer):
    # extends the user table into Members
    user = GetUserDataSerializer(many=False, read_only=True)
    location = GetLocationDataSerializer(many=False, read_only=True)
    top_rating = serializers.SerializerMethodField()
    # rating = serializers.PrimaryKeyRelatedField(many=False, queryset=Ratings.objects.all())

    class Meta:
        model = Member
        fields = ['id', 'role', 'pay_rate', 'location', 'user', 'top_rating']

    def get_top_rating(self, obj):
        top_rating = Ratings.objects.filter(member_id_id=obj.id).aggregate((Max('rating')))
        return top_rating



# avg = Ratings.objects.filter(member_id_id=memberid).aggregate(avg=Avg('rating'))

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
