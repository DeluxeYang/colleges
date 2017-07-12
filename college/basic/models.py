from django.db import models


class Tables(models.Model):
    table_name = models.CharField(max_length=30, unique=True)
    table_name_cn = models.CharField(max_length=255, unique=True)
    create_time = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tables'

    def __str__(self):  # __unicode__ on Python 2
        return self.table_name_cn


class DateOfTable(models.Model):
    table = models.ForeignKey(Tables, related_name='DateOfTable')
    year = models.IntegerField()
    month = models.IntegerField()
    create_time = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'date_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.table) + " - " + str(self.year) + " " + str(self.month)


class Types(models.Model):
    field_type = models.CharField(max_length=30)

    class Meta:
        db_table = 'types'

    def __str__(self):  # __unicode__ on Python 2
        return self.field_type


class Fields(models.Model):
    table = models.ForeignKey(Tables, related_name='Fields')
    field_type = models.ForeignKey(Types, related_name='Fields')
    field_name = models.CharField(max_length=30)
    field_name_cn = models.CharField(max_length=255)

    class Meta:
        db_table = 'fields'

    def __str__(self):  # __unicode__ on Python 2
            return str(self.table) + " - " + str(self.field_name_cn)


class Nation(models.Model):
    code = models.CharField(max_length=40, null=True, blank=True)
    province = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    district = models.CharField(max_length=40, null=True, blank=True)
    parent = models.CharField(max_length=40, null=True, blank=True)
    lng = models.FloatField(default=0)
    lat = models.FloatField(default=0)
    geohash = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'nation'

    def __str__(self):  # __unicode__ on Python 2
            return self.province + self.city + self.district
