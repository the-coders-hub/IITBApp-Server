from django.contrib import admin
from models import News, NewsImage

# Register your models here.
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_by', 'time')

class NewsImageAdmin(admin.ModelAdmin):
    list_display = ('news', 'image')

admin.site.register(News, NewsAdmin)
admin.site.register(NewsImage, NewsImageAdmin)