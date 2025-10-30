#!/usr/bin/env python3
"""
Ejemplo interactivo del framework de IA
Permite interacción en tiempo real con el sistema cognitivo
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
from src.examples.sensor import InputSensor
from src.examples.actuator import ConsoleActuator, StateActuator


async def interactive_mode(cognitive_core, input_sensor):
    """Modo interactivo para proporcionar comandos"""
    print("\n=== Modo Interactivo ===")
    print("Comandos disponibles:")
    print("  - escribir algo: envía datos al sistema")
    print("  - 'salir' o 'exit': terminar\n")
    
    while True:
        try:
            # Leer entrada de forma no bloqueante
            user_input = await asyncio.get_event_loop().run_in_executor(
                None,
                input,
                "> "
            )
            
            if user_input.lower() in ['salir', 'exit', 'quit']:
                break
                
            # Enviar entrada al sensor
            await input_sensor.provide_input(user_input)
            
        except Exception as e:
            print(f"Error: {e}")
            break


async def main():
    """Ejecutar ejemplo interactivo"""
    print("=== Framework de IA - Modo Interactivo ===\n")
    
    # 1. Crear componentes principales
    event_bus = EventBus()
    memory = MemoryModule(memory_file="interactive_memory.json")
    reasoning = ReasoningEngine()
    
    # 2. Configurar reglas de razonamiento para entrada de usuario
    reasoning.add_rule(
        name="respond_to_input",
        condition=lambda ctx: any(
            p.get("data", {}).get("sensor") == "user_input" 
            for p in ctx.get("perceptions", [])
        ),
        action=lambda ctx: {
            "action": "respond",
            "confidence": 0.9,
            "reason": "user_interaction_detected"
        },
        priority=20
    )
    
    reasoning.add_rule(
        name="default_observe",
        condition=lambda ctx: True,
        action=lambda ctx: {
            "action": "observe",
            "confidence": 0.5,
            "reason": "waiting_for_input"
        },
        priority=1
    )
    
    # 3. Crear núcleo cognitivo
    cognitive_core = CognitiveCore(
        event_bus=event_bus,
        memory_module=memory,
        reasoning_engine=reasoning
    )
    
    # 4. Crear sensores y actuadores
    input_sensor = InputSensor("user_input", event_bus)
    console_actuator = ConsoleActuator("console", event_bus, verbose=True)
    state_actuator = StateActuator("state", event_bus)
    
    print("✓ Sistema interactivo inicializado")
    print("✓ Esperando entrada del usuario...\n")
    
    # Crear tareas
    tasks = [
        asyncio.create_task(event_bus.start()),
        asyncio.create_task(cognitive_core.run(cycle_interval=1.0)),
        asyncio.create_task(input_sensor.start(interval=0.5))
    ]
    
    try:
        # Ejecutar modo interactivo
        await interactive_mode(cognitive_core, input_sensor)
        
    except KeyboardInterrupt:
        print("\n\nDeteniendo sistema...")
    finally:
        # Limpieza
        cognitive_core.stop()
        input_sensor.stop()
        event_bus.stop()
        
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)
        await memory.persist()
        
        print("\n✓ Sistema detenido correctamente")


if __name__ == "__main__":
    asyncio.run(main())
