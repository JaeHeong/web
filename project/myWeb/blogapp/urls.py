from django.urls import path

from .views import *

urlpatterns = [
    path('', board, name='board'),
    path('edit/<int:pk>', boardEdit, name='edit'),
    path('delete/<int:pk>', boardDelete, name='delete'),
    path('detail/<int:pk>', boardDetail, name='detail'),

    path('file/', file, name='file'),
    path('fileupload/', fileUpload, name="fileupload"),
    path('filedetail/<int:pk>', fileUploadDetail, name='filedetail'),
    path('fileedit/<int:pk>', fileEdit, name='fileedit'),
    path('filedelete/<int:pk>', fileDelete, name='filedelete'),
]