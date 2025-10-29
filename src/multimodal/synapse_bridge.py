"""
SynapseBridge - Puente de comunicación multimodal
Sincroniza contexto entre texto, imagen y audio para comprensión unificada
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import deque

from ..core.event_bus import EventBus, Event


class SynapseBridge:
    """
    Puente sináptico que conecta modalidades (texto, visión, audio).
    Mantiene contexto compartido y sincroniza información multimodal.
    Inspirado en arquitecturas como CLIP para embeddings unificados.
    """
    
    def __init__(self, event_bus: EventBus, context_window: int = 50):
        self.event_bus = event_bus
        self.context_window = context_window
        
        # Contexto compartido entre modalidades
        self.shared_context = {
            "vision": deque(maxlen=context_window),
            "audio": deque(maxlen=context_window),
            "text": deque(maxlen=context_window),
            "unified": deque(maxlen=context_window)
        }
        
        # Registro de sincronizaciones
        self._sync_history = []
        
        # Suscribirse a eventos multimodales
        self.event_bus.subscribe("vision_data", self._on_vision_data)
        self.event_bus.subscribe("audio_data", self._on_audio_data)
        self.event_bus.subscribe("text_data", self._on_text_data)
        self.event_bus.subscribe("perception_received", self._on_perception)
        
    async def _on_vision_data(self, event: Event) -> None:
        """Handler para datos de visión"""
        data = event.data
        self.shared_context["vision"].append({
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "source": event.source
        })
        await self._sync_context("vision", data)
        
    async def _on_audio_data(self, event: Event) -> None:
        """Handler para datos de audio"""
        data = event.data
        self.shared_context["audio"].append({
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "source": event.source
        })
        await self._sync_context("audio", data)
        
    async def _on_text_data(self, event: Event) -> None:
        """Handler para datos de texto"""
        data = event.data
        self.shared_context["text"].append({
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "source": event.source
        })
        await self._sync_context("text", data)
        
    async def _on_perception(self, event: Event) -> None:
        """Handler para percepciones generales del núcleo cognitivo"""
        data = event.data
        
        # Clasificar percepción por modalidad
        if "sensor" in str(data).lower():
            sensor_data = data.get("data", {})
            if "image" in str(sensor_data) or "vision" in str(sensor_data):
                await self._on_vision_data(event)
            elif "audio" in str(sensor_data) or "sound" in str(sensor_data):
                await self._on_audio_data(event)
            else:
                # Por defecto, tratar como texto
                self.shared_context["text"].append({
                    "data": data,
                    "timestamp": datetime.now().isoformat(),
                    "source": event.source
                })
                
    async def _sync_context(self, modality: str, data: Any) -> None:
        """
        Sincronizar contexto entre modalidades.
        Aquí es donde se implementaría la lógica de embeddings unificados.
        """
        # Crear entrada unificada
        unified_entry = {
            "modality": modality,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "embedding": await self._create_embedding(modality, data)
        }
        
        self.shared_context["unified"].append(unified_entry)
        
        # Registrar sincronización
        sync_record = {
            "modality": modality,
            "timestamp": datetime.now().isoformat(),
            "context_state": {
                "vision_count": len(self.shared_context["vision"]),
                "audio_count": len(self.shared_context["audio"]),
                "text_count": len(self.shared_context["text"])
            }
        }
        self._sync_history.append(sync_record)
        
        # Emitir evento de sincronización
        await self.event_bus.emit(
            "synapse_sync",
            {
                "modality": modality,
                "context_state": sync_record["context_state"]
            },
            source="synapse_bridge"
        )
        
        if len(self._sync_history) > 1000:
            self._sync_history = self._sync_history[-500:]
            
    async def _create_embedding(self, modality: str, data: Any) -> Dict[str, Any]:
        """
        Crear embedding unificado para la modalidad.
        TODO: Integrar con CLIP, CLAP u otros modelos de embeddings multimodales.
        Por ahora retorna representación simbólica.
        """
        # Representación simbólica simple
        if modality == "vision":
            prompt = data.get("prompt", "") if isinstance(data, dict) else str(data)
            return {
                "type": "vision_embedding",
                "dimension": 512,  # Dimensión típica de CLIP
                "representation": f"<vision_emb:{prompt[:20]}...>",
                "model": "symbolic"
            }
        elif modality == "audio":
            text = data.get("text", "") if isinstance(data, dict) else str(data)
            return {
                "type": "audio_embedding",
                "dimension": 512,
                "representation": f"<audio_emb:{text[:20]}...>",
                "model": "symbolic"
            }
        elif modality == "text":
            text = str(data)
            return {
                "type": "text_embedding",
                "dimension": 512,
                "representation": f"<text_emb:{text[:20]}...>",
                "model": "symbolic"
            }
        else:
            return {
                "type": "unknown_embedding",
                "dimension": 512,
                "representation": "<unknown>",
                "model": "symbolic"
            }
            
    def get_unified_context(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener contexto unificado reciente"""
        unified_list = list(self.shared_context["unified"])
        return unified_list[-limit:] if unified_list else []
        
    def get_context_by_modality(self, modality: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener contexto de una modalidad específica"""
        if modality not in self.shared_context:
            return []
        context_list = list(self.shared_context[modality])
        return context_list[-limit:] if context_list else []
        
    async def cross_modal_search(self, query: str, modality: str = "all") -> List[Dict[str, Any]]:
        """
        Búsqueda cross-modal: buscar en una modalidad usando query de otra.
        Ejemplo: buscar imágenes usando descripción de texto.
        TODO: Implementar con embeddings reales y similitud coseno.
        """
        results = []
        
        if modality == "all":
            # Buscar en todas las modalidades
            for mod in ["vision", "audio", "text"]:
                results.extend(self.get_context_by_modality(mod, limit=5))
        else:
            results = self.get_context_by_modality(modality, limit=10)
            
        return results
        
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del puente sináptico"""
        return {
            "context_sizes": {
                "vision": len(self.shared_context["vision"]),
                "audio": len(self.shared_context["audio"]),
                "text": len(self.shared_context["text"]),
                "unified": len(self.shared_context["unified"])
            },
            "sync_events": len(self._sync_history),
            "context_window": self.context_window,
            "last_sync": self._sync_history[-1] if self._sync_history else None
        }
