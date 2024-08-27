from django.contrib import admin
from store.models import Address


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name',
                    'address', 'zip_code', 'country_or_region']
    list_editable = ['zip_code']

    @admin.display(ordering='street_address1')
    def address(self, address):
        return f'{address.street_address1}, {address.city}'
