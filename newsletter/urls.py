from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView, MailingLogsListView

app_name = NewsletterConfig.name

urlpatterns = [
    path('list/', MessageListView.as_view(), name='message_list'),
    path('list/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('list/create/', MessageCreateView.as_view(), name='message_create'),
    path('list/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('list/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('report/', MailingLogsListView.as_view(), name='report_list'),
]
