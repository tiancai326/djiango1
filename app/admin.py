from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Ad, Member, News, Product, ProductImg, Resume


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


class ProductImgInline(admin.StackedInline):
    model = ProductImg
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInline]
    list_display = ("id", "title", "productType", "price", "publishDate", "views")
    list_filter = ("productType", "publishDate")
    search_fields = ("title", "description")
    date_hierarchy = "publishDate"


class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "personID",
        "birth",
        "edu",
        "school",
        "major",
        "position",
        "image_data",
    )

    def image_data(self, obj):
        if not obj.photo:
            return "-"
        return mark_safe('<img src="%s" width="120px" />' % obj.photo.url)

    image_data.short_description = "个人照片"


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Ad)
