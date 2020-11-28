from django.db import models
from real_state_backend.utils import upload_image


# Create your models here.
class State(models.Model):
    name = models.CharField(max_length=48)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=48)

    def __str__(self):
        return self.name


class Pincode(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return self.pincode


class NearBy(models.Model):
    place = models.CharField(max_length=20)
    distance = models.IntegerField(verbose_name='Distance (in KM.)', default=1)

    def __str__(self):
        return self.place


class Location(models.Model):
    locality = models.TextField()
    zip_code = models.ForeignKey(Pincode, on_delete=models.CASCADE)

    def __str__(self):
        return self.locality


class PropertyImages(models.Model):
    image = models.ImageField(
        verbose_name='Upload Property Image',
        upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.image)


class MeasurementUnit:
    SQ_FEET=1


MEASUREMENT_UNIT_CHOICES = [
    (MeasurementUnit.SQ_FEET, 'Square Feet')
]

class Property(models.Model):
    unique_id = models.CharField(max_length=10)
    description = models.TextField()
    size = models.IntegerField(default=50)
    measurement = models.IntegerField(choices=MEASUREMENT_UNIT_CHOICES, default=MeasurementUnit.SQ_FEET)
    bhk = models.IntegerField(default=1)
    est_price = models.IntegerField(default=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    images = models.ManyToManyField(PropertyImages, blank=True)
    thumbnail_image = models.ForeignKey(PropertyImages, related_name='thum', null=True, blank=True, on_delete=models.CASCADE)
    nearby = models.ManyToManyField(NearBy, blank=True)

    def __str__(self):
        return self.unique_id


class PropertyReview(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    number = models.CharField(max_length=10)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=1)
    date_joined = models.DateField(verbose_name='date of query', auto_now_add=True)

    def __str__(self):
        return self.name


class CustomerQuery(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    property_id = models.CharField(max_length=20, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    date_query = models.DateField(verbose_name='date of query', auto_now_add=True)

    def __str__(self):
        return self.name
