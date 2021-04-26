from django.utils.encoding import smart_text
from rest_framework import serializers
from .models import SongModel, PodcastModel,AudiobookModel, ParticipantsModel

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongModel
        fields = (
            '__all__'
        )
class PodcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastModel
        fields = (
            '__all__'
        )
class AudiobookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudiobookModel
        fields = (
            '__all__'
        )

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantsModel
        fields = (
            '__all__'
        )