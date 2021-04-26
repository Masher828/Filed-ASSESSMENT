from django.urls import path
from . import  views

urlpatterns = [
    path('', views.CreateAudio.as_view(),name="Create"),
    path('<str:audioFileType>/<str:audioFileId>/', views.AudioFileDetail.as_view(),name="RUD_API")
]