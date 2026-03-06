from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lidera.views import (
    RepresentanteViewSet, SolicitudCupoViewSet,
    AlumnoViewSet, InscripcionViewSet
)

router = DefaultRouter()
router.register(r'representantes', RepresentanteViewSet)
router.register(r'solicitudes', SolicitudCupoViewSet)
router.register(r'alumnos', AlumnoViewSet)
router.register(r'inscripciones', InscripcionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]