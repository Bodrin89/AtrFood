from django.contrib import admin

from apps.library.models import City, Region, District, ManufacturingCompany, ManufacturingCountry


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    pass


@admin.register(ManufacturingCompany)
class ManufacturingCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(ManufacturingCountry)
class ManufacturingCountryAdmin(admin.ModelAdmin):
    pass
