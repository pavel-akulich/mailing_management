from django.urls import path

from service_client.apps import ServiceClientConfig
from home.views import HomeView


app_name = ServiceClientConfig.name

urlpatterns = [
    path('', (HomeView.as_view()), name='home'),
]
