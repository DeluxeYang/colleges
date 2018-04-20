from django.urls import include, path
from django.contrib import admin
from django.views.static import serve

from basic.views import test
from college.settings import MEDIA_ROOT


urlpatterns = [
    path('upload/<str:path>/', serve, {'document_root': MEDIA_ROOT}),
    path(r'admin/', admin.site.urls),

    path('backend/', include('backend.urls')),
    path('api/', include('api.urls')),

    path('test/', test.test),
    path('ueditor/', include('DjangoUeditor.urls')),
]
