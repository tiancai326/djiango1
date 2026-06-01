from datetime import datetime

from django.db import models
from froala_editor.fields import FroalaField


class Member(models.Model):
    email = models.EmailField("邮箱", unique=True)
    username = models.CharField("姓名", max_length=150, unique=True)
    password = models.CharField("密码", max_length=128)
    created_at = models.DateTimeField("注册时间", auto_now_add=True)

    class Meta:
        verbose_name = "会员"
        verbose_name_plural = "会员"

    def __str__(self):
        return self.username


class News(models.Model):
    NEWS_TYPE_CHOICES = (
        ("company", "企业新闻"),
        ("industry", "行业新闻"),
        ("notice", "通知公告"),
    )

    title = models.CharField("标题", max_length=200)
    content = FroalaField("内容")
    news_type = models.CharField("新闻类型", max_length=20, choices=NEWS_TYPE_CHOICES, default="company")
    published_at = models.DateTimeField("发布时间")
    views = models.PositiveIntegerField("浏览量", default=0)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = "新闻"
        ordering = ("-published_at",)

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name="招聘岗位")
    description = models.TextField(verbose_name="岗位要求")
    publishDate = models.DateTimeField(max_length=20, default=datetime.now, verbose_name="发布时间")

    class Meta:
        verbose_name = "招聘广告"
        verbose_name_plural = "招聘广告"
        ordering = ("-publishDate",)

    def __str__(self):
        return self.title


class Resume(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    personID = models.CharField(max_length=30, verbose_name="身份证号")
    sex = models.CharField(max_length=5, default="男", verbose_name="性别")
    email = models.EmailField(max_length=30, verbose_name="邮箱")
    birth = models.DateField(
        max_length=20,
        default=datetime.strftime(datetime.now(), "%Y-%m-%d"),
        verbose_name="出生日期",
    )
    edu = models.CharField(max_length=5, default="本科", verbose_name="学历")
    school = models.CharField(max_length=40, verbose_name="毕业院校")
    major = models.CharField(max_length=40, verbose_name="专业")
    position = models.CharField(max_length=40, verbose_name="申请职位")
    experience = models.TextField(blank=True, null=True, verbose_name="学习或工作经历")
    photo = models.ImageField(upload_to="contact/recruit/%Y_%m_%d", verbose_name="个人照片")

    grade_list = (
        (1, "未审"),
        (2, "通过"),
        (3, "未通过"),
    )
    status = models.IntegerField(choices=grade_list, default=1, verbose_name="审核")
    publishDate = models.DateTimeField(max_length=20, default=datetime.now, verbose_name="提交时间")

    class Meta:
        verbose_name = "简历"
        verbose_name_plural = "简历"
        ordering = ("-status", "-publishDate")

    def __str__(self):
        return self.name
