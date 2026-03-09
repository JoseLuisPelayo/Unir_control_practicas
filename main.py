from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, create_engine, Session, Field, select
from seed_data import data_seed
from datetime import date
from docxtpl import DocxTemplate

class Alumno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellidos: str
    curso_academico: str
    email: str
    num_convenio: str
    num_anexo: str
    
class Centro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    nombre_tutor: str
    apellidos_tutor: str
    email_tutor: str
    
class Modulo(SQLModel, table=True):
    cod: str = Field(default=None, primary_key=True)
    nombre: str
    
class Ra(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str
    descripcion: str
    modulo_cod: str = Field(default=None, foreign_key="modulo.cod")
    
class Ce(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    codigo: str
    descripcion: str
    modulo_cod: str = Field(default=None, foreign_key="modulo.cod")
    ra_id: int = Field(default=None, foreign_key="ra.id")
    
class Activity(SQLModel):
    id: str
    descripcion: str
    cod_modulo: str
    cod_ra: str
    
class DocumentPayload(SQLModel):
    alumno: Alumno
    centro: Centro
    periodo_seguimiento_inicio: str
    periodo_seguimiento_fin: str
    activity_catalog: list[Activity]
    

engine = create_engine("sqlite:///database.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db(): 
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        ya_existen_modulos = session.exec(select(Modulo)).first()
        if not ya_existen_modulos:
            session.connection().connection.executescript(data_seed())
            session.commit()
            
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request, session: SessionDep):
    alumno = session.exec(select(Alumno)).first()
    centro = session.exec(select(Centro)).first()
    
    activity_catalog = []
    modulos = session.exec(select(Modulo)).all()
    for modulo in modulos:
        ras = session.exec(select(Ra).where(Ra.modulo_cod == modulo.cod)).all()

        activity_catalog.append(
            {
                "cod": modulo.cod,
                "nombre": modulo.nombre,
                "ras": [
                    {
                        "id": ra.id,
                        "codigo": ra.codigo,
                        "descripcion": ra.descripcion,
                    }
                    for ra in ras
                ],
            }
        )
        
    print(f"alumno: {alumno}")
    print(f"centro: {centro}")
        
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "activity_catalog": activity_catalog,
            "alumno": alumno,
            "centro": centro,
        },
    )

@app.post("/generate")
async def generate_document(
    payload: DocumentPayload,
    session: SessionDep
):
    try:
        print (f"Payload recibido: {payload}")
        
        if not check_periodo_seguimiento(payload.periodo_seguimiento_inicio, payload.periodo_seguimiento_fin):
            return "Periodo de seguimiento no válido: la fecha de inicio debe ser anterior a la fecha de fin."
        
        for activity in payload.activity_catalog:
            if not activity.descripcion or not activity.cod_modulo or not activity.cod_ra:
                return "Actividad no válida: todos los campos son obligatorios."
            
        save_constants(payload.alumno, payload.centro, session)
            
        doc = DocxTemplate("plantilla.docx")
        
        content =  {
            "curso_academico": payload.alumno.curso_academico,
            "nombre_alumno": payload.alumno.nombre,
            "apellidos_alumno": payload.alumno.apellidos,
            "num_convenio": payload.alumno.num_convenio,
            "num_anexo": payload.alumno.num_anexo,
            "email_alumno": payload.alumno.email,
            "centro_nombre": payload.centro.nombre,
            "apellidos_tutor": payload.centro.apellidos_tutor,
            "nombre_tutor": payload.centro.nombre_tutor,
            "email_tutor": payload.centro.email_tutor,
            "fecha_seguimiento_inicio": payload.periodo_seguimiento_inicio,
            "fecha_seguimiento_fin": payload.periodo_seguimiento_fin
        }
        
        for i, activity in enumerate(payload.activity_catalog):
            content[f"codigo_modulo_{ i + 1 }"] = activity.cod_modulo
            content[f"ra_{ i + 1 }"] = session.exec(select(Ra.codigo).where(Ra.id == activity.cod_ra)).first()
            content[f"descripcion_actividad_{ i + 1 }"] = activity.descripcion
        
        
        doc_title = f"{payload.alumno.nombre}_{payload.alumno.apellidos}_{payload.periodo_seguimiento_inicio}_{payload.periodo_seguimiento_fin}.docx".replace(" ", "_").upper() 
        
        doc.render(content)
        doc.save(f"{doc_title}")
        
    except Exception as e:
        print(f"Error al procesar el payload: {e}")
        return "Error al procesar el payload."
    

def save_constants(alumno: Alumno, centro: Centro, session: SessionDep):
    
    alumno_db =  session.exec(select(Alumno)).first()
    if alumno_db:
        alumno_db.nombre = alumno.nombre
        alumno_db.apellidos = alumno.apellidos
        alumno_db.curso_academico = alumno.curso_academico
        alumno_db.email = alumno.email
        alumno_db.num_convenio = alumno.num_convenio
        alumno_db.num_anexo = alumno.num_anexo
    else:
        alumno =  Alumno(
            nombre = alumno.nombre,
            apellidos = alumno.apellidos,
            curso_academico = alumno.curso_academico,
            email = alumno.email,
            num_convenio = alumno.num_convenio,
            num_anexo = alumno.num_anexo,
        )
        session.add(alumno)
    session.commit()
        
    centro_db = session.exec(select(Centro)).first()
    if centro_db:
        centro_db.nombre = centro.nombre
        centro_db.nombre_tutor = centro.nombre_tutor
        centro_db.apellidos_tutor = centro.apellidos_tutor
        centro_db.email_tutor = centro.email_tutor
    else:
        centro = Centro(
            nombre = centro.nombre,
            nombre_tutor = centro.nombre_tutor,
            apellidos_tutor = centro.apellidos_tutor,
            email_tutor = centro.email_tutor
        )
        session.add(centro)
    session.commit()

def check_periodo_seguimiento(fecha_inicio: date, fecha_fin: date) -> bool:
    return fecha_inicio <= fecha_fin 