# lidera/serializers.py
from rest_framework import serializers
from .models import (
    Representante, SolicitudCupo, 
    Alumno, DatosFacturacion, Inscripcion
)

class RepresentanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'

class SolicitudCupoSerializer(serializers.ModelSerializer):
    representante_detalle = RepresentanteSerializer(
        source='id_representante', 
        read_only=True
    )
    
    class Meta:
        model = SolicitudCupo
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

class DatosFacturacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatosFacturacion
        fields = '__all__'

class InscripcionSerializer(serializers.ModelSerializer):
    alumno_detalle = AlumnoSerializer(source='id_alumno', read_only=True)
    facturacion_detalle = DatosFacturacionSerializer(
        source='id_datos_facturacion', 
        read_only=True
    )
    
    class Meta:
        model = Inscripcion
        fields = '__all__'