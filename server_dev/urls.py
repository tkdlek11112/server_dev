from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="TO-DO API",  # 타이틀
        default_version='v1',   # 버전
        description="서버개발자가 되는법 #12",   # 설명
        terms_of_service="https://cholol.tistory.com/551",
        contact=openapi.Contact(email="mychew@kakao.com")
),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,)
)


urlpatterns = [
    # swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    # django
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('todo/', include('todo.urls')),
]
