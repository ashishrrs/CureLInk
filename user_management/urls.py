from django.urls import path
from .views import *

app_name = 'user_management'

urlpatterns = [
    path('article/list/', get_article_list),      # listing the article
    path('article/add_article/', add_article),
    path('subscriber/list/',  get_subscriber_list),
    path('subscriber/add_subscriber/',  add_subscriber),
    path('topic/list/',  get_topic_list),
    path('topic/add_topic/',  add_topic),
    path('topic/delete_topic/',  delete_topic),
    path('subscriber/delete_subscriber/',  delete_subscriber),
    path('article/delete_article/', delete_article),
    path('article/update_article/', update_article),
    path('subscriber/update_subscriber/', update_subscriber),
    path('topic/update_topic/', update_topic),
]
