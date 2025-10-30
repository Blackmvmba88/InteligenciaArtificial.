# MambaCore v2 - Sinapsis Multimodal

## Visión General

MambaCore v2 extiende el framework base de InteligenciaArtificial con capacidades multimodales, permitiendo que el sistema cognitivo:

- 🎨 **Vea y cree**: Genere y analice imágenes
- 🎵 **Escuche y componga**: Genere música y sintetice voz
- 💬 **Comprenda y hable**: Procese lenguaje natural
- 🔗 **Integre todo**: Sincronice percepciones multimodales

## Arquitectura Multimodal

```
┌─────────────────────────────────────────────────────────┐
│                    MambaCLI (Usuario)                    │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
    ┌────▼─────┐          ┌────▼─────┐
    │ Vision   │          │  Audio   │
    │ Module   │          │  Module  │
    └────┬─────┘          └────┬─────┘
         │                     │
         └──────┬──────────────┘
                │
         ┌──────▼──────┐
         │  Synapse    │
         │   Bridge    │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  EventBus   │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  Cognitive  │
         │    Core     │
         └─────────────┘
```

## Componentes

### 1. VisionModule

Interfaz para generación y análisis de imágenes.

**Backends soportados:**
- `mock` - Simulación sin dependencias (por defecto)
- `stable_diffusion` - Stable Diffusion WebUI API
- `comfyui` - ComfyUI API

**Ejemplo de uso:**

```python
from src.multimodal.vision_module import VisionModule

vision = VisionModule("vision", event_bus, backend="mock")

# Generar imagen
await vision.generate("Paisaje cyberpunk con neón y lluvia")

# Analizar imagen
result = await vision.analyze_image("path/to/image.jpg")
```

**Integración con Stable Diffusion:**

```python
# TODO: Configurar SD WebUI con --api flag
# vision = VisionModule("vision", event_bus, backend="stable_diffusion")
# Requiere: requests, pillow (opcional)
```

### 2. AudioModule

Interfaz para generación de audio, música y síntesis de voz.

**Backends soportados:**
- `mock` - Simulación sin dependencias (por defecto)
- `suno` - Suno AI API
- `tts_local` - TTS local (pyttsx3, espeak)
- `music_gen` - MusicGen / AudioCraft

**Ejemplo de uso:**

```python
from src.multimodal.audio_module import AudioModule

audio = AudioModule("audio", event_bus, backend="mock")

# Generar música
await audio.generate_music("Jazz suave con piano", style="ambient")

# Síntesis de voz
await audio.generate_speech("Hola mundo", voice="default")

# Efecto de sonido
await audio.generate_sound("Lluvia cayendo")
```

**Integración con Suno:**

```python
# TODO: Configurar API key de Suno
# audio = AudioModule("audio", event_bus, backend="suno")
# Requiere: suno-client (pip install suno-client)
```

### 3. CommandInterface (MambaCLI)

Terminal inteligente que interpreta comandos en lenguaje natural.

**Comandos:**
- `vision <descripción>` - Generar imagen
- `audio <descripción>` - Generar música
- `speech <texto>` - Síntesis de voz
- `status` - Estado del sistema
- `history` - Historial de comandos
- `help` - Ayuda
- `exit` - Salir

**Ejemplo de uso:**

```python
from src.multimodal.command_interface import CommandInterface

cli = CommandInterface("mamba", event_bus, verbose=True)

# Ejecutar comando
await cli.execute_command("genera una imagen de robot futurista")

# Modo interactivo
await cli.start_interactive_mode()
```

### 4. SynapseBridge

Puente sináptico que sincroniza contexto entre modalidades.

**Características:**
- Mantiene contexto compartido entre visión, audio y texto
- Prepara embeddings unificados (estilo CLIP)
- Búsqueda cross-modal
- Historial de sincronizaciones

**Ejemplo de uso:**

```python
from src.multimodal.synapse_bridge import SynapseBridge

bridge = SynapseBridge(event_bus, context_window=50)

# Obtener contexto unificado
unified = bridge.get_unified_context(limit=10)

# Contexto por modalidad
vision_context = bridge.get_context_by_modality("vision", limit=5)
audio_context = bridge.get_context_by_modality("audio", limit=5)

# Búsqueda cross-modal
results = await bridge.cross_modal_search("paisaje", modality="all")

# Estadísticas
stats = bridge.get_statistics()
```

## Inicio Rápido

### 1. Demo Automático

```bash
python3 examples_mambacore_v2.py
```

Ejecuta ejemplos automáticos de:
- Generación de imágenes
- Generación de música
- Síntesis de voz
- Análisis multimodal

### 2. Modo Interactivo

```bash
python3 examples_mambacore_v2_interactive.py
```

Interactúa en tiempo real:
```
mamba> vision crea un dragón de cristal volando
[MambaCore] 🎨 Generando imagen: crea un dragón de cristal volando

mamba> audio música electrónica atmosférica
[MambaCore] 🎵 Generando audio: música electrónica atmosférica

mamba> status
[MambaCLI] 📊 Estado del sistema:
  Acciones ejecutadas: 2
  Comandos en historial: 2
```

### 3. Crear tu Propio Sistema Multimodal

```python
import asyncio
from src.core.event_bus import EventBus
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine
from src.multimodal import VisionModule, AudioModule, CommandInterface, SynapseBridge

async def main():
    # Inicializar componentes
    bus = EventBus()
    memory = MemoryModule("my_mamba.json")
    reasoning = ReasoningEngine()
    
    # Crear núcleo cognitivo
    core = CognitiveCore(bus, memory, reasoning)
    
    # Añadir capacidades multimodales
    vision = VisionModule("vision", bus, backend="mock")
    audio = AudioModule("audio", bus, backend="mock")
    cli = CommandInterface("cli", bus)
    bridge = SynapseBridge(bus)
    
    # Ejecutar
    await asyncio.gather(
        bus.start(),
        core.run(cycle_interval=1.0),
        vision.start(interval=0.5),
        audio.start(interval=0.5)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Extensiones Futuras

### Cognitive Mesh (Red Cognitiva Distribuida)

```python
# TODO: Implementar comunicación distribuida
# Raspberry Pi → sensores físicos
# Mac → núcleo cognitivo y render
# Android (Termux) → CLI Mamba remoto
# Comunicación: WebSockets + ZeroMQ + SQLite replicado
```

### QuantumBridge (Motor de Resonancia Creativa)

```python
# TODO: Implementar motor cuántico de creatividad
# - Patrones no deterministas
# - Interferencia de decisiones
# - "Estado emocional" del sistema
# - Rutas creativas evolutivas
```

### Memoria Vectorial Semántica

```python
# TODO: Implementar almacenamiento vectorial
# - Integración con FAISS o Qdrant
# - Embeddings con CLIP/CLAP/GPT
# - Búsqueda semántica cross-modal
# - "Sueños": combinaciones creativas de percepciones
```

### Panel Web Visual

```python
# TODO: Implementar visualización web
# - FastAPI + React + WebSocket
# - Flujo cognitivo en tiempo real
# - Visualización de percepciones y decisiones
# - Control remoto del sistema
```

## Integración con Herramientas Externas

### Stable Diffusion

1. Instalar Stable Diffusion WebUI con API
2. Configurar backend:
   ```python
   vision = VisionModule("vision", bus, backend="stable_diffusion")
   ```
3. Opcional: Instalar dependencias
   ```bash
   pip install requests pillow
   ```

### Suno (Música)

1. Obtener API key de Suno
2. Instalar cliente:
   ```bash
   pip install suno-client
   ```
3. Configurar backend:
   ```python
   audio = AudioModule("audio", bus, backend="suno")
   ```

### ComfyUI

1. Instalar ComfyUI con API habilitada
2. Configurar backend:
   ```python
   vision = VisionModule("vision", bus, backend="comfyui")
   ```

### TTS Local

1. Instalar pyttsx3:
   ```bash
   pip install pyttsx3
   ```
2. Configurar backend:
   ```python
   audio = AudioModule("audio", bus, backend="tts_local")
   ```

## Testing

Ejecutar tests multimodales:

```bash
python3 test_mambacore_v2.py
```

Tests incluidos:
1. VisionModule - Generación de imágenes
2. AudioModule - Generación de audio
3. CommandInterface - CLI Mamba
4. SynapseBridge - Sincronización multimodal
5. Integración - Sistema completo

## Filosofía de Diseño

1. **Ligero por defecto**: Funciona sin dependencias externas (backends mock)
2. **Extensible**: Fácil integración con herramientas reales
3. **Modular**: Cada componente independiente
4. **Evolutivo**: Preparado para crecimiento futuro
5. **Portable**: Compatible con múltiples plataformas

## Contribuir

Para añadir nuevos backends:

1. Crear método `_<backend>_generate` en el módulo
2. Añadir backend al enum de opciones
3. Documentar dependencias necesarias
4. Crear test para el backend

Ejemplo:
```python
async def _my_backend_generate(self, prompt: str) -> Dict[str, Any]:
    # Tu implementación
    return {
        "type": "vision",
        "prompt": prompt,
        "image": result,
        "backend": "my_backend"
    }
```

## Recursos

- [README.md](README.md) - Documentación principal
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida
- [examples_mambacore_v2.py](examples_mambacore_v2.py) - Demo completo
- [test_mambacore_v2.py](test_mambacore_v2.py) - Suite de tests

---

**MambaCore v2 - Donde visión, audio y lenguaje se encuentran en una sola conciencia cognitiva. 🧬**
