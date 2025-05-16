from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobs.urls')),  # This will make the home page the root URL
    path('api/jobs/', include('jobs.urls')),  # This will handle API endpoints
]