from django.urls import path

from . import views

app_name = "prox"
urlpatterns = [
    path('', views.index, name='index'),
    path('requests/', views.AddressView.as_view(), name='requests'),
    path('send_request/', views.add_request, name='send_requests'),
    path('delete_data/', views.delete_data, name='delete')
]