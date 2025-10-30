"""
Sensors - Abstracción de entrada para el sistema cognitivo
"""
import asyncio
import random
from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime

from ..core.event_bus import EventBus


class Sensor(ABC):
    """Clase base para sensores"""
    
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.event_bus = event_bus
        self._running = False
        
    @abstractmethod
    async def read(self) -> Any:
        """Leer datos del sensor"""
        pass
        
    async def start(self, interval: float = 1.0) -> None:
        """Iniciar lectura continua del sensor"""
        self._running = True
        while self._running:
            try:
                data = await self.read()
                if data is not None:
                    await self.event_bus.emit(
                        "sensor_data",
                        {"sensor": self.name, "value": data},
                        source=self.name
                    )
            except Exception as e:
                print(f"Error reading sensor {self.name}: {e}")
                
            await asyncio.sleep(interval)
            
    def stop(self) -> None:
        """Detener el sensor"""
        self._running = False


class RandomSensor(Sensor):
    """
    Sensor de ejemplo que genera valores aleatorios.
    Útil para pruebas y demostraciones.
    """
    
    def __init__(self, name: str, event_bus: EventBus, min_val: float = 0, max_val: float = 100):
        super().__init__(name, event_bus)
        self.min_val = min_val
        self.max_val = max_val
        
    async def read(self) -> float:
        """Generar un valor aleatorio"""
        return random.uniform(self.min_val, self.max_val)


class TimeSensor(Sensor):
    """
    Sensor que reporta información temporal.
    Útil para tareas temporales y cronometraje.
    """
    
    def __init__(self, name: str, event_bus: EventBus):
        super().__init__(name, event_bus)
        
    async def read(self) -> dict:
        """Leer timestamp actual"""
        now = datetime.now()
        return {
            "timestamp": now.isoformat(),
            "hour": now.hour,
            "minute": now.minute,
            "second": now.second,
            "day_of_week": now.weekday()
        }


class InputSensor(Sensor):
    """
    Sensor que captura entrada del usuario.
    Útil para interacción humana.
    """
    
    def __init__(self, name: str, event_bus: EventBus):
        super().__init__(name, event_bus)
        self._input_queue = asyncio.Queue()
        
    async def read(self) -> str:
        """Leer entrada del usuario (no bloqueante)"""
        try:
            # Intentar obtener entrada sin bloquear indefinidamente
            data = await asyncio.wait_for(self._input_queue.get(), timeout=0.1)
            return data
        except asyncio.TimeoutError:
            return None
            
    async def provide_input(self, data: str) -> None:
        """Método para proporcionar entrada al sensor"""
        await self._input_queue.put(data)
