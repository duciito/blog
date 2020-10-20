# core/urls.py
from rest_framework import routers
from core.views import CategoriesViewSet

router = routers.DefaultRouter()
router.register('categories', CategoriesViewSet, basename='categories')

urlpatterns = router.urls
