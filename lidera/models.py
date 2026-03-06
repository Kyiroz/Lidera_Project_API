from django.db import models

class Representante(models.Model):
    #'Como se guarda en la BD', 'Como lo ve el usuario'
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('S', 'Soltero/a'),
        ('C', 'Casado/a'),
        ('D', 'Divorciado/a'),
        ('V', 'Viudo/a'),
        ('U', 'Unión Libre'),
    ]
    
    NACIONALIDAD_CHOICES = [
        ('V', 'Venezolano'),
        ('E', 'Extranjero'),
        ('P', 'Pasaporte'),
    ]
    
    NIVEL_EDUCATIVO_CHOICES = [
        ('basica', 'Educación Básica'),
        ('media', 'Educación Media'),
        ('tsp', 'Técnico Superior'),
        ('lic', 'Licenciatura'),
        ('ing', 'Ingeniería'),
        ('postgrado', 'Postgrado'),
        ('maestria', 'Maestría'),
        ('doctorado', 'Doctorado'),
    ]
    
    # Identificación
    id_representante = models.AutoField(primary_key=True)
    cedula = models.CharField(max_length=8, unique=True, verbose_name="Cédula de Identidad")
    nacionalidad = models.CharField(max_length=10, choices=NACIONALIDAD_CHOICES, verbose_name="Nacionalidad")
    nombres = models.CharField(max_length=20, verbose_name="Nombres")
    apellidos = models.CharField(max_length=20, verbose_name="Apellidos")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL_CHOICES, verbose_name="Estado Civil")
    
    # Datos de contacto
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    celular = models.CharField(max_length=20, verbose_name="Teléfono Celular")
    tel_habitacion = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de Habitación")
    
    # Dirección de habitación
    direccion_habitacion = models.TextField(verbose_name="Dirección de Habitación")
    codigo_postal = models.CharField(max_length=20, verbose_name="Código Postal")
    municipio = models.CharField(max_length=100, verbose_name="Municipio")
    estado = models.CharField(max_length=100, verbose_name="Estado")
    pais = models.CharField(max_length=100, verbose_name="País")
    
    # Lugar de nacimiento
    pais_nacimiento = models.CharField(max_length=100, verbose_name="País de Nacimiento")
    ciudad_nacimiento = models.CharField(max_length=100, verbose_name="Ciudad de Nacimiento")
    
    # Información adicional
    otras_nacionalidades = models.TextField(blank=True, null=True, verbose_name="Otras Nacionalidades")
    idiomas = models.TextField(blank=True, null=True, help_text="Separar por comas", verbose_name="Idiomas")
    religion = models.CharField(max_length=100, blank=True, verbose_name="Religión")
    nivel_educativo = models.CharField(max_length=20, choices=NIVEL_EDUCATIVO_CHOICES, verbose_name="Nivel Educativo")
    profesion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profesión")
    ocupacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ocupación")
    
    # Datos laborales
    empresa_trabajo = models.CharField(max_length=200, blank=True, null=True, verbose_name="Empresa donde Trabaja")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo")
    direccion_trabajo = models.TextField(blank=True, null=True, verbose_name="Dirección de Trabajo")
    estado_trabajo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado (Trabajo)")
    pais_trabajo = models.CharField(max_length=100, blank=True, null=True, verbose_name="País (Trabajo)")
    tel_oficina = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono de Oficina")
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    
    class Meta:
        verbose_name = "Representante"
        verbose_name_plural = "Representantes"
        ordering = ['apellidos', 'nombres']
    
    def __str__(self):
        return f"{self.apellidos}, {self.nombres} - {self.cedula}"

class SolicitudCupo(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
        ('EN_REVISION', 'En Revisión'),
    ]
    
    PARENTESCO_CHOICES = [
        ('PADRE', 'Padre'),
        ('MADRE', 'Madre'),
        ('TUTOR', 'Tutor Legal'),
        ('OTRO', 'Otro'),
    ]
    
    id_solicitud = models.AutoField(primary_key=True)
    id_representante = models.ForeignKey(
        Representante, 
        on_delete=models.CASCADE, 
        db_column='id_representante'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES,
        default='PENDIENTE'
    )
    
    # Datos básicos del alumno
    nombres_alumno = models.CharField(max_length=100)
    apellidos_alumno = models.CharField(max_length=100)
    fecha_nacimiento_alumno = models.DateField()
    sexo_alumno = models.CharField(max_length=1, choices=Representante.SEXO_CHOICES)
    grado_a_cursar = models.CharField(max_length=50)
    año_escolar = models.CharField(max_length=20)
    colegio_precedencia = models.CharField(max_length=200)
    parentesco_representante = models.CharField(
        max_length=20, 
        choices=PARENTESCO_CHOICES
    )
    
    class Meta:
        db_table = 'solicitud_cupo'
        verbose_name = 'Solicitud de Cupo'
        verbose_name_plural = 'Solicitudes de Cupo'
    
    def __str__(self):
        return f"Solicitud {self.id_solicitud} - {self.nombres_alumno} {self.apellidos_alumno}"

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    cedula_escolar = models.CharField(max_length=50, unique=True)
    cedula = models.CharField(max_length=20, blank=True, null=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=Representante.SEXO_CHOICES)
    pais = models.CharField(max_length=100)
    ciudad_nacimiento = models.CharField(max_length=100)
    otras_nacionalidades = models.TextField(blank=True)
    idiomas = models.TextField(blank=True)
    direccion = models.TextField()
    codigo_postal = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais_residencia = models.CharField(max_length=100)
    telefono_habitacion = models.CharField(max_length=20, blank=True)
    telefono_celular = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'alumno'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula_escolar}"

class DatosFacturacion(models.Model):
    id_datos_facturacion = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=200)
    rif = models.CharField(max_length=20)
    direccion_fiscal = models.TextField()
    correo_facturacion = models.EmailField()
    
    class Meta:
        db_table = 'datos_facturacion'
        verbose_name = 'Datos de Facturación'
        verbose_name_plural = 'Datos de Facturación'

class Inscripcion(models.Model):
    ESTADO_PAGO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Pago Parcial'),
        ('COMPLETO', 'Completo'),
        ('CONFIRMADO', 'Confirmado'),
    ]
    
    id_inscripcion = models.AutoField(primary_key=True)
    id_alumno = models.ForeignKey(
        Alumno, 
        on_delete=models.CASCADE, 
        db_column='id_alumno'
    )
    id_datos_facturacion = models.ForeignKey(
        DatosFacturacion, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_datos_facturacion'
    )
    periodo_academico = models.CharField(max_length=50)
    grado_cursado = models.CharField(max_length=50)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estatus_pago = models.CharField(
        max_length=20, 
        choices=ESTADO_PAGO_CHOICES,
        default='PENDIENTE'
    )
    fecha_pago_confirmado = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'inscripcion'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
    
    def __str__(self):
        return f"Inscripción {self.id_inscripcion} - {self.id_alumno}"