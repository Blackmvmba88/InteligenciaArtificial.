"""
Memory Module - Sistema de memoria persistente con JSON
"""
import json
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import deque


class MemoryModule:
    """
    Módulo de memoria con persistencia JSON.
    Implementa memoria de corto y largo plazo.
    """
    
    def __init__(self, memory_file: str = "memory_data.json", max_short_term: int = 100):
        self.memory_file = Path(memory_file)
        self.max_short_term = max_short_term
        
        # Memoria de corto plazo (en RAM)
        self._short_term: deque = deque(maxlen=max_short_term)
        
        # Memoria de largo plazo (persistente)
        self._long_term: Dict[str, List[Any]] = {}
        
        # Índice por tipo para búsquedas rápidas
        self._index_by_type: Dict[str, List[int]] = {}
        
        # Cargar memoria existente
        self._load()
        
    def _load(self) -> None:
        """Cargar memoria desde archivo JSON"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._long_term = data.get("long_term", {})
                    self._index_by_type = data.get("index", {})
            except Exception as e:
                print(f"Error loading memory: {e}")
                
    def _save(self) -> None:
        """Guardar memoria en archivo JSON"""
        try:
            data = {
                "long_term": self._long_term,
                "index": self._index_by_type,
                "last_saved": datetime.now().isoformat()
            }
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving memory: {e}")
            
    async def store(self, memory_type: str, data: Any) -> None:
        """
        Almacenar información en memoria
        """
        memory_entry = {
            "type": memory_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Añadir a memoria de corto plazo
        self._short_term.append(memory_entry)
        
        # Añadir a memoria de largo plazo
        if memory_type not in self._long_term:
            self._long_term[memory_type] = []
        
        self._long_term[memory_type].append(memory_entry)
        
        # Actualizar índice
        if memory_type not in self._index_by_type:
            self._index_by_type[memory_type] = []
        self._index_by_type[memory_type].append(len(self._long_term[memory_type]) - 1)
        
        # Guardar periódicamente (cada 10 entradas)
        if len(self._short_term) % 10 == 0:
            await self.persist()
            
    async def recall(self, query: str, limit: int = 10) -> Optional[List[Any]]:
        """
        Recuperar información de memoria
        """
        # Buscar en memoria de corto plazo primero
        short_term_results = [
            entry for entry in self._short_term 
            if entry["type"] == query
        ]
        
        if short_term_results:
            return short_term_results[-limit:]
            
        # Buscar en memoria de largo plazo
        if query in self._long_term:
            return self._long_term[query][-limit:]
            
        # Búsqueda especial para contexto reciente
        if query == "recent_context":
            recent = list(self._short_term)[-limit:]
            return recent if recent else None
            
        return None
        
    async def forget(self, memory_type: str, older_than_days: int = 30) -> int:
        """
        Olvidar memorias antiguas (limpieza de memoria)
        """
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=older_than_days)
        forgotten_count = 0
        
        if memory_type in self._long_term:
            original_count = len(self._long_term[memory_type])
            self._long_term[memory_type] = [
                entry for entry in self._long_term[memory_type]
                if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
            ]
            forgotten_count = original_count - len(self._long_term[memory_type])
            
        await self.persist()
        return forgotten_count
        
    async def persist(self) -> None:
        """Guardar memoria en disco"""
        await asyncio.get_event_loop().run_in_executor(None, self._save)
        
    async def get_statistics(self) -> Dict:
        """Obtener estadísticas de memoria"""
        return {
            "short_term_count": len(self._short_term),
            "long_term_types": list(self._long_term.keys()),
            "total_memories": sum(len(v) for v in self._long_term.values()),
            "memory_file": str(self.memory_file),
            "file_exists": self.memory_file.exists()
        }
        
    async def clear(self) -> None:
        """Limpiar toda la memoria (usar con precaución)"""
        self._short_term.clear()
        self._long_term.clear()
        self._index_by_type.clear()
        await self.persist()
