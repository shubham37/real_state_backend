from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

from api.views import ContactView, SearchView, PropertyView, ReviewViewSet

reviews_router = DefaultRouter()

urlpatterns = [
    url(r'^contact/', ContactView.as_view(), name='user_query_view'),
    url(r'^search/', SearchView.as_view(), name='search_property_view'),
    url(r'property/(?P<prop_id>[0-9]+)/', PropertyView.as_view(), name='property_view')
]

reviews_router.register('review', ReviewViewSet)

urlpatterns += reviews_router.urls
