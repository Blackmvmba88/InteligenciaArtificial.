"""
Event Bus - Sistema asincrónico de eventos para arquitectura modular
"""
import asyncio
from collections import defaultdict
from typing import Callable, Any, Dict, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Event:
    """Evento base del sistema"""
    type: str
    data: Any
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = "unknown"


class EventBus:
    """
    Bus de eventos asincrónico para comunicación entre módulos.
    Permite arquitectura desacoplada y reactiva.
    """
    
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._event_queue: asyncio.Queue = asyncio.Queue()
        self._running = False
        
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Suscribir un callback a un tipo de evento"""
        self._listeners[event_type].append(callback)
        
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Cancelar suscripción"""
        if event_type in self._listeners:
            self._listeners[event_type].remove(callback)
            
    async def publish(self, event: Event) -> None:
        """Publicar un evento en el bus"""
        await self._event_queue.put(event)
        
    async def emit(self, event_type: str, data: Any, source: str = "system") -> None:
        """Conveniencia para crear y publicar evento"""
        event = Event(type=event_type, data=data, source=source)
        await self.publish(event)
        
    async def start(self) -> None:
        """Iniciar el procesamiento de eventos"""
        self._running = True
        while self._running:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=0.1)
                await self._dispatch(event)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                print(f"Error processing event: {e}")
                
    async def _dispatch(self, event: Event) -> None:
        """Despachar evento a todos los listeners registrados"""
        listeners = self._listeners.get(event.type, [])
        for callback in listeners:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                print(f"Error in event handler for {event.type}: {e}")
                
    def stop(self) -> None:
        """Detener el procesamiento de eventos"""
        self._running = False
