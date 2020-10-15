# accounts/urls.py
from rest_framework import routers
from accounts.views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('', AuthViewSet, basename='auth')

urlpatterns = router.urls
