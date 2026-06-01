from django.contrib import admin

from .models import Member, News


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "created_at")
    search_fields = ("username", "email")
    readonly_fields = ("created_at",)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "news_type", "published_at", "views")
    list_filter = ("news_type", "published_at")
    search_fields = ("title", "content")
    date_hierarchy = "published_at"
