from django.urls import path

from service_client.apps import ServiceClientConfig
from service_client.views import ClientListView, ClientDetailView, HomeView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView

app_name = ServiceClientConfig.name

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
