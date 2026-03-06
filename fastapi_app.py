from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from asgiref.sync import sync_to_async
from django.db import models

from lidera.models import Representante, SolicitudCupo, Alumno, Inscripcion

app = FastAPI(
    title="Lidera API",
    description="API FastAPI para acceder a datos de Django",
    version="1.0.0"
)

class RepresentanteOut(BaseModel):
    id: int
    nombre_completo: str
    cedula: str
    correo: str
    celular: str
    
    class Config:
        from_attributes = True

class RepresentanteDetalleOut(BaseModel):
    id: int
    cedula: str
    nacionalidad: str
    nombres: str
    apellidos: str
    fecha_nacimiento: str
    sexo: str
    estado_civil: str
    correo: str
    celular: str
    telefono_habitacion: str
    direccion: str
    
    class Config:
        from_attributes = True

class SolicitudOut(BaseModel):
    id: int
    representante: str
    alumno: str
    grado: str
    estado: str
    fecha: str
    
    class Config:
        from_attributes = True

def get_all_representantes():
    """Función síncrona para obtener representantes"""
    representantes = Representante.objects.all()
    result = []
    for r in representantes:
        result.append({
            "id": r.id_representante,
            "nombre_completo": f"{r.nombres} {r.apellidos}",
            "cedula": r.cedula,
            "correo": r.correo,
            "celular": r.celular
        })
    return result

def get_representante_by_id(representante_id):
    """Función síncrona para obtener un representante por ID"""
    try:
        r = Representante.objects.get(id_representante=representante_id)
        return {
            "id": r.id_representante,
            "cedula": r.cedula,
            "nacionalidad": r.nacionalidad,
            "nombres": r.nombres,
            "apellidos": r.apellidos,
            "fecha_nacimiento": r.fecha_nacimiento.isoformat(),
            "sexo": r.sexo,
            "estado_civil": r.estado_civil or "",
            "correo": r.correo,
            "celular": r.celular,
            "telefono_habitacion": r.tel_habitacion or "",
            "direccion": r.direccion_habitacion
        }
    except Representante.DoesNotExist:
        return None

def get_all_solicitudes():
    """Función síncrona para obtener solicitudes"""
    solicitudes = SolicitudCupo.objects.select_related('id_representante').all()
    result = []
    for s in solicitudes:
        result.append({
            "id": s.id_solicitud,
            "representante": f"{s.id_representante.nombres} {s.id_representante.apellidos}",
            "alumno": f"{s.nombres_alumno} {s.apellidos_alumno}",
            "grado": s.grado_a_cursar,
            "estado": s.estado_solicitud,
            "fecha": s.fecha_creacion.isoformat() if s.fecha_creacion else None
        })
    return result

def get_solicitud_by_id(solicitud_id):
    """Función síncrona para obtener una solicitud por ID"""
    try:
        s = SolicitudCupo.objects.select_related('id_representante').get(id_solicitud=solicitud_id)
        return {
            "id": s.id_solicitud,
            "representante": f"{s.id_representante.nombres} {s.id_representante.apellidos}",
            "representante_id": s.id_representante.id_representante,
            "alumno": f"{s.nombres_alumno} {s.apellidos_alumno}",
            "fecha_nacimiento_alumno": s.fecha_nacimiento_alumno.isoformat(),
            "sexo_alumno": s.sexo_alumno,
            "grado_a_cursar": s.grado_a_cursar,
            "año_escolar": s.año_escolar,
            "colegio_precedencia": s.colegio_precedencia,
            "parentesco": s.parentesco_representante,
            "estado": s.estado_solicitud,
            "fecha_creacion": s.fecha_creacion.isoformat()
        }
    except SolicitudCupo.DoesNotExist:
        return None

def count_representantes():
    """Contar representantes (para debug)"""
    return Representante.objects.count()

@app.get("/")
async def root():
    return {
        "message": "API de Gestión Escolar",
        "endpoints_disponibles": [
            "/representantes/",
            "/representantes/{id}",
            "/solicitudes/",
            "/solicitudes/{id}",
            "/alumnos/",
            "/inscripciones/",
            "/docs",
            "/redoc",
            "/debug"
        ]
    }

@app.get("/debug/") #Indica si la BD Django está conectada correctamente y cuántos representantes hay
async def debug():
    """Endpoint de depuración para verificar conexión"""
    try:
        count = await sync_to_async(count_representantes)()
        return {
            "status": "ok",
            "representantes_en_bd": count,
            "django_connected": True
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "django_connected": False
        }

@app.get("/representantes/")
async def get_representantes():
    """Obtener todos los representantes"""
    try:
        # Usamos sync_to_async para ejecutar la función síncrona en un hilo separado
        representantes = await sync_to_async(get_all_representantes)()
        return representantes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener representantes: {str(e)}")

@app.get("/representantes/{representante_id}")
async def get_representante(representante_id: int):
    """Obtener un representante por ID"""
    try:
        representante = await sync_to_async(get_representante_by_id)(representante_id)
        if representante is None:
            raise HTTPException(status_code=404, detail="Representante no encontrado")
        return representante
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener representante: {str(e)}")

@app.get("/solicitudes/")
async def get_solicitudes():
    """Obtener todas las solicitudes de cupo"""
    try:
        solicitudes = await sync_to_async(get_all_solicitudes)()
        return solicitudes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitudes: {str(e)}")

@app.get("/solicitudes/{solicitud_id}")
async def get_solicitud(solicitud_id: int):
    """Obtener una solicitud por ID"""
    try:
        solicitud = await sync_to_async(get_solicitud_by_id)(solicitud_id)
        if solicitud is None:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener solicitud: {str(e)}")

@app.get("/alumnos/")
async def get_alumnos():
    """Obtener todos los alumnos"""
    try:
        @sync_to_async
        def get_alumnos_sync():
            alumnos = Alumno.objects.all()
            return [
                {
                    "id": a.id_alumno,
                    "nombre_completo": f"{a.nombres} {a.apellidos}",
                    "cedula_escolar": a.cedula_escolar,
                    "fecha_nacimiento": a.fecha_nacimiento.isoformat()
                }
                for a in alumnos
            ]
        
        alumnos = await get_alumnos_sync()
        return alumnos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener alumnos: {str(e)}")

@app.get("/inscripciones/")
async def get_inscripciones():
    """Obtener todas las inscripciones"""
    try:
        @sync_to_async
        def get_inscripciones_sync():
            inscripciones = Inscripcion.objects.select_related('id_alumno').all()
            return [
                {
                    "id": i.id_inscripcion,
                    "alumno": f"{i.id_alumno.nombres} {i.id_alumno.apellidos}",
                    "periodo": i.periodo_academico,
                    "grado": i.grado_cursado,
                    "monto": float(i.monto_total),
                    "estatus_pago": i.estatus_pago
                }
                for i in inscripciones
            ]
        
        inscripciones = await get_inscripciones_sync()
        return inscripciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener inscripciones: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)