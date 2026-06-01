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
