from django.db import models
from django.conf import settings
from utils.models import BaseOfModel


# Create your models here.
class Address(BaseOfModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='adressess')
    country_or_region = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state_province_region = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.user} , {self.street_address1}, {self.state_province_region}, {self.zip_code}, {self.country_or_region}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'