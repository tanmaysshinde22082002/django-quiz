from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Quizproject.Quizproject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),  # this line is important!
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)