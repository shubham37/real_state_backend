import random
import uuid
import datetime

from django.db.models import Q
from django.core.mail import EmailMessage

from rest_framework.views import  APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import State, City, Pincode, NearBy, Location, \
    PropertyImages, Property, PropertyReview, CustomerQuery
from api.serializers import PropertyReviewSerializer, PropertySerializer


class ContactView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        data = request.data.get('contactData')
        email = data.get('email','')
        if email:
            subject = "Query Recieved"
            body = "Hi,\n Our teM WILL contact you soon \n   \nThanks & Regards\n .."

            Email = EmailMessage(subject=subject, body=body, to=(email,))
            try:
                reponse = Email.send()
                query = CustomerQuery.objects.create(**data)
                return Response(data={'detail': 'Successfully Query Saved'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'detail':'Please Try again'}, status=status.HTTP_400_BAD_REQUEST)
        


class SearchView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request):
        query = request.GET.get('value','')
        if query:
            query_option = (
                    Q(location__zip_code__city__state__name__iexact=query) |
                    Q(location__zip_code__city__name__iexact=query) |
                    Q(location__zip_code__pincode__iexact=query) |
                    Q(location__locality__iexact=query)
                )
        bhk = int(request.GET.get('bhk',0))
        if bhk:
            bhk_option = (
                Q(bhk=bhk)
            )
        else:
            bhk_option = (
                Q(bhk__gt=0)
            )

        size = int(request.GET.get('size',0))
        if size:
            if size==1:
                size_option = (
                    Q(size__lt=1000)
                )
            elif size==2:
                size_option = (
                    Q(size__gte=1000), Q(size_lt=1500)
                )
            elif size==3:
                size_option = (
                    Q(size_gt=1500)
                )
        else:
            size_option = (
                Q(size__gt=0)
            )


        price = int(request.GET.get('price',0))
        if price:
            if price==1:
                price_option = (
                    Q(est_price__lt=100000)
                )
            elif price==2:
                price_option = (
                    Q(est_price__gte=100000), Q(est_price_lt=150000)
                )
            elif price==3:
                price_option = (
                    Q(est_price_gt=150000)
                )
        else:
            price_option = (
                Q(est_price__gt=0)
            )



        properties = Property.objects.filter(
            query_option, bhk_option, size_option, price_option
        )
        if properties:
            serialized = self.serializer_class(properties, many=True)
            return Response(data=serialized.data, status=status.HTTP_200_OK)
        return Response(data={'detail':'No Property'}, status=status.HTTP_204_NO_CONTENT)
        # return Response(data={'detail':'Please Try again'}, status=status.HTTP_400_BAD_REQUEST)


class PropertyView(APIView):

    permission_classes = (AllowAny,)
    serializer_class = PropertySerializer

    def get(self, request, prop_id):
        property_id = int(prop_id)
        if property_id:
            try:
                prop = Property.objects.get(id=property_id)
            except Exception as e:
                return Response(data={'error':e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            serialized = self.serializer_class(prop)
            return Response(data=serialized.data, status=status.HTTP_200_OK)                
        return Response(data={'detail':'Please Try again'}, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ViewSet):
    queryset = PropertyReview.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PropertyReviewSerializer

    def get_object(self, request, id):
        review = self.queryset.filter(id=id)
        return review

    # list address
    def list(self, request):
        reviewes = self.queryset.all()
        if reviewes.exists():
            serialize = self.serializer_class(reviewes, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail':"No Data"}, status=status.HTTP_204_NO_CONTENT)

    # Retreive aaddress
    def retrieve(self, request, pk=None):
        reviews = self.queryset.filter(prop_id=pk)
        if reviews.exists():
            serialized = self.serializer_class(reviews, many=True)
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response("Please Check uuid", status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=['POST'])
    def add_review(self, request, pk):
        prop_id = int(pk)
        data = request.data.get('reviewData')
        if data:
            data.update({'prop_id':prop_id})
            review = PropertyReview.objects.create(**data)
            return Response(data={'detail':'Added Successfully'}, status=status.HTTP_201_CREATED)
        return Response("Please Try Again", status=status.HTTP_204_NO_CONTENT)

