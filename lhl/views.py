from rest_framework.views import APIView
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from lhl.models import Member, Location, Properties, Reservations, Ratings
from lhl.serializers import GetUserDataSerializer, GetLocationDataSerializer, GetMemberDataSerializer, \
    GetPropertiesSerializer, RegisterSerializer, PostMemberDataSerializer, GetReservationsSerializer, \
    GetReservationsByMemberSerializer, GetRatingsByMemberSerializer


class AllUsers(APIView):
    def get(self, request):
        data = Member.objects.all()
        serializer = GetMemberDataSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserData(APIView):
    if settings.DEBUG is False:
        permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        data = User.objects.filter(username=username)
        serializer = GetUserDataSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationData(APIView):
    if settings.DEBUG is False:
        permission_classes = (IsAuthenticated,)

    def get(self, request, userid):
        try:
            memberdata = Member.objects.get(user_id=userid)
            try:
                locationdata = Location.objects.get(id=memberdata.location_id)
                serializer = GetLocationDataSerializer(locationdata)
                locations = serializer.data
            except Location.DoesNotExist:
                locations = []
                return Response(locations, status=status.HTTP_400_BAD_REQUEST)
        except Member.DoesNotExist:
            locations = []
            return Response(locations, status=status.HTTP_400_BAD_REQUEST)
        return Response(locations, status=status.HTTP_200_OK)

    def post(self, request):
        # deserialize the json into objects to put into database
        serializer = GetLocationDataSerializer(data=request.data)
        # checks for valid form
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMember(APIView):
    if settings.DEBUG is False:
        permission_classes = (IsAuthenticated,)

    def get(self, request, userid):
        memberdata = Member.objects.get(user_id=userid)
        serializer = GetMemberDataSerializer(memberdata)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostMemberDataSerializer(data=request.data)
        # checks for valid form
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertiesData(APIView):
    if settings.DEBUG is False:
        permission_classes = (IsAuthenticated,)

    def get(self, request, userid):
        memberdata = Member.objects.get(user_id=userid)
        propertiesdata = Properties.objects.filter(member_id_id=memberdata.id)
        serializer = GetPropertiesSerializer(propertiesdata, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, userid):
        # deserialize the json into objects to put into database
        serializer = GetPropertiesSerializer(data=request.data)
        # checks for valid form
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationsData(APIView):
    def get(self, request):
        # memberdata = Member.objects.get(user_id=userid)
        data = Reservations.objects.all()
        serializer = GetReservationsSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
        # now need a serializer for reservation data


class MemberReservationsData(APIView):
    def get(self, request, memberid):
        memberdata = Member.objects.get(user_id=memberid)
        data = Reservations.objects.filter(member_id_id=memberdata.id)
        serializer = GetReservationsByMemberSerializer(data, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class RatingByCleaner(APIView):
    def get(self, request, memberid):
        memberdata = Member.objects.get(user_id=memberid)
        data = Ratings.objects.filter(member_id_id=memberdata.id).order_by('-rating')
        serializer = GetRatingsByMemberSerializer(data, many=True)

        return Response(serializer.data, status.HTTP_200_OK)


class TopRatingByCleaner(APIView):
    def get(self, request, memberid):
        memberdata = Member.objects.get(user_id=memberid)
        data = Ratings.objects.filter(member_id_id=memberdata.id).order_by('-rating')[:1]
        serializer = GetRatingsByMemberSerializer(data, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    # const
    # sampleData = [
    #     {
    #         firstName: "Winona",
    #         lastName: "Williams",
    #         imgURL:
    #             "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBwgu1A5zgPSvfE83nurkuzNEoXs9DMNr8Ww&usqp=CAU",
    #         payRate: 60,
    #         transportMode: "Vehicle",
    #         avgRating: 4.5,
    #         numRatings: 20,
    #         topReview: {
    #                        date: "Jan 23, 2022",
    #                        reviewerName: "James Dean",
    #                        rating: 5,
    #                        reviewMessage: `Winona is spectacular and very efficient at her job.We always use her
    #                 service to clean our apartment when we don't have time to do it
    #                        ourselves.She responds quickly and is always on time!`,
    # }