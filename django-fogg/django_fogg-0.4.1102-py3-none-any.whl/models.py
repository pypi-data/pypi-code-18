from django.db import models


CONTINENT_CHOICES = [
    ('EU', 'Europe'),
    ('AS', 'Asia'),
    ('NA', 'North America'),
    ('AF', 'Africa'),
    ('OC', 'Ocean'),
    ('SA', 'South America'),
    ('AN', 'Antarctica')]


class Country(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    isoN = models.CharField(max_length=3)
    fips = models.CharField(max_length=2)
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES)
    tld = models.CharField(max_length=8)
    currency_code = models.CharField(max_length=3)
    phone_number_prefix = models.CharField(max_length=255)
    phone_number_regex = models.CharField(max_length=255)
    postal_code_format = models.CharField(max_length=255)
    postal_code_regex = models.CharField(max_length=255)
    geoname_id = models.PositiveIntegerField()

    def __str__(self):
        return self.name or self.iso3

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        localizable_fields = ('name',)


class PostalZoneManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class PostalZone(models.Model):
    objects = PostalZoneManager()

    id = models.AutoField(unique=True, primary_key=True)
    country = models.ForeignKey(Country, related_name='+', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Postal Zone'
        verbose_name_plural = 'Postal Zones'


class CountryDivisionTypeManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class CountryDivisionType(models.Model):
    objects = CountryDivisionTypeManager()

    id = models.AutoField(unique=True, primary_key=True)
    country = models.ForeignKey(Country, related_name='+', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return self.name or self.code

    class Meta:
        verbose_name = 'Country Division Type'
        verbose_name_plural = 'Country Division Types'
        localizable_fields = ('name',)


class CountryDivisionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class CountryDivision(models.Model):
    objects = CountryDivisionManager()

    id = models.AutoField(unique=True, primary_key=True)
    country = models.ForeignKey(Country, related_name='+', on_delete=models.CASCADE)
    country_division_type = models.ForeignKey(CountryDivisionType, related_name='+', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    postal_zone = models.ForeignKey(PostalZone, null=True, blank=True, related_name='+', on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    latitude_min = models.DecimalField(max_digits=12, decimal_places=8)
    latitude_max = models.DecimalField(max_digits=12, decimal_places=8)
    longitude_min = models.DecimalField(max_digits=12, decimal_places=8)
    longitude_max = models.DecimalField(max_digits=12, decimal_places=8)
    geoname_id = models.PositiveIntegerField(null=True, blank=True)

    def natural_key(self):
        return (self.code,)

    def __str__(self):
        return '{0}, {1}'.format(self.parent, self.name or self.code) if self.parent else (self.name or self.code)

    class Meta:
        verbose_name = 'Country Division'
        verbose_name_plural = 'Country Divisions'
        localizable_fields = ('name',)
