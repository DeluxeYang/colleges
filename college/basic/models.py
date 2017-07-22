import datetime

from django.db import models
from django.contrib.auth.models import User


class TypeOfTable(models.Model):  # 表类型：榜单 人才
    name_cn = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'type_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class Table(models.Model):  # 表
    type = models.ForeignKey(TypeOfTable, related_name='Table')  # 表类型
    name = models.CharField(max_length=30, unique=True)  # 表名
    name_cn = models.CharField(max_length=255, unique=True)  # 中文表名
    create_time = models.DateField(null=True, blank=True)  # 创建时间

    class Meta:
        db_table = 'table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn

    def save(self, *args, **kwargs):
        self.create_time = datetime.datetime.now().date()
        super().save(*args, **kwargs)


class YearSeasonMonth(models.Model):
    year = models.IntegerField(null=True, blank=True)  # 年
    season = models.IntegerField(null=True, blank=True)  # 季度
    month = models.IntegerField(null=True, blank=True)  # 月
    type = models.IntegerField(default=0)  # 类型：1年2季度3月
    text = models.CharField(max_length=30, null=True, blank=True)  # 文本

    class Meta:
        db_table = 'year_season_month'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.text)


class BatchOfTable(models.Model):  # 具体到批次的表名
    table = models.ForeignKey(Table, related_name='BatchOfTable')  # 表
    batch = models.ForeignKey(YearSeasonMonth, related_name='BatchOfTable')  # 批次
    name_cn = models.CharField(max_length=255, null=True, blank=True)  # 名
    create_time = models.DateField(null=True, blank=True)  # 创建时间
    excel_file = models.FileField(upload_to='data/excel', null=True, blank=True)

    class Meta:
        db_table = 'batch_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.table) + "_" + str(self.batch)

    def save(self, *args, **kwargs):
        self.create_time = datetime.datetime.now().date()
        super().save(*args, **kwargs)


class TypeOfField(models.Model):  # 字段类型
    name = models.CharField(max_length=30, unique=True)  # 名称
    size = models.IntegerField(null=True, blank=True)

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
    name_cn = models.CharField(max_length=30)  # 名称

    class Meta:
        db_table = 'edu_class'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class College(models.Model):
    name_cn = models.CharField(max_length=30, verbose_name="学校名称")  # 学校名
    id_code = models.CharField(max_length=30, verbose_name="学校标识码")  # 学校识别码
    department = models.CharField(max_length=30, null=True, blank=True, verbose_name="主管部门")  # 所属部门
    area = models.CharField(max_length=30, null=True, blank=True, verbose_name="片区")  # 片区
    nation_code = models.CharField(max_length=40, null=True, blank=True, verbose_name="行政区划编码")  # 行政区划编码
    edu_level = models.CharField(max_length=30, null=True, blank=True, verbose_name="办学层次")  # 办学层次：本科or专科
    edu_class = models.ForeignKey(EduClass, related_name='college', verbose_name="类别")  # 办学类型
    is_vice_ministry = models.BooleanField(default=False, verbose_name="副部级高校")  # 副部级高校
    is_211 = models.BooleanField(default=False, verbose_name="211工程")  # 211工程
    is_985 = models.BooleanField(default=False, verbose_name="985工程")  # 985工程
    is_985_platform = models.BooleanField(default=False, verbose_name="985平台")  # 985平台
    is_double_first_class = models.BooleanField(default=False, verbose_name="双一流大学")  # 双一流大学
    setup_time = models.DateField(null=True, blank=True, verbose_name="成立时间")  # 成立时间
    cancel_time = models.DateField(null=True, blank=True, verbose_name="注销时间")  # 注销时间
    note = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")  # 备注
    is_cancelled = models.BooleanField(default=False, verbose_name="已注销")  # 是否已取消
    transfer_to = models.CharField(max_length=30, null=True, blank=True, verbose_name="合并后学校代码")  # 合并后的高校编码

    class Meta:
        db_table = 'college'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class NewsTag(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'news_tag'

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class News(models.Model):
    user = models.ForeignKey(User, related_name='news')  # 发布用户
    college = models.ForeignKey(College, related_name='news')  # 新闻所属学校
    tag = models.ManyToManyField(NewsTag, through='NewsAndTag', related_name='news')  # 所属标签
    title = models.CharField(max_length=255, unique=True)  # 标题
    keywords = models.CharField(max_length=100, null=True, blank=True)  # 关键字
    description = models.TextField(null=True, blank=True)  # 描述
    content = models.TextField(null=True, blank=True)  # 内容
    is_published = models.BooleanField(default=False)  # 是否已发布
    comment_count = models.IntegerField(default=0)  # 评论数
    is_allow_comments = models.BooleanField(default=True)  # 是否允许评论
    is_stick_top = models.BooleanField(default=False)  # 是否置顶
    is_bold = models.BooleanField(default=False)  # 是否加粗
    create_time = models.DateTimeField(null=True, blank=True)  # 创建时间
    update_time = models.DateTimeField(null=True, blank=True)  # 更新时间
    publish_time = models.DateTimeField(null=True, blank=True)  # 发布时间

    class Meta:
        db_table = 'news'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.create_time:
            self.create_time = datetime.datetime.now()
        else:
            self.update_time = datetime.datetime.now()
        super().save(*args, **kwargs)


class NewsAndTag(models.Model):
    news = models.ForeignKey(News, related_name='news_and_tag')
    tag = models.ForeignKey(NewsTag, related_name='news_and_tag')

    class Meta:
        db_table = 'news_and_tag'


class NewsComment(models.Model):
    user = models.ForeignKey(User, related_name='news_comment')  # 发布用户
    news = models.ForeignKey(News, related_name='news_comment')  # 发布用户
    content = models.TextField(null=True, blank=True)  # 内容
    reply = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'news_comment'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.news) + " - " + str(self.content)[:10] + "..."
