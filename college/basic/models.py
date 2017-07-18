from django.db import models


class TypeOfTable(models.Model):
    name_cn = models.CharField(max_length=30, unique=True)
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'type_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Table(models.Model):
    type = models.ForeignKey(TypeOfTable, related_name='Table')
    table_name = models.CharField(max_length=30, unique=True)
    table_name_cn = models.CharField(max_length=255, unique=True)
    create_time = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'table'

    def __str__(self):  # __unicode__ on Python 2
        return self.table_name_cn


class YearAndMonth(models.Model):
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(default=0)

    class Meta:
        db_table = 'year_and_month'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.year) + " " + str(self.month)


class DateOfTable(models.Model):
    table = models.ForeignKey(Table, related_name='DateOfTable')
    date = models.ForeignKey(YearAndMonth, related_name='DateOfTable')
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'date_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.table) + " - " + str(self.date)


class TypeOfField(models.Model):
    field_type = models.CharField(max_length=30)

    class Meta:
        db_table = 'type_of_field'

    def __str__(self):  # __unicode__ on Python 2
        return self.field_type


class Field(models.Model):
    table = models.ForeignKey(Table, related_name='Fields')
    field_type = models.ForeignKey(TypeOfField, related_name='Fields')
    field_name = models.CharField(max_length=30)
    field_name_cn = models.CharField(max_length=255)

    class Meta:
        db_table = 'field'

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
