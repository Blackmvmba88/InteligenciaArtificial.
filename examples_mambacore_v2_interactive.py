#!/usr/bin/env python3
"""
MambaCore v2: Modo Interactivo
Permite control en tiempo real del sistema multimodal
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


async def interactive_loop(vision_module, audio_module, command_interface):
    """Loop interactivo para comandos del usuario"""
    print("\n" + "="*60)
    print("🧬 MambaCore v2 - Modo Interactivo")
    print("="*60)
    print("\nComandos disponibles:")
    print("  vision <prompt>    → Generar imagen")
    print("  audio <texto>      → Generar música/audio")
    print("  speech <texto>     → Síntesis de voz")
    print("  status             → Ver estado del sistema")
    print("  history            → Ver historial de comandos")
    print("  help               → Mostrar ayuda")
    print("  exit/salir         → Salir")
    print("="*60 + "\n")
    
    while True:
        try:
            command = await asyncio.get_event_loop().run_in_executor(
                None,
                input,
                "mamba> "
            )
            
            command = command.strip()
            
            if not command:
                continue
                
            if command.lower() in ["exit", "salir", "quit"]:
                print("[MambaCore] Terminando modo interactivo...")
                break
                
            # Parsear comando
            parts = command.split(maxsplit=1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if cmd == "vision":
                if args:
                    print(f"[MambaCore] 🎨 Generando imagen: {args}")
                    await vision_module.generate(args)
                else:
                    print("[MambaCore] ⚠️  Uso: vision <descripción>")
                    
            elif cmd == "audio":
                if args:
                    print(f"[MambaCore] 🎵 Generando audio: {args}")
                    await audio_module.generate_music(args)
                else:
                    print("[MambaCore] ⚠️  Uso: audio <descripción>")
                    
            elif cmd == "speech":
                if args:
                    print(f"[MambaCore] 🗣️  Sintetizando voz: {args}")
                    await audio_module.generate_speech(args)
                else:
                    print("[MambaCore] ⚠️  Uso: speech <texto>")
                    
            elif cmd == "status":
                await command_interface.act({"action": "status"})
                
            elif cmd == "history":
                history = command_interface.get_command_history()
                print(f"\n[MambaCore] 📜 Últimos {len(history)} comandos:")
                for i, entry in enumerate(history, 1):
                    print(f"  {i}. {entry['action'].get('action', 'unknown')} - {entry['timestamp']}")
                    
            elif cmd == "help":
                print("\n[MambaCore] 📚 Comandos disponibles:")
                print("  vision <prompt>    → Generar imagen con IA")
                print("  audio <texto>      → Generar música/audio")
                print("  speech <texto>     → Convertir texto a voz")
                print("  status             → Estado del sistema")
                print("  history            → Historial de comandos")
                print("  help               → Esta ayuda")
                print("  exit/salir         → Salir del modo interactivo")
                
            else:
                # Intentar como comando natural
                await command_interface.execute_command(command)
                
            # Pequeña pausa para procesamiento
            await asyncio.sleep(0.5)
            
        except EOFError:
            print("\n[MambaCore] EOF detectado, terminando...")
            break
        except Exception as e:
            print(f"[MambaCore] ❌ Error: {e}")


async def main():
    """Ejecutar MambaCore v2 en modo interactivo"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🧬 MambaCore v2 - Modo Interactivo 🧬               ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # 1. Inicializar componentes
    event_bus = EventBus()
    memory = MemoryModule("mambacore_v2_interactive.json")
    reasoning = ReasoningEngine()
    
    # 2. Configurar reglas
    reasoning.add_rule(
        name="vision_ack",
        condition=lambda ctx: any(
            p.get("data", {}).get("type") == "vision"
            for p in ctx.get("perceptions", [])
        ),
        action=lambda ctx: {
            "action": "emitir_mensaje",
            "content": "✓ Imagen lista",
            "confidence": 0.95
        },
        priority=10
    )
    
    reasoning.add_rule(
        name="audio_ack",
        condition=lambda ctx: any(
            p.get("data", {}).get("type") == "audio"
            for p in ctx.get("perceptions", [])
        ),
        action=lambda ctx: {
            "action": "emitir_mensaje",
            "content": "✓ Audio completado",
            "confidence": 0.95
        },
        priority=10
    )
    
    # 3. Crear componentes
    cognitive_core = CognitiveCore(event_bus, memory, reasoning)
    vision_module = VisionModule("vision_interactive", event_bus, backend="mock")
    audio_module = AudioModule("audio_interactive", event_bus, backend="mock")
    command_interface = CommandInterface("mamba_cli_interactive", event_bus, verbose=False)
    synapse_bridge = SynapseBridge(event_bus)
    
    print("✓ Sistema multimodal inicializado")
    print("✓ Núcleo cognitivo activo")
    print("✓ Módulos de visión y audio listos")
    print("✓ CLI Mamba preparado\n")
    
    # 4. Tareas del sistema
    tasks = [
        asyncio.create_task(event_bus.start()),
        asyncio.create_task(cognitive_core.run(cycle_interval=1.5)),
        asyncio.create_task(vision_module.start(interval=0.3)),
        asyncio.create_task(audio_module.start(interval=0.3))
    ]
    
    # Esperar inicialización
    await asyncio.sleep(0.5)
    
    try:
        # 5. Loop interactivo
        await interactive_loop(vision_module, audio_module, command_interface)
        
    finally:
        # Limpieza
        print("\n[MambaCore] Deteniendo sistema...")
        cognitive_core.stop()
        vision_module.stop()
        audio_module.stop()
        event_bus.stop()
        
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)
        await memory.persist()
        
        # Mostrar estadísticas finales
        print("\n📊 Estadísticas de sesión:")
        memory_stats = await memory.get_statistics()
        synapse_stats = synapse_bridge.get_statistics()
        
        print(f"  Memorias almacenadas: {memory_stats['total_memories']}")
        print(f"  Percepciones visuales: {synapse_stats['context_sizes']['vision']}")
        print(f"  Percepciones auditivas: {synapse_stats['context_sizes']['audio']}")
        print(f"  Acciones ejecutadas: {command_interface.get_statistics()['actions_performed']}")
        
        print("\n✓ MambaCore v2 detenido correctamente")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🧠 MambaCore v2 interrumpido")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
