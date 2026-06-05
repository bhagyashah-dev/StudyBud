# from django.urls import path
# from . import views

# urlpatterns = [
#     path('students/', views.get_students, name='get_student'),
#     path('students/create', views.create_students, name='create_students'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('gRooms/', views.gRooms, name='gRooms'),
    path('gRooms/createRooms/', views.createRooms, name='createRooms'),
    path('gRooms/room_detail/<int:pk>', views.room_detail, name='room_detail'),
]