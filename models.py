from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4

class RepuestoBase(BaseModel):
    repuesto: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del repuesto o autoparte",
        example="Kit de Embrague Completo"
    )
    modelo_compatible: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Modelo de vehículo compatible",
        example="Renault Logan / Sandero"
    )
    precio: float = Field(
        ...,
        gt=0,
        description="Precio unitario. Debe ser estrictamente mayor a 0",
        example=450000.0
    )
    disponible: bool = Field(
        default=True,
        description="Estado de disponibilidad en el inventario"
    )

class RepuestoCreate(RepuestoBase):
    """Modelo utilizado para recibir solicitudes POST de creación"""
    pass

class RepuestoUpdate(BaseModel):
    """Modelo para solicitudes PUT (Campos opcionales para edición parcial)"""
    repuesto: Optional[str] = Field(None, min_length=2, max_length=100)
    modelo_compatible: Optional[str] = Field(None, min_length=2, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    disponible: Optional[bool] = None

class Repuesto(RepuestoBase):
    """Modelo completo de respuesta que incluye el ID único autogenerado (UUIDv4)"""
    id: UUID = Field(default_factory=uuid4, description="Identificador Único Universal")

    class Config:
        from_attributes = True