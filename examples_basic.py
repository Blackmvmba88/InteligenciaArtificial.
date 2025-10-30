#!/usr/bin/env python3
"""
Ejemplo básico del framework de IA
Demuestra el ciclo cognitivo perceive → think → act
"""
import asyncio
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.event_bus import EventBus
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine
from src.examples.sensor import RandomSensor, TimeSensor
from src.examples.actuator import ConsoleActuator, LogActuator


async def main():
    """Ejecutar ejemplo básico"""
    print("=== Framework de IA - Ejemplo Básico ===\n")
    
    # 1. Crear bus de eventos
    event_bus = EventBus()
    
    # 2. Crear módulo de memoria
    memory = MemoryModule(memory_file="example_memory.json")
    
    # 3. Crear motor de razonamiento con reglas simples
    reasoning = ReasoningEngine()
    
    # Añadir regla: si hay muchas percepciones, procesarlas
    reasoning.add_rule(
        name="process_many_perceptions",
        condition=lambda ctx: ctx.get("perception_count", 0) > 3,
        action=lambda ctx: {
            "action": "process",
            "confidence": 0.8,
            "reason": "many_perceptions_accumulated"
        },
        priority=10
    )
    
    # Añadir regla: si hay pocas percepciones, seguir observando
    reasoning.add_rule(
        name="continue_observing",
        condition=lambda ctx: ctx.get("perception_count", 0) <= 3,
        action=lambda ctx: {
            "action": "observe",
            "confidence": 0.6,
            "reason": "gathering_more_data"
        },
        priority=5
    )
    
    # 4. Crear núcleo cognitivo
    cognitive_core = CognitiveCore(
        event_bus=event_bus,
        memory_module=memory,
        reasoning_engine=reasoning
    )
    
    # 5. Crear sensores
    random_sensor = RandomSensor("temperature_sensor", event_bus, min_val=15, max_val=30)
    time_sensor = TimeSensor("time_sensor", event_bus)
    
    # 6. Crear actuadores
    console_actuator = ConsoleActuator("console", event_bus, verbose=True)
    log_actuator = LogActuator("logger", event_bus, log_file="example_actions.log")
    
    print("✓ Sistema inicializado")
    print("✓ Núcleo cognitivo creado")
    print("✓ Sensores y actuadores configurados")
    print("\nIniciando ciclo cognitivo (Ctrl+C para detener)...\n")
    
    # Crear tareas asíncronas
    tasks = [
        asyncio.create_task(event_bus.start()),
        asyncio.create_task(cognitive_core.run(cycle_interval=2.0)),
        asyncio.create_task(random_sensor.start(interval=1.5)),
        asyncio.create_task(time_sensor.start(interval=3.0))
    ]
    
    try:
        # Ejecutar por un tiempo limitado para demostración
        await asyncio.sleep(15)
        
    except KeyboardInterrupt:
        print("\n\nDeteniendo sistema...")
    finally:
        # Detener componentes
        cognitive_core.stop()
        random_sensor.stop()
        time_sensor.stop()
        event_bus.stop()
        
        # Cancelar tareas
        for task in tasks:
            task.cancel()
        
        # Esperar a que las tareas terminen
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Guardar memoria
        await memory.persist()
        
        # Mostrar estadísticas
        print("\n=== Estadísticas Finales ===")
        memory_stats = await memory.get_statistics()
        print(f"\nMemoria:")
        print(f"  - Memorias de corto plazo: {memory_stats['short_term_count']}")
        print(f"  - Total de memorias: {memory_stats['total_memories']}")
        print(f"  - Tipos: {', '.join(memory_stats['long_term_types'])}")
        
        reasoning_stats = await reasoning.get_statistics()
        print(f"\nRazonamiento:")
        print(f"  - Total de reglas: {reasoning_stats['total_rules']}")
        print(f"  - Decisiones tomadas: {reasoning_stats['reasoning_history_size']}")
        
        print(f"\nActuadores:")
        print(f"  - Console: {console_actuator.get_statistics()['actions_performed']} acciones")
        print(f"  - Logger: {log_actuator.get_statistics()['actions_performed']} acciones")
        
        print("\n✓ Sistema detenido correctamente")


if __name__ == "__main__":
    asyncio.run(main())
