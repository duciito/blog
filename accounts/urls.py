# accounts/urls.py
from rest_framework import routers
from accounts.views import AuthViewSet, UsersViewSet

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('users', UsersViewSet, basename='users')

urlpatterns = router.urls
