"""
Actuators - Abstracción de salida para acciones del sistema cognitivo
"""
import asyncio
from abc import ABC, abstractmethod
from typing import Any, Dict
from datetime import datetime

from ..core.event_bus import EventBus, Event


class Actuator(ABC):
    """Clase base para actuadores"""
    
    def __init__(self, name: str, event_bus: EventBus):
        self.name = name
        self.event_bus = event_bus
        self._action_count = 0
        
        # Suscribirse a eventos de acción
        self.event_bus.subscribe("action_requested", self._on_action_requested)
        
    async def _on_action_requested(self, event: Event) -> None:
        """Handler para eventos de acción"""
        action = event.data
        if self._should_handle(action):
            await self.act(action)
            
    def _should_handle(self, action: Dict) -> bool:
        """Determinar si este actuador debe manejar la acción"""
        # Por defecto, manejar todas las acciones
        # Las subclases pueden override para filtrar
        return True
        
    @abstractmethod
    async def act(self, action: Dict) -> None:
        """Ejecutar una acción"""
        pass
        
    def get_statistics(self) -> Dict:
        """Obtener estadísticas del actuador"""
        return {
            "name": self.name,
            "actions_performed": self._action_count
        }


class LogActuator(Actuator):
    """
    Actuador que registra acciones en un archivo de log.
    Útil para auditoría y debugging.
    """
    
    def __init__(self, name: str, event_bus: EventBus, log_file: str = "actions.log"):
        super().__init__(name, event_bus)
        self.log_file = log_file
        
    async def act(self, action: Dict) -> None:
        """Registrar acción en archivo de log"""
        self._action_count += 1
        log_entry = f"[{datetime.now().isoformat()}] {self.name}: {action}\n"
        
        try:
            # Escribir de forma asíncrona
            await asyncio.get_event_loop().run_in_executor(
                None,
                self._write_log,
                log_entry
            )
        except Exception as e:
            print(f"Error writing to log: {e}")
            
    def _write_log(self, entry: str) -> None:
        """Escribir entrada en el log"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry)


class ConsoleActuator(Actuator):
    """
    Actuador que muestra acciones en la consola.
    Útil para debugging y demostraciones.
    """
    
    def __init__(self, name: str, event_bus: EventBus, verbose: bool = True):
        super().__init__(name, event_bus)
        self.verbose = verbose
        
    async def act(self, action: Dict) -> None:
        """Mostrar acción en consola"""
        self._action_count += 1
        
        if self.verbose:
            print(f"\n[{self.name}] Ejecutando acción:")
            print(f"  Tipo: {action.get('action', 'unknown')}")
            print(f"  Confianza: {action.get('confidence', 'N/A')}")
            if 'reason' in action:
                print(f"  Razón: {action['reason']}")
            print(f"  Timestamp: {datetime.now().isoformat()}")
        else:
            print(f"[{self.name}] Acción: {action.get('action', 'unknown')}")


class StateActuator(Actuator):
    """
    Actuador que mantiene estado interno y puede modificarlo.
    Útil para simulaciones y control de estado.
    """
    
    def __init__(self, name: str, event_bus: EventBus):
        super().__init__(name, event_bus)
        self._state = {}
        
    async def act(self, action: Dict) -> None:
        """Actualizar estado basado en acción"""
        self._action_count += 1
        
        action_type = action.get('action', 'unknown')
        
        # Procesar diferentes tipos de acciones
        if action_type == "set_state":
            key = action.get('key')
            value = action.get('value')
            if key:
                self._state[key] = value
                
        elif action_type == "clear_state":
            self._state.clear()
            
        elif action_type == "increment":
            key = action.get('key', 'counter')
            self._state[key] = self._state.get(key, 0) + 1
            
        # Emitir evento de cambio de estado
        await self.event_bus.emit(
            "state_changed",
            {"actuator": self.name, "state": self._state.copy()},
            source=self.name
        )
        
    def get_state(self) -> Dict:
        """Obtener estado actual"""
        return self._state.copy()
