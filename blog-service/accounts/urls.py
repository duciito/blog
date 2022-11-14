# accounts/urls.py
from rest_framework import routers
from accounts.views import UsersViewSet

app_name = 'accounts'

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')

urlpatterns = router.urls
