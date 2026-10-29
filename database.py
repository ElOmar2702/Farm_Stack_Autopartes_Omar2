from typing import List
from models import Repuesto
from uuid import uuid4

# Lista global que actúa como nuestra tabla en memoria
db_repuestos: List[Repuesto] = []

def cargar_datos_semilla():
    """Carga registros iniciales de prueba al iniciar la API"""
    if not db_repuestos:
        db_repuestos.extend([
            Repuesto(
                id=uuid4(),
                repuesto="Kit de Embrague Completo",
                modelo_compatible="Renault Logan / Sandero",
                precio=450000.0,
                disponible=True
            ),
            Repuesto(
                id=uuid4(),
                repuesto="Amortiguadores Delanteros",
                modelo_compatible="Chevrolet Spark GT",
                precio=320000.0,
                disponible=True
            ),
            Repuesto(
                id=uuid4(),
                repuesto="Filtro de Aceite",
                modelo_compatible="Mazda 3 Skyactiv",
                precio=45000.0,
                disponible=False
            )
        ])