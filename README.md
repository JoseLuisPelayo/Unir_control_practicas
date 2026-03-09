# Unir Control Practicas

FastAPI app for generating a follow-up document for student internships/practices. It collects student and center data, selects activities tied to modules and learning outcomes, and renders a docx using a template.

## Funcionalidad
- Formulario web con datos de alumno y centro.
- Catalogo de actividades por modulo y RA.
- Generacion de documento `.docx` desde `plantilla.docx`.
- Datos constantes (alumno/centro) almacenados en SQLite para recarga automatica.

## Requisitos
- Python 3.12 (ver `.python-version`).
- Gestor de dependencias: `uv` o `pip`.

## Instalacion
### Con uv (recomendado)
```bash
uv sync
```

### Con pip
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```
`requirements.txt` se incluye en el repo. Si necesitas regenerarlo:
```bash
pip install -U pip uv
uv pip compile pyproject.toml -o requirements.txt
```

## Uso
Iniciar el servidor en desarrollo:
```bash
uv run fastapi dev main.py
```

Alternativas:
```bash
uv run uvicorn main:app --reload
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

Luego abre `http://localhost:8000`.

Flujo principal:
1. Completa los datos del alumno y del centro.
2. Selecciona periodo de seguimiento y actividades.
3. Genera el documento.

El archivo generado se guarda en la raiz del proyecto con el formato:
`NOMBRE_APELLIDOS_FECHA_INICIO_FECHA_FIN.docx`.

## Estructura
- `main.py`: app FastAPI, modelos SQLModel, endpoints y logica de generacion.
- `seed_data.py`: datos iniciales de modulos y RAs.
- `templates/`: plantilla HTML (Jinja2).
- `static/`: JS y estilos.
- `database.db`: base de datos SQLite local.
- `plantilla.docx`: plantilla docx base.

## Contribucion
Las contribuciones son bienvenidas. Flujo recomendado:
1. Haz un fork del repositorio.
2. Crea una rama desde `main`: `git checkout -b feature/mi-cambio`.
3. Realiza cambios pequenos y enfocados.
4. Verifica el flujo principal (formulario y generacion de documento).
5. Haz commit con un mensaje claro.
6. Abre un Pull Request describiendo el cambio.

Guia rapida de estilo:
- Seguir PEP 8 y el orden de imports.
- Evitar introducir nuevas dependencias sin documentar comandos.

## Ideas y mejoras posibles
- Convertir la interfaz a aplicacion de escritorio (ej. Tauri, Electron o PySide).
- Validaciones mas completas (formatos, longitud, datos opcionales).
- Soporte para campos opcionales y secciones condicionales.
- Personalizacion de la plantilla docx por curso o centro.
