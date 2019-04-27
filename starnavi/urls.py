from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_swagger.views import get_swagger_view

from posts.views import CustomUserCreateViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/createuser', CustomUserCreateViewSet)
router.register(r'api/v1/posts', PostViewSet)

schema_view = get_swagger_view(title='Posts API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('schema/', schema_view),
]
