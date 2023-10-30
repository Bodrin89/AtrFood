from django.contrib import admin

from apps.library.models import City, Country, District, ManufacturingCompany, NameLevelLoyalty, PackageType, Region, \
    AddressArtFood, ContactArtFood, OpenStore


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(PackageType)
class PackageTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
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


class ContactArtFoodInline(admin.TabularInline):
    model = ContactArtFood
    extra = 1


class OpenStoreInline(admin.TabularInline):
    model = OpenStore
    extra = 1


@admin.register(AddressArtFood)
class AddressArtFoodAdmin(admin.ModelAdmin):
    inlines = [OpenStoreInline, ContactArtFoodInline]
