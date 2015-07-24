__author__ = 'dheerenr'

from rest_framework import serializers
from models import Event, EventLike, EventViews, EventImage
from authentication.serializers import DesignationReadSerializer


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage


class EventWriteSerializer(serializers.ModelSerializer):
    images = serializers.StringRelatedField(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes.count', read_only=True)
    views = serializers.IntegerField(source='views.count', read_only=True)

    class Meta:
        model = Event


class EventReadSerializer(EventWriteSerializer):
    posted_by = DesignationReadSerializer(read_only=True)


class EventLikeSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='event.likes.count', read_only=True)

    class Meta:
        model = EventLike


class EventViewSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField(source='event.views.count', read_only=True)
    liked = serializers.SerializerMethodField()

    def get_liked(self, obj):
        if isinstance(obj, EventViews):
            event = obj.event
            user = obj.user
            return EventLike.objects.all().filter(event=event).filter(user=user).exists()
        return False

    class Meta:
        model = EventViews
