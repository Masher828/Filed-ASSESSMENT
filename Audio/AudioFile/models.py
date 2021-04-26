from djongo import models
from django.core.validators import ValidationError
import datetime


class SongModel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField()
    uploaded_time = models.DateTimeField(default=datetime.datetime.now)

    def clean(self, *args, **kwargs):
        if self.duration < 0:
            raise ValidationError("Duration Cannot be Negative")
        super(SongModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(SongModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class PodcastModel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)
    uploaded_time = models.DateTimeField(default=datetime.datetime.now)
    host = models.CharField(max_length=100, blank=True, null=True)

    def clean(self, *args, **kwargs):
        if self.duration < 0:
            raise ValidationError("Duration Cannot be Negative")
        super(PodcastModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(PodcastModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ParticipantsModel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    podcast = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class AudiobookModel(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    narrator = models.CharField(max_length=100, null=False, blank=False)
    duration = models.IntegerField(null=False, blank=False)

    def clean(self, *args, **kwargs):
        if self.duration < 0:
            raise ValidationError("Duration Cannot be Negative")
        super(AudiobookModel, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AudiobookModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
