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
    
    def __init__(self, max_queue_size: int = 1000):
        """
        Inicializar EventBus con límite de cola configurable
        
        Args:
            max_queue_size: Tamaño máximo de la cola de eventos (default: 1000)
        """
        if max_queue_size <= 0:
            raise ValueError("max_queue_size debe ser positivo")
        
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._event_queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self._running = False
        
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Suscribir un callback a un tipo de evento
        
        Args:
            event_type: Tipo de evento a escuchar
            callback: Función a ejecutar cuando ocurra el evento
        
        Raises:
            ValueError: Si event_type está vacío o callback no es callable
        """
        if not event_type or not isinstance(event_type, str):
            raise ValueError("event_type debe ser una cadena no vacía")
        if not callable(callback):
            raise ValueError("callback debe ser una función callable")
        
        self._listeners[event_type].append(callback)
        
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """
        Cancelar suscripción de un callback
        
        Args:
            event_type: Tipo de evento
            callback: Función a desuscribir
        """
        if not event_type or not isinstance(event_type, str):
            raise ValueError("event_type debe ser una cadena no vacía")
        
        if event_type in self._listeners and callback in self._listeners[event_type]:
            self._listeners[event_type].remove(callback)
            
    async def publish(self, event: Event) -> None:
        """
        Publicar un evento en el bus
        
        Args:
            event: Evento a publicar
        
        Raises:
            ValueError: Si event no es una instancia de Event
        """
        if not isinstance(event, Event):
            raise ValueError("event debe ser una instancia de Event")
        
        try:
            await asyncio.wait_for(self._event_queue.put(event), timeout=1.0)
        except asyncio.TimeoutError:
            print(f"Warning: Event queue full, dropping event of type {event.type}")
        
    async def emit(self, event_type: str, data: Any, source: str = "system") -> None:
        """
        Conveniencia para crear y publicar evento
        
        Args:
            event_type: Tipo de evento
            data: Datos del evento
            source: Origen del evento (default: "system")
        
        Raises:
            ValueError: Si event_type está vacío
        """
        if not event_type or not isinstance(event_type, str):
            raise ValueError("event_type debe ser una cadena no vacía")
        
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
