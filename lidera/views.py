from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Representante, SolicitudCupo, Alumno, Inscripcion
from .serializers import (
    RepresentanteSerializer, SolicitudCupoSerializer, 
    AlumnoSerializer, InscripcionSerializer
)

class RepresentanteViewSet(viewsets.ModelViewSet):
    queryset = Representante.objects.all()
    serializer_class = RepresentanteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SolicitudCupoViewSet(viewsets.ModelViewSet):
    queryset = SolicitudCupo.objects.all()
    serializer_class = SolicitudCupoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]