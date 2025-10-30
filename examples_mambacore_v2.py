#!/usr/bin/env python3
"""
MambaCore v2: Sinapsis Multimodal
Integra visión, audio y lenguaje sobre el núcleo cognitivo base
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
from src.multimodal.vision_module import VisionModule
from src.multimodal.audio_module import AudioModule
from src.multimodal.command_interface import CommandInterface
from src.multimodal.synapse_bridge import SynapseBridge


async def main():
    """Ejecutar MambaCore v2 con capacidades multimodales"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🧬 MambaCore v2 - Sinapsis Multimodal 🧬            ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # 1. Componentes base del framework
    event_bus = EventBus()
    memory = MemoryModule("mambacore_v2_memory.json")
    reasoning = ReasoningEngine()
    
    # 2. Configurar reglas de razonamiento multimodal
    reasoning.add_rule(
        name="vision_response",
        condition=lambda ctx: any(
            p.get("data", {}).get("type") == "vision"
            for p in ctx.get("perceptions", [])
        ),
        action=lambda ctx: {
            "action": "emitir_mensaje",
            "content": "✓ Imagen procesada correctamente",
            "confidence": 0.9
        },
        priority=10
    )
    
    reasoning.add_rule(
        name="audio_response",
        condition=lambda ctx: any(
            p.get("data", {}).get("type") == "audio"
            for p in ctx.get("perceptions", [])
        ),
        action=lambda ctx: {
            "action": "emitir_mensaje",
            "content": "✓ Audio generado con éxito",
            "confidence": 0.9
        },
        priority=10
    )
    
    reasoning.add_rule(
        name="multimodal_analysis",
        condition=lambda ctx: ctx.get("perception_count", 0) > 5,
        action=lambda ctx: {
            "action": "emitir_mensaje",
            "content": "📊 Análisis multimodal: Múltiples percepciones integradas",
            "confidence": 0.8
        },
        priority=5
    )
    
    # 3. Crear núcleo cognitivo
    cognitive_core = CognitiveCore(
        event_bus=event_bus,
        memory_module=memory,
        reasoning_engine=reasoning
    )
    
    # 4. Crear módulos multimodales
    vision_module = VisionModule("vision_core", event_bus, backend="mock")
    audio_module = AudioModule("audio_core", event_bus, backend="mock")
    command_interface = CommandInterface("mamba_cli", event_bus, verbose=True)
    synapse_bridge = SynapseBridge(event_bus, context_window=50)
    
    print("✓ EventBus inicializado")
    print("✓ Memoria persistente configurada")
    print("✓ Motor de razonamiento con reglas multimodales")
    print("✓ Núcleo cognitivo activado")
    print("✓ VisionModule cargado (backend: mock)")
    print("✓ AudioModule cargado (backend: mock)")
    print("✓ CommandInterface (MambaCLI) activado")
    print("✓ SynapseBridge sincronizado\n")
    
    print("═══════════════════════════════════════════════════════════")
    print("🎨 Generando ejemplos de percepción multimodal...")
    print("═══════════════════════════════════════════════════════════\n")
    
    # Tareas asíncronas
    tasks = [
        asyncio.create_task(event_bus.start()),
        asyncio.create_task(cognitive_core.run(cycle_interval=2.0)),
        asyncio.create_task(vision_module.start(interval=0.5)),
        asyncio.create_task(audio_module.start(interval=0.5))
    ]
    
    # Generar ejemplos de percepciones multimodales
    await asyncio.sleep(1)  # Esperar inicialización
    
    # Ejemplo 1: Generación de imagen
    print("[Demo] Solicitando generación de imagen...")
    await vision_module.generate("Paisaje neón azteca con pirámides y cielos cósmicos")
    await asyncio.sleep(2)
    
    # Ejemplo 2: Generación de música
    print("\n[Demo] Solicitando generación de música...")
    await audio_module.generate_music("Mezcla de reggae y trap con vibras cósmicas", style="experimental")
    await asyncio.sleep(2)
    
    # Ejemplo 3: Síntesis de voz
    print("\n[Demo] Solicitando síntesis de voz...")
    await audio_module.generate_speech("Hola, soy MambaCore v2, tu sistema cognitivo multimodal")
    await asyncio.sleep(2)
    
    # Ejemplo 4: Nueva imagen
    print("\n[Demo] Solicitando otra imagen...")
    await vision_module.generate("Robot orgánico en ciudad futurista bioluminiscente")
    await asyncio.sleep(2)
    
    print("\n═══════════════════════════════════════════════════════════")
    print("📊 Estadísticas del Sistema")
    print("═══════════════════════════════════════════════════════════\n")
    
    # Mostrar estadísticas
    memory_stats = await memory.get_statistics()
    reasoning_stats = await reasoning.get_statistics()
    synapse_stats = synapse_bridge.get_statistics()
    
    print(f"Memoria:")
    print(f"  - Memorias de corto plazo: {memory_stats['short_term_count']}")
    print(f"  - Total de memorias: {memory_stats['total_memories']}")
    
    print(f"\nRazonamiento:")
    print(f"  - Reglas activas: {reasoning_stats['total_rules']}")
    print(f"  - Decisiones tomadas: {reasoning_stats['reasoning_history_size']}")
    
    print(f"\nSynapseBridge:")
    print(f"  - Visión: {synapse_stats['context_sizes']['vision']} entradas")
    print(f"  - Audio: {synapse_stats['context_sizes']['audio']} entradas")
    print(f"  - Texto: {synapse_stats['context_sizes']['text']} entradas")
    print(f"  - Eventos de sincronización: {synapse_stats['sync_events']}")
    
    print(f"\nCommandInterface:")
    print(f"  - Acciones ejecutadas: {command_interface.get_statistics()['actions_performed']}")
    
    print("\n═══════════════════════════════════════════════════════════")
    print("✓ Demo completada - Deteniendo sistema...")
    print("═══════════════════════════════════════════════════════════\n")
    
    # Limpieza
    cognitive_core.stop()
    vision_module.stop()
    audio_module.stop()
    event_bus.stop()
    
    for task in tasks:
        task.cancel()
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await memory.persist()
    
    print("✓ MambaCore v2 detenido correctamente")
    print("\nPara modo interactivo, ejecuta:")
    print("  python3 examples_mambacore_v2_interactive.py")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🧠 MambaCore v2 interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
