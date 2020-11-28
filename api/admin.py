from django.contrib import admin
from api.models import State, City, Pincode, NearBy, Location, \
    PropertyImages, Property, PropertyReview, CustomerQuery


admin.site.register(State) 
admin.site.register(City) 
admin.site.register(Pincode) 
admin.site.register(NearBy) 
admin.site.register(Location)
admin.site.register(PropertyImages) 
admin.site.register(Property) 
admin.site.register(PropertyReview) 
admin.site.register(CustomerQuery)