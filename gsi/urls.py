from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include(('eptGSI.urls', 'gsi'),namespace='gsi')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="EPT GESTION ET SUIVI DES IMMERSIONS"
admin.site.site_title="GSI"
admin.site.index_title="Interface d'administration GSI"

