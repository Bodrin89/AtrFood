from django.contrib import admin

from apps.library.models import City, Country, District, ManufacturingCompany, NameLevelLoyalty, PackageType


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ManufacturingCompany)
class ManufacturingCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(NameLevelLoyalty)
class NameLevelLoyaltyAdmin(admin.ModelAdmin):
    pass
