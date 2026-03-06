> [!IMPORTANT]
> Importante:

> 1. Crear y activar entorno virtual

python -m venv .venv

>> Windows:

.venv\Scripts\activate

>> Mac/Linux:

source .venv/bin/activate

> 2. Instalar dependencias

pip install -r requirements.txt

> 3. Iniciar servidores

>> Terminal 1 - Django:

python manage.py runserver

>> Terminal 2 - FastAPI:

uvicorn fastapi_app:app --reload --port 8001

> [!NOTE]
> Si se hizo un cambio en models.py:

python manage.py makemigrations lidera

python manage.py migrate
