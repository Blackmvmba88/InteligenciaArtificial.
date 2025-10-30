"""
Cognitive Core - Núcleo cognitivo con ciclo perceive → think → act
"""
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime

from .event_bus import EventBus, Event


class CognitiveCore:
    """
    Núcleo cognitivo que implementa el ciclo básico de IA:
    - Percepción: Recibir información del entorno
    - Pensamiento: Razonar sobre la información
    - Acción: Actuar sobre el entorno
    """
    
    def __init__(self, event_bus: EventBus, memory_module=None, reasoning_engine=None):
        self.event_bus = event_bus
        self.memory = memory_module
        self.reasoning = reasoning_engine
        self._state = "idle"
        self._perceptions: List[Any] = []
        self._running = False
        
        # Suscribirse a eventos de percepción
        self.event_bus.subscribe("perception", self._on_perception)
        self.event_bus.subscribe("sensor_data", self._on_perception)
        
    async def _on_perception(self, event: Event) -> None:
        """Handler para eventos de percepción"""
        await self.perceive(event.data, source=event.source)
        
    async def perceive(self, data: Any, source: str = "sensor") -> None:
        """
        Fase de percepción: Recibir y procesar información del entorno
        """
        perception = {
            "data": data,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
        
        self._perceptions.append(perception)
        
        # Guardar en memoria si disponible
        if self.memory:
            await self.memory.store("perception", perception)
            
        # Emitir evento de nueva percepción
        await self.event_bus.emit("perception_received", perception, source="cognitive_core")
        
    async def think(self) -> Optional[Dict]:
        """
        Fase de pensamiento: Razonar sobre percepciones recientes
        """
        if not self._perceptions:
            return None
            
        # Obtener contexto de memoria
        context = {}
        if self.memory:
            context = await self.memory.recall("recent_context") or {}
            
        # Razonar sobre percepciones
        thoughts = {
            "perceptions_count": len(self._perceptions),
            "recent_perceptions": self._perceptions[-5:],  # Últimas 5
            "context": context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Usar motor de razonamiento si disponible
        if self.reasoning:
            decision = await self.reasoning.reason(self._perceptions, context)
            thoughts["decision"] = decision
        else:
            # Razonamiento básico sin motor especializado
            thoughts["decision"] = {
                "action": "observe",
                "confidence": 0.5
            }
            
        # Emitir evento de pensamiento completado
        await self.event_bus.emit("thought_completed", thoughts, source="cognitive_core")
        
        return thoughts
        
    async def act(self, action: Dict) -> None:
        """
        Fase de acción: Ejecutar acciones en el entorno
        """
        action_event = {
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        # Guardar acción en memoria
        if self.memory:
            await self.memory.store("action", action_event)
            
        # Emitir evento de acción para actuadores
        await self.event_bus.emit("action_requested", action, source="cognitive_core")
        
    async def cognitive_cycle(self) -> None:
        """
        Ejecutar un ciclo cognitivo completo: perceive → think → act
        """
        # Pensar sobre percepciones recientes
        thoughts = await self.think()
        
        if thoughts and "decision" in thoughts:
            decision = thoughts["decision"]
            
            # Actuar basado en la decisión
            if decision.get("action") != "observe":
                await self.act(decision)
                
        # Limpiar percepciones antiguas
        if len(self._perceptions) > 100:
            self._perceptions = self._perceptions[-50:]
            
    async def run(self, cycle_interval: float = 1.0) -> None:
        """
        Ejecutar el núcleo cognitivo continuamente
        """
        self._running = True
        self._state = "running"
        
        await self.event_bus.emit("cognitive_core_started", {}, source="cognitive_core")
        
        try:
            while self._running:
                await self.cognitive_cycle()
                await asyncio.sleep(cycle_interval)
        finally:
            self._state = "stopped"
            await self.event_bus.emit("cognitive_core_stopped", {}, source="cognitive_core")
            
    def stop(self) -> None:
        """Detener el núcleo cognitivo"""
        self._running = False
        
    @property
    def state(self) -> str:
        """Estado actual del núcleo cognitivo"""
        return self._state
