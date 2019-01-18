from django.urls import path

from . import views

app_name = 'chat'
urlpatterns = [
    # 元のコードは→url(r'^$', views.index, name='index'),
    path('<slug:room_name>/', views.RoomView.as_view(), name='room'),
    path('c/<slug:room_name>/', views.send_msg, name='send_msg'),
]