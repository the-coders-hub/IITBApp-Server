__author__ = 'dheerendra'

from django import forms
from django.utils.translation import gettext as _
from django.utils import timezone

from event.models import Event, EventImage
from authentication.models import Designation
from core.globals import categories, datetime_input_formats
import event.signals as event_signals


class EventForm(forms.Form):
    id = forms.IntegerField(required=False)
    title = forms.CharField(max_length=256)
    description = forms.CharField(required=False)
    category = forms.ChoiceField(choices=categories)
    event_time = forms.DateTimeField(input_formats=datetime_input_formats)
    event_place = forms.CharField(max_length=256)
    cancelled = forms.BooleanField(required=False, initial=False)
    event_image = forms.ImageField(required=False)
    designation = forms.IntegerField()
    notify_users = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """
        Validation on the basis of
        1. id should be -1 or None. If anything else is present as id then current user should be owner of that item
        2. designation should belongs to the user who is adding/modifying item
        :return: cleaned_data
        """

        cleaned_data = super(EventForm, self).clean()
        id_ = cleaned_data.get('id')
        if id_ is not None and id_ != -1:
            event = Event.objects.all().filter(posted_by__user=self.user).filter(id=id_)
            if not event.exists():
                raise forms.ValidationError(_('Unauthorised access on event'), code='InvalidAccess')
        designation = Designation.objects.all().filter(user=self.user).filter(pk=cleaned_data['designation'])
        if not designation.exists():
            raise forms.ValidationError(_('The designation provided is invalid'), code='InvalidDesignation')
        if not designation[0].is_active():
            raise forms.ValidationError(_('The designation is outdated. Please use any active designation'),
                                        code='InActiveDesignation')
        event_time = cleaned_data.get('event_time')
        if event_time is not None and event_time < timezone.now():
            raise forms.ValidationError(_('Event time should be in future'), code='InvalidEventDate')
        return cleaned_data

    def save(self):
        id_ = self.cleaned_data.get('id')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        category = self.cleaned_data.get('category')
        event_time = self.cleaned_data.get('event_time')
        event_place = self.cleaned_data.get('event_place')
        cancelled = self.cleaned_data.get('cancelled')
        event_image = self.cleaned_data.get('event_image')
        designation = self.cleaned_data.get('designation')
        notify_users = self.cleaned_data.get('notify_users')
        if id_ is not None and id_ != -1:
            created = False
            event = Event.objects.get(pk=id_)
            event.title = title
            event.description = description
            event.category = category
            event.event_time = event_time
            event.event_place = event_place
            event.cancelled = cancelled
            event.posted_by_id = designation
        else:
            created = True
            event = Event(title=title,
                          description=description,
                          category=category,
                          event_time=event_time,
                          event_place=event_place,
                          cancelled=cancelled,
                          posted_by_id=designation)
            notify_users = True
        event.save()
        if event_image is not None and event_image.image is not None:
            '''
            updating old image to just support single image for now. Should be changed in future to support multiple
            images here and at UI side
            '''
            try:
                eventImage = EventImage.objects.get(event=event)
                eventImage.image = event_image
            except EventImage.DoesNotExist:
                eventImage = EventImage(
                    event=event,
                    image=event_image
                )
            eventImage.save()
        if notify_users:
            event.refresh_from_db()
            event_signals.event_done.send(Event, instance=event, created=created)
        return event
