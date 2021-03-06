from django.contrib import admin
from models import Event, EventImage, EventLike, EventViews
from django.db.models import Prefetch


class EventAdmin(admin.ModelAdmin):
    # TODO: Add total views if possible in 1 or 2 queries. Adding Sum in queryset gives error
    list_display = ['id', 'title', 'category', 'posted_by', 'total_likes', 'unique_views']

    def get_queryset(self, request):
        queryset = Event.objects.all().prefetch_related(Prefetch('likes', EventLike.objects.all())).prefetch_related(
            Prefetch('views', EventViews.objects.all()))
        return queryset

    def total_likes(self, ins):
        return ins.likes.count()

    def unique_views(self, ins):
        return ins.views.count()


class EventImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'image']


admin.site.register(Event, EventAdmin)
admin.site.register(EventImage, EventImageAdmin)
