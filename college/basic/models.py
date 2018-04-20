import datetime
from django.contrib.postgres.fields import JSONField
from DjangoUeditor.models import UEditorField
from django.db import models
from django.contrib.auth.models import User


class TypeOfTable(models.Model):  # 表类型：榜单 人才
    name_cn = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'type_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class Table(models.Model):  # 表
    type = models.ForeignKey(TypeOfTable, related_name='Table', on_delete=models.CASCADE)  # 表类型
    name = models.CharField(max_length=30, null=True, blank=True)  # 表名
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

    def save(self, *args, **kwargs):
        seasons = ["一", "二", "三", "四"]
        self.text = str(self.year) + "年"
        if self.type == 2:
            self.text += ("第" + seasons[self.season-1] + "季度")
        if self.type == 3:
            self.text += (str(self.month) + "月")
        super().save(*args, **kwargs)


class BatchOfTable(models.Model):  # 具体到批次的表名
    table = models.ForeignKey(Table, related_name='BatchOfTable', on_delete=models.CASCADE)  # 表
    batch = models.ForeignKey(YearSeasonMonth, related_name='BatchOfTable', on_delete=models.CASCADE)  # 批次
    name_cn = models.CharField(max_length=255, null=True, blank=True, unique=True)  # 名
    create_time = models.DateField(null=True, blank=True)  # 创建时间
    excel_file = models.FileField(upload_to='data/excel', null=True, blank=True)
    table_type = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'batch_of_table'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.table) + "_" + str(self.batch)

    def save(self, *args, **kwargs):
        self.create_time = datetime.datetime.now().date()
        self.table_type = self.table.type.id
        self.name_cn = self.table.name_cn + "_" + self.batch.text
        super().save(*args, **kwargs)


# class TypeOfField(models.Model):  # 字段类型
#     name = models.CharField(max_length=30, unique=True)  # 名称
#     size = models.IntegerField(null=True, blank=True)
#
#     class Meta:
#         db_table = 'type_of_field'
#
#     def __str__(self):  # __unicode__ on Python 2
#         return self.name


class Field(models.Model):  # 表的字段
    table = models.ForeignKey(Table, related_name='Fields', on_delete=models.CASCADE)  # 表
    name = models.CharField(max_length=30, null=True, blank=True)  # 字段名
    name_cn = models.CharField(max_length=255)  # 中文字段名
    # type = models.ForeignKey(TypeOfField, related_name='Fields')  # 字段类型

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


class Department(models.Model):  # 主管部门
    name_cn = models.CharField(max_length=30, null=True, blank=True)  # 名称

    class Meta:
        db_table = 'department'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class EduLevel(models.Model):  # 办学层次
    name_cn = models.CharField(max_length=30, null=True, blank=True)  # 名称

    class Meta:
        db_table = 'edu_level'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class EduClass(models.Model):  # 办学类别
    name_cn = models.CharField(max_length=30, null=True, blank=True)  # 名称

    class Meta:
        db_table = 'edu_class'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class College(models.Model):
    name_cn = models.CharField(max_length=30, unique=True, verbose_name="学校名称")  # 学校名
    id_code = models.CharField(max_length=30, unique=True, verbose_name="学校标识码")  # 学校识别码
    department = models.ForeignKey(Department, related_name='college', verbose_name="主管部门", on_delete=models.CASCADE)  # 办学类型
    area = models.CharField(max_length=30, null=True, blank=True, verbose_name="片区")  # 片区
    province = models.CharField(max_length=30, null=True, blank=True, verbose_name="所在地（省级）")  # 所在地（省级）
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name="所在地（城市）")  # 所在地（城市）
    nation_code = models.CharField(max_length=40, null=True, blank=True, verbose_name="行政区划编码")  # 行政区划编码
    edu_level = models.ForeignKey(EduLevel, related_name='college', verbose_name="办学层次", on_delete=models.CASCADE)  # 办学层次：本科or专科
    edu_class = models.ForeignKey(EduClass, related_name='college', verbose_name="类别", on_delete=models.CASCADE)  # 办学类型
    is_vice_ministry = models.BooleanField(default=False, verbose_name="副部级高校")  # 副部级高校
    is_211 = models.BooleanField(default=False, verbose_name="211工程")  # 211工程
    is_985 = models.BooleanField(default=False, verbose_name="985工程")  # 985工程
    is_985_platform = models.BooleanField(default=False, verbose_name="985平台")  # 985平台
    is_double_first_class = models.BooleanField(default=False, verbose_name="双一流大学")  # 双一流大学
    setup_time = models.DateField(null=True, blank=True, verbose_name="成立时间")  # 成立时间
    cancel_time = models.DateField(null=True, blank=True, verbose_name="注销时间")  # 注销时间
    note = models.CharField(max_length=255, null=True, blank=True, verbose_name="备注")  # 备注
    is_cancelled = models.BooleanField(default=False, verbose_name="已撤销")  # 是否已取消
    transfer_to = models.CharField(max_length=30, null=True, blank=True, verbose_name="合并后学校代码")  # 合并后的高校编码

    class Meta:
        db_table = 'college'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class Area(models.Model):
    name_cn = models.CharField(max_length=30)
    nation_code_2 = models.CharField(max_length=2, null=True, blank=True)
    is_index = models.BooleanField(default=False)

    class Meta:
        db_table = 'area'

    def __str__(self):  # __unicode__ on Python 2
        return self.name_cn


class NewsTag(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'news_tag'

    def __str__(self):  # __unicode__ on Python 2
        return self.title


class News(models.Model):
    user = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)  # 发布用户
    tag = models.ManyToManyField(NewsTag, through='NewsAndTag', verbose_name="标签")  # 所属标签
    college = models.ManyToManyField(College, through='NewsAndCollege', verbose_name="相关院校")
    title = models.CharField(max_length=255, verbose_name="标题")  # 标题
    link = models.TextField(null=True, blank=True, verbose_name="链接")  # 链接
    keywords = models.CharField(max_length=100, null=True, blank=True, verbose_name="关键字")  # 关键字
    abstract = models.TextField(null=True, blank=True, verbose_name="摘要")  # 摘要
    content = UEditorField('内容', height=500, width="auto", default=u'',
                           blank=True, imagePath="news/images/",
                           toolbars='full', filePath='upload/files/')
    is_published = models.BooleanField(default=False, verbose_name="已发布")  # 是否已发布
    is_allow_comments = models.BooleanField(default=True, verbose_name="允许评论")  # 是否允许评论
    is_stick_top = models.BooleanField(default=False, verbose_name="置顶")  # 是否置顶
    is_bold = models.BooleanField(default=False, verbose_name="加粗")  # 是否加粗
    create_time = models.DateTimeField(null=True, blank=True)  # 创建时间
    update_time = models.DateTimeField(null=True, blank=True)  # 更新时间
    publish_time = models.DateTimeField(null=True, blank=True)  # 发布时间
    comment_count = models.IntegerField(default=0)  # 评论数

    class Meta:
        db_table = 'news'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.create_time:
            self.create_time = datetime.datetime.now()
        else:
            self.update_time = datetime.datetime.now()
        self.publish_time = datetime.datetime.now() if self.is_published else None
        super().save(*args, **kwargs)


class NewsAndCollege(models.Model):
    news = models.ForeignKey(News, related_name='news_and_college', on_delete=models.CASCADE)
    college = models.ForeignKey(College, related_name='news_and_college', on_delete=models.CASCADE)

    class Meta:
        db_table = 'news_and_college'


class NewsAndTag(models.Model):
    news = models.ForeignKey(News, related_name='news_and_tag', on_delete=models.CASCADE)
    tag = models.ForeignKey(NewsTag, related_name='news_and_tag', on_delete=models.CASCADE)

    class Meta:
        db_table = 'news_and_tag'


class NewsComment(models.Model):
    user = models.ForeignKey(User, related_name='news_comment', on_delete=models.CASCADE)  # 发布用户
    news = models.ForeignKey(News, related_name='news_comment', on_delete=models.CASCADE)  # 发布用户
    content = models.TextField(null=True, blank=True)  # 内容
    reply = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'news_comment'

    def __str__(self):  # __unicode__ on Python 2
        return str(self.news) + " - " + str(self.content)[:10] + "..."


class NewsImage(models.Model):
    image = models.ImageField(upload_to='news/images/')

    class Meta:
        db_table = 'news_image'


class Ranking(models.Model):
    batch = models.ForeignKey(BatchOfTable, related_name="ranking", on_delete=models.CASCADE)
    data = JSONField()

    class Meta:
        db_table = 'ranking'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Professor(models.Model):
    batch = models.ForeignKey(BatchOfTable, related_name="professor", on_delete=models.CASCADE)
    data = JSONField()

    class Meta:
        db_table = 'professor'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class RankingAndCollegeRelation(models.Model):
    college = models.ForeignKey(College, related_name="RankingAndCollegeRelation", on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, related_name="RankingAndCollegeRelation", on_delete=models.CASCADE)

    class Meta:
        db_table = 'ranking_and_college'


class ProfessorAndCollegeRelation(models.Model):
    college = models.ForeignKey(College, related_name="ProfessorAndCollegeRelation", on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, related_name="ProfessorAndCollegeRelation", on_delete=models.CASCADE)

    class Meta:
        db_table = 'professor_and_college'
