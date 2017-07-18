from django.db import models


class TypeOfTable(models.Model):  # 表类型：榜单 人才
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'type_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Table(models.Model):  # 表
    type = models.ForeignKey(TypeOfTable, related_name='Table')  # 表类型
    name = models.CharField(max_length=30, unique=True)  # 表名
    name_cn = models.CharField(max_length=255, unique=True)  # 中文表名
    create_time = models.DateField(null=True, blank=True)  # 创建时间

    class Meta:
        db_table = 'table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class YearSeasonMonth(models.Model):
    year = models.IntegerField(null=True, blank=True)  # 年
    season = models.IntegerField(null=True, blank=True)  # 季度
    month = models.IntegerField(null=True, blank=True)  # 月
    type = models.IntegerField(default=0)  # 类型：1年2季度3月

    class Meta:
        db_table = 'year_season_month'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.year) + " " + str(self.month)


class BatchOfTable(models.Model):  # 具体到批次的表名
    table = models.ForeignKey(Table, related_name='BatchOfTable')  # 表
    batch = models.ForeignKey(YearSeasonMonth, related_name='BatchOfTable')  # 批次
    name = models.CharField(max_length=255, null=True, blank=True)  # 名

    class Meta:
        db_table = 'batch_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.table) + " - " + str(self.batch)


class TypeOfField(models.Model):  # 字段类型
    name = models.CharField(max_length=30)  # 名称

    class Meta:
        db_table = 'type_of_field'

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class Field(models.Model):  # 表的字段
    table = models.ForeignKey(Table, related_name='Fields')  # 表
    type = models.ForeignKey(TypeOfField, related_name='Fields')  # 字段类型
    name = models.CharField(max_length=30)  # 字段名
    name_cn = models.CharField(max_length=255)  # 中文字段名

    class Meta:
        db_table = 'field'

    def __str__(self):  # __unicode__ on Python 2
            return str(self.table) + " - " + str(self.name_cn)


class Nation(models.Model):  # 行政区划
    code = models.CharField(max_length=40, null=True, blank=True)  # 行政区划编码
    province = models.CharField(max_length=40, null=True, blank=True)  # 省
    city = models.CharField(max_length=40, null=True, blank=True)  # 市
    district = models.CharField(max_length=40, null=True, blank=True)  # 区
    parent = models.CharField(max_length=40, null=True, blank=True)  # 父
    lng = models.FloatField(default=0)  # 经度
    lat = models.FloatField(default=0)  # 纬度
    geohash = models.CharField(max_length=40, null=True, blank=True)  # geohash

    class Meta:
        db_table = 'nation'

    def __str__(self):  # __unicode__ on Python 2
            return self.province + self.city + self.district


class EduClass(models.Model):  # 办学类别
    name = models.CharField(max_length=30)  # 名称

    class Meta:
        db_table = 'edu_class'

    def __str__(self):  # __unicode__ on Python 2
        return self.name


class College(models.Model):
    name = models.CharField(max_length=30)  # 学校名
    id_code = models.CharField(max_length=30)  # 学校识别码
    department = models.CharField(max_length=30, null=True, blank=True)  # 所属部门
    area = models.CharField(max_length=30, null=True, blank=True)  # 片区
    nation_code = models.CharField(max_length=40, null=True, blank=True)  # 行政区划编码
    edu_level = models.CharField(max_length=30, null=True, blank=True)  # 办学层次：本科or专科
    edu_class = models.ForeignKey(EduClass, related_name='college')  # 办学类型
    is_vice_ministry = models.BooleanField(default=False)  # 副部级高校
    is_211 = models.BooleanField(default=False)  # 211工程
    is_985 = models.BooleanField(default=False)  # 985工程
    is_985_platform = models.BooleanField(default=False)  # 985平台
    is_double_first_class = models.BooleanField(default=False)  # 双一流大学
    setup_time = models.DateField(null=True, blank=True)  # 成立时间
    cancel_time = models.DateField(null=True, blank=True)  # 注销时间
    note = models.CharField(max_length=255, null=True, blank=True)  # 备注
    is_cancelled = models.BooleanField(default=False)  # 是否已取消
    transfer_to = models.CharField(max_length=30, null=True, blank=True)  # 合并后的高校编码

    class Meta:
        db_table = 'college'

    def __str__(self):  # __unicode__ on Python 2
        return self.name
