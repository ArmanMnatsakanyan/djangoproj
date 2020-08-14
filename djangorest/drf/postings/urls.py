from django.urls import include, path

from .views import BlogPostAPIView, BlogPostRudView
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter
# router.register('blogs', BlogPostRudView, basename='blogs')
app_name = 'postings'

urlpatterns = [
    # path('', include(router.urls)),
    path('', BlogPostAPIView.as_view(), name='post'),
    path('blogs/', BlogPostAPIView.as_view(), name='post-listblogs'),
    path('blogs/<int:pk>', BlogPostRudView.as_view(), name='post-rud'),
]
