from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'expe'

urlpatterns = [
    path('', views.expe_list, name='expe_list'),
    path('expe', views.expe, name='expe'),
    path('indications', views.indications, name='indications'),
    path('admin/results', views.list_results, name='results'),
    path('admin/results/<str:expe>', views.list_results, name='results_expe'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)