from fastapi import FastAPI, HTTPException, status
from typing import List
from uuid import UUID
from models import Repuesto, RepuestoCreate, RepuestoUpdate
from database import db_repuestos, cargar_datos_semilla

app = FastAPI(
    title="API Inventario de Repuestos de Autos",
    description="API RESTful para la gestión de autopartes con Pydantic y FastAPI.",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    cargar_datos_semilla()

@app.get("/", tags=["General"], summary="Raíz de la API")
def read_root():
    return {
        "mensaje": "Bienvenido a la API de Inventario de Repuestos de Autos",
        "documentacion": "/docs"
    }

@app.get("/repuestos", response_model=List[Repuesto], tags=["Repuestos"], summary="Listar todos los repuestos")
def obtener_repuestos():
    return db_repuestos

@app.get("/repuestos/{repuesto_id}", response_model=Repuesto, tags=["Repuestos"], summary="Buscar repuesto por ID")
def obtener_repuesto_por_id(repuesto_id: UUID):
    for rep in db_repuestos:
        if rep.id == repuesto_id:
            return rep
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El repuesto con ID '{repuesto_id}' no fue encontrado en el inventario."
    )

@app.post("/repuestos", response_model=Repuesto, status_code=status.HTTP_201_CREATED, tags=["Repuestos"], summary="Crear un nuevo repuesto")
def crear_repuesto(repuesto_in: RepuestoCreate):
    # Validación de duplicados por nombre y modelo compatible
    for rep in db_repuestos:
        if (rep.repuesto.strip().lower() == repuesto_in.repuesto.strip().lower() and 
            rep.modelo_compatible.strip().lower() == repuesto_in.modelo_compatible.strip().lower()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El repuesto '{repuesto_in.repuesto}' para el modelo '{repuesto_in.modelo_compatible}' ya se encuentra registrado."
            )
    
    nuevo_repuesto = Repuesto(**repuesto_in.model_dump())
    db_repuestos.append(nuevo_repuesto)
    return nuevo_repuesto

@app.put("/repuestos/{repuesto_id}", response_model=Repuesto, tags=["Repuestos"], summary="Actualizar un repuesto existente")
def actualizar_repuesto(repuesto_id: UUID, repuesto_in: RepuestoUpdate):
    for index, rep in enumerate(db_repuestos):
        if rep.id == repuesto_id:
            datos_actualizacion = repuesto_in.model_dump(exclude_unset=True)
            repuesto_actualizado = rep.model_copy(update=datos_actualizacion)
            db_repuestos[index] = repuesto_actualizado
            return repuesto_actualizado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El repuesto con ID '{repuesto_id}' no fue encontrado para actualizar."
    )

@app.delete("/repuestos/{repuesto_id}", response_model=dict, tags=["Repuestos"], summary="Eliminar un repuesto")
def eliminar_repuesto(repuesto_id: UUID):
    for index, rep in enumerate(db_repuestos):
        if rep.id == repuesto_id:
            repuesto_eliminado = db_repuestos.pop(index)
            return {
                "mensaje": f"El repuesto '{repuesto_eliminado.repuesto}' fue eliminado exitosamente.",
                "id": str(repuesto_id)
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El repuesto con ID '{repuesto_id}' no fue encontrado para eliminar."
    )