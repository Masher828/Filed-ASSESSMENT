from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PodcastModel, AudiobookModel, SongModel, ParticipantsModel
from .serializers import SongSerializer, PodcastSerializer, AudiobookSerializer, ParticipantSerializer
from bson.objectid import ObjectId
from django.views.defaults import bad_request

types = ['song', 'podcast', 'audiobook']

class CreateAudio(APIView):

    def post(self, request):
        try:
            audio = str(request.POST['audioFileType']).lower()
            if audio in types:
                if audio == "song":
                    try:
                        SongModel(name=request.POST['name'], duration=int(request.POST['duration'])).save()
                    except MultiValueDictKeyError:
                        return Response({"status":False,"info":"Data Missing"})
                elif audio == "audiobook":
                    try:
                        AudiobookModel(title=request.POST['title'], duration=int(request.POST['duration']),
                                       author=request.POST['author'], narrator=request.POST['narrator']).save()
                    except MultiValueDictKeyError:
                        return Response({"status":False,"info":"Data Missing"})
                elif audio == "podcast":
                    try:
                        pod = PodcastModel()
                        pod.name = request.POST['name']
                        pod.duration = int(request.POST['duration'])
                        pod.host = request.POST['host']
                        pod.save()
                    except MultiValueDictKeyError:
                        return Response({"status":False,"info":"Data Missing"})

                    try:
                        participants = request.POST['participants'].split(",")
                        for per in participants:
                            ParticipantsModel(name=per, podcast=pod._id).save()
                    except MultiValueDictKeyError:
                        pass
                else:
                    raise bad_request

            else:
                raise bad_request

        except Exception as e:
            return Response({'status': False, "info":'Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e))})
        return Response({'status': True})



class AudioFileDetail(APIView):
    def delete(self, request, audioFileType, audioFileId):
        try:
            audio = str(audioFileType).lower()
            if audio in types:
                if audio == "song":
                    SongModel.objects.get(_id=ObjectId(audioFileId)).delete()
                elif audio == "audiobook":
                    AudiobookModel.objects.get(_id=ObjectId(audioFileId)).delete()
                elif audio == "podcast":
                    print("don")
                    ParticipantsModel.objects.filter(podcast = audioFileId).delete()
                    PodcastModel.objects.get(_id=ObjectId(audioFileId)).delete()
                else:
                    raise bad_request
            else:
                raise bad_request

        except Exception as e:
            return Response({'status': False, "info":'Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e))})
        return Response({'status': True})

    def put(self, request, audioFileType, audioFileId):
        try:
            audio = str(audioFileType).lower()
            if audio in types:
                if audio == "song":
                    audio = SongModel.objects.get(_id=ObjectId(audioFileId))
                    try:
                        audio.name = request.POST['name']
                    except MultiValueDictKeyError:
                        pass
                    try:
                        audio.duration = int(request.POST['duration'])
                    except MultiValueDictKeyError:
                        pass
                    audio.save()

                elif audio == "audiobook":
                    audio = AudiobookModel.objects.get(_id=ObjectId(audioFileId))
                    try:
                        audio.title = request.POST['title']
                    except MultiValueDictKeyError:
                        pass

                    try:
                        audio.author = request.POST['author']
                    except MultiValueDictKeyError:
                        pass
                    try:
                        audio.narrator = request.POST['narrator']
                    except MultiValueDictKeyError:
                        pass
                    try:
                        audio.duration = int(request.POST['duration'])
                    except MultiValueDictKeyError:
                        pass
                    audio.save()
                elif audio == "podcast":
                    audio = PodcastModel.objects.get(_id=ObjectId(audioFileId))
                    try:
                        audio.name = request.POST['name']
                    except MultiValueDictKeyError:
                        pass

                    try:
                        audio.host = request.POST['host']
                    except MultiValueDictKeyError:
                        pass
                    try:

                        ParticipantsModel.objects.filter(podcast=audioFileId).delete()
                        participants = request.POST['participants'].split(",")
                        for per in participants:
                            ParticipantsModel(name=per, podcast=audioFileId).save()
                    except MultiValueDictKeyError:
                        pass
                    try:
                        audio.duration = int(request.POST['duration'])
                    except MultiValueDictKeyError:
                        pass
                    except ValueError:
                        return Response({"status":False,"info":"Duration should be Integer"})
                    audio.save()
                else:
                    raise bad_request
            else:
                raise bad_request

        except Exception as e:
            return Response({'status': False, "info":'Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e))})
        return Response({'status': True})

    def get(self, request, audioFileType, audioFileId):
        try:
            audio = str(audioFileType).lower()
            if audio in types:
                if audio == "song":
                    return Response(SongSerializer(SongModel.objects.get(_id=ObjectId(audioFileId))).data)

                elif audio == "audiobook":
                    return Response(AudiobookSerializer(AudiobookModel.objects.get(_id=ObjectId(audioFileId))).data)

                elif audio == "podcast":
                    participants = ParticipantSerializer(ParticipantsModel.objects.filter(podcast=audioFileId),many=True)
                    return Response({"Podcast":PodcastSerializer(PodcastModel.objects.get(_id=ObjectId(audioFileId))).data,"Participants":participants.data})

                else:
                    raise bad_request
            else:
                raise bad_request

        except Exception as e:
            return  Response({'status':False,"info":'Error! Code: {c}, Message, {m}'.format(c=type(e).__name__, m=str(e))})
