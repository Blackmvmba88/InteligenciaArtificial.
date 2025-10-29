"""
CommandInterface - CLI Mamba para control natural del sistema
Terminal inteligente que interpreta comandos en lenguaje natural
"""
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from ..core.event_bus import EventBus, Event
from ..examples.actuator import Actuator


class CommandInterface(Actuator):
    """
    CLI Mamba - Interfaz de comandos universal.
    Interpreta lenguaje natural y ejecuta acciones en el sistema.
    """
    
    def __init__(self, name: str, event_bus: EventBus, verbose: bool = True):
        super().__init__(name, event_bus)
        self.verbose = verbose
        self._command_history = []
        
        # Suscribirse a eventos adicionales
        self.event_bus.subscribe("vision_data", self._on_vision_event)
        self.event_bus.subscribe("audio_data", self._on_audio_event)
        self.event_bus.subscribe("cognitive_core_started", self._on_system_event)
        self.event_bus.subscribe("cognitive_core_stopped", self._on_system_event)
        
    async def _on_vision_event(self, event: Event) -> None:
        """Handler para eventos de visión"""
        data = event.data
        if self.verbose:
            print(f"\n[MambaCLI] 🎨 Visión generada:")
            print(f"  Prompt: {data.get('prompt', 'N/A')}")
            print(f"  Backend: {data.get('backend', 'N/A')}")
            if 'note' in data:
                print(f"  Nota: {data['note']}")
                
    async def _on_audio_event(self, event: Event) -> None:
        """Handler para eventos de audio"""
        data = event.data
        if self.verbose:
            print(f"\n[MambaCLI] 🎵 Audio generado:")
            print(f"  Tipo: {data.get('request_type', 'N/A')}")
            print(f"  Texto: {data.get('text', 'N/A')}")
            print(f"  Backend: {data.get('backend', 'N/A')}")
            if 'note' in data:
                print(f"  Nota: {data['note']}")
                
    async def _on_system_event(self, event: Event) -> None:
        """Handler para eventos del sistema"""
        if event.type == "cognitive_core_started":
            print("\n[MambaCLI] 🧠 Núcleo cognitivo iniciado")
        elif event.type == "cognitive_core_stopped":
            print("\n[MambaCLI] 🧠 Núcleo cognitivo detenido")
            
    async def act(self, action: Dict[str, Any]) -> None:
        """Ejecutar acción en la interfaz"""
        self._action_count += 1
        
        action_type = action.get("action", "unknown")
        
        # Comandos específicos de MambaCLI
        if action_type == "emitir_mensaje":
            content = action.get("content", "")
            print(f"\n[MambaCLI] → {content}")
            
        elif action_type == "vision":
            prompt = action.get("prompt", "")
            print(f"\n[MambaCLI] 🎨 Generando imagen: {prompt}")
            
        elif action_type == "audio":
            description = action.get("description", "")
            print(f"\n[MambaCLI] 🎵 Generando audio: {description}")
            
        elif action_type == "status":
            print(f"\n[MambaCLI] 📊 Estado del sistema:")
            print(f"  Acciones ejecutadas: {self._action_count}")
            print(f"  Comandos en historial: {len(self._command_history)}")
            
        elif self.verbose:
            print(f"\n[MambaCLI] ⚡ Acción ejecutada:")
            print(f"  Tipo: {action_type}")
            if "confidence" in action:
                print(f"  Confianza: {action['confidence']}")
            if "reason" in action:
                print(f"  Razón: {action['reason']}")
                
        # Registrar en historial
        self._command_history.append({
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantener historial limitado
        if len(self._command_history) > 1000:
            self._command_history = self._command_history[-500:]
            
    async def execute_command(self, command: str) -> None:
        """
        Ejecutar comando en lenguaje natural.
        Parsea el comando y emite eventos apropiados.
        """
        command_lower = command.lower().strip()
        
        # Comandos de visión
        if any(keyword in command_lower for keyword in ["genera", "crea", "dibuja", "imagen"]):
            prompt = command.replace("genera", "").replace("crea", "").replace("dibuja", "").strip()
            await self.event_bus.emit("command_vision", {"prompt": prompt}, source=self.name)
            print(f"[MambaCLI] 🎨 Comando de visión: {prompt}")
            
        # Comandos de audio
        elif any(keyword in command_lower for keyword in ["música", "musica", "canción", "audio", "sonido"]):
            description = command
            await self.event_bus.emit("command_audio", {"description": description}, source=self.name)
            print(f"[MambaCLI] 🎵 Comando de audio: {description}")
            
        # Comando de estado
        elif "estado" in command_lower or "status" in command_lower:
            await self.act({"action": "status"})
            
        # Comando desconocido
        else:
            await self.event_bus.emit("command_text", {"text": command}, source=self.name)
            print(f"[MambaCLI] 💬 Comando procesado: {command}")
            
    def get_command_history(self, limit: int = 10) -> list:
        """Obtener historial de comandos"""
        return self._command_history[-limit:]
        
    async def start_interactive_mode(self) -> None:
        """
        Modo interactivo de CLI Mamba.
        Permite al usuario ingresar comandos en tiempo real.
        """
        print("\n" + "="*60)
        print("🧬 MambaCLI - Terminal Inteligente")
        print("="*60)
        print("Comandos disponibles:")
        print("  - Genera/crea/dibuja [descripción] → Generar imagen")
        print("  - Música/audio/sonido [descripción] → Generar audio")
        print("  - Estado/status → Ver estado del sistema")
        print("  - Salir/exit → Terminar")
        print("="*60 + "\n")
        
        while True:
            try:
                command = await asyncio.get_event_loop().run_in_executor(
                    None,
                    input,
                    "mamba> "
                )
                
                if command.lower() in ["salir", "exit", "quit"]:
                    print("[MambaCLI] Terminando...")
                    break
                    
                if command.strip():
                    await self.execute_command(command)
                    
            except Exception as e:
                print(f"[MambaCLI] Error: {e}")
                break
