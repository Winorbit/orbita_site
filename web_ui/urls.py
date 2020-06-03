from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('', include('webui.urls', namespace='orbita')),
    path('admin/', admin.site.urls),
]