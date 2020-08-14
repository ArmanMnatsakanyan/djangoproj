from django.urls import path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetail, GenericApiView, ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    path('', include(router.urls)),
    path('/<int:pk>/', include(router.urls)),

    #path('articles/', article_list),
    path('articles/', ArticleAPIView.as_view()),
    path('generic/', GenericApiView.as_view()),
    #path('detail/<int:pk>', article_detail),
    path('detail/<int:id>', ArticleDetail.as_view()),


]