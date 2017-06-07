from django.contrib import admin

from .models import Country
from .models import CountryDivision
from .models import CountryDivisionType
from .models import PostalZone


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [
                ('id',), ('iso2',), ('iso3',), ('isoN',), ('name',),
                ('fips',), ('continent',), ('tld',), ('currency_code',),
                ('phone_number_prefix',), ('phone_number_regex',),
                ('postal_code_format',), ('postal_code_regex',),
                ('geoname_id',)]
        }),
    ]
    list_display = ['id', 'iso2', 'iso3', 'name']
    ordering = ['iso3']
    search_fields = ['iso2', 'iso3', 'phone_number_prefix', '_name_localizations']


@admin.register(PostalZone)
class PostalZoneAdmin(admin.ModelAdmin):
    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('country',), ('code',)]
        }),
    ]
    list_display = ['id', 'country', 'code']
    list_filter = ['country']
    ordering = ['code']
    search_fields = ['code']


@admin.register(CountryDivisionType)
class CountryDivisionTypeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(CountryDivisionTypeAdmin, self).get_queryset(request)
        queryset = queryset.prefetch_related('country')

        return queryset

    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [('country',), ('code',), ('name',)]
        }),
    ]
    list_display = ['id', 'country', 'code', 'name']
    list_filter = ['country']
    ordering = ['code']
    search_fields = ['code', '_name_localizations']


@admin.register(CountryDivision)
class CountryDivisionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super(CountryDivisionAdmin, self).get_queryset(request)
        queryset = queryset.select_related('parent')
        queryset = queryset.prefetch_related(
            'postal_zone',
            'country_division_type',
            'country_division_type__country',
            'country')

        return queryset

    fieldsets = [
        ('General',  {
            'classes': ('wide',),
            'fields': [
                ('country',), ('country_division_type',), ('parent',), ('postal_zone',), ('code',), ('name',),
                ('latitude_min',), ('latitude_max',), ('longitude_min',), ('longitude_max',),
                ('geoname_id',)]
        }),
    ]
    list_display = ['id', 'country', 'country_division_type', 'parent', 'postal_zone', 'code', 'name', 'geoname_id']
    list_filter = ['country_division_type', 'country', 'postal_zone']
    ordering = ['code']
    search_fields = ['code', '_name_localizations']
