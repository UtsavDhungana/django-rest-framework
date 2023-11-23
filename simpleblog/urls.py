from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import *

router = DefaultRouter()
router.register(r"model", PostModelViewset, basename="model_posts")
router.register(r"", PostViewset, basename="posts")

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("posts/",include("posts.urls")),
    path("posts/",include(router.urls)),
]
