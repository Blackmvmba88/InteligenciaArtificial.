"""
Reasoning Engine - Motor de razonamiento simbólico adaptable
"""
import asyncio
from typing import Any, Dict, List, Optional
from datetime import datetime


class Rule:
    """Regla de razonamiento simbólico"""
    
    def __init__(self, name: str, condition: callable, action: callable, priority: int = 0):
        self.name = name
        self.condition = condition
        self.action = action
        self.priority = priority
        self.execution_count = 0
        self.last_executed = None
        
    def evaluate(self, context: Dict) -> bool:
        """Evaluar si la condición se cumple"""
        try:
            return self.condition(context)
        except Exception as e:
            print(f"Error evaluating rule {self.name}: {e}")
            return False
            
    def execute(self, context: Dict) -> Any:
        """Ejecutar la acción de la regla"""
        try:
            result = self.action(context)
            self.execution_count += 1
            self.last_executed = datetime.now()
            return result
        except Exception as e:
            print(f"Error executing rule {self.name}: {e}")
            return None


class ReasoningEngine:
    """
    Motor de razonamiento simbólico adaptable.
    Utiliza reglas para tomar decisiones basadas en el contexto.
    """
    
    def __init__(self):
        self._rules: List[Rule] = []
        self._reasoning_history: List[Dict] = []
        self._adaptive_weights: Dict[str, float] = {}
        
    def add_rule(self, name: str, condition: callable, action: callable, priority: int = 0) -> None:
        """Añadir una nueva regla de razonamiento"""
        rule = Rule(name, condition, action, priority)
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
        self._adaptive_weights[name] = 1.0
        
    def remove_rule(self, name: str) -> bool:
        """Eliminar una regla por nombre"""
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                self._rules.pop(i)
                if name in self._adaptive_weights:
                    del self._adaptive_weights[name]
                return True
        return False
        
    async def reason(self, perceptions: List[Any], context: Dict) -> Dict:
        """
        Razonar sobre percepciones y contexto para tomar una decisión
        """
        # Preparar contexto completo para razonamiento
        reasoning_context = {
            "perceptions": perceptions,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "perception_count": len(perceptions)
        }
        
        # Evaluar todas las reglas
        applicable_rules = []
        for rule in self._rules:
            if rule.evaluate(reasoning_context):
                applicable_rules.append(rule)
                
        # Si no hay reglas aplicables, usar razonamiento por defecto
        if not applicable_rules:
            return self._default_reasoning(reasoning_context)
            
        # Seleccionar mejor regla (considerando prioridad y pesos adaptativos)
        best_rule = max(
            applicable_rules,
            key=lambda r: r.priority * self._adaptive_weights.get(r.name, 1.0)
        )
        
        # Ejecutar regla seleccionada
        decision = best_rule.execute(reasoning_context)
        
        # Registrar razonamiento
        reasoning_record = {
            "rule_used": best_rule.name,
            "applicable_rules": [r.name for r in applicable_rules],
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        }
        self._reasoning_history.append(reasoning_record)
        
        # Mantener historial limitado
        if len(self._reasoning_history) > 1000:
            self._reasoning_history = self._reasoning_history[-500:]
            
        return decision
        
    def _default_reasoning(self, context: Dict) -> Dict:
        """Razonamiento por defecto cuando no hay reglas aplicables"""
        perceptions = context.get("perceptions", [])
        
        # Análisis simple de percepciones
        if len(perceptions) > 10:
            return {
                "action": "process",
                "confidence": 0.6,
                "reason": "many_perceptions"
            }
        elif len(perceptions) > 0:
            return {
                "action": "observe",
                "confidence": 0.5,
                "reason": "few_perceptions"
            }
        else:
            return {
                "action": "wait",
                "confidence": 0.4,
                "reason": "no_perceptions"
            }
            
    async def adapt(self, rule_name: str, performance_score: float) -> None:
        """
        Adaptar pesos de reglas basado en desempeño
        performance_score: 0.0 (malo) a 1.0 (excelente)
        """
        if rule_name in self._adaptive_weights:
            current_weight = self._adaptive_weights[rule_name]
            # Ajustar peso gradualmente
            adjustment = (performance_score - 0.5) * 0.1
            new_weight = max(0.1, min(2.0, current_weight + adjustment))
            self._adaptive_weights[rule_name] = new_weight
            
    async def get_statistics(self) -> Dict:
        """Obtener estadísticas del motor de razonamiento"""
        rule_stats = [
            {
                "name": rule.name,
                "priority": rule.priority,
                "executions": rule.execution_count,
                "weight": self._adaptive_weights.get(rule.name, 1.0),
                "last_executed": rule.last_executed.isoformat() if rule.last_executed else None
            }
            for rule in self._rules
        ]
        
        return {
            "total_rules": len(self._rules),
            "reasoning_history_size": len(self._reasoning_history),
            "rules": rule_stats
        }
        
    def get_history(self, limit: int = 10) -> List[Dict]:
        """Obtener historial reciente de razonamiento"""
        return self._reasoning_history[-limit:]
