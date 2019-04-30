from rest_framework import routers
from django.urls import include, path

from core.api.views import (
    ListContent, 
    ListUser,
    ListCommit,
    )


urlpatterns = [
    path('content/', ListContent.as_view()),
    path('user/', ListUser.as_view()),
    path('commit/', ListCommit.as_view()),
]
