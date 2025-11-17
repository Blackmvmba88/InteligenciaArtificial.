# InteligenciaArtificial

Framework modular de IA ligera y evolutiva con arquitectura asincrónica basada en eventos.

## Descripción

Framework vivo de IA ligera, hecho para aprender, percibir y crear. Código limpio, adaptable y con conciencia de su propio entorno. Implementa un núcleo cognitivo completo con memoria persistente, razonamiento simbólico adaptable y arquitectura extensible mediante sensores y actuadores.

**🧬 MambaCore v2** añade capacidades multimodales: visión, audio y lenguaje integrados en una sola conciencia cognitiva.

## Características

### Core Framework
- 🧠 **Núcleo Cognitivo**: Ciclo completo perceive → think → act
- 💾 **Memoria Persistente**: Sistema de memoria con JSON para corto y largo plazo
- 🎯 **Razonamiento Adaptable**: Motor de razonamiento simbólico con reglas priorizadas
- ⚡ **Arquitectura Asíncrona**: Sistema basado en eventos con asyncio
- 🔌 **Modular y Extensible**: Fácil integración de sensores y actuadores personalizados
- 🌐 **Portable**: Compatible con Python 3.10+, Mac, Linux, Termux y Raspberry Pi
- ✅ **Optimizado y Validado**: Validación de entrada completa y límites de recursos configurables

### MambaCore v2 (Multimodal)
- 🎨 **VisionModule**: Interfaz para generación de imágenes (Stable Diffusion, ComfyUI)
- 🎵 **AudioModule**: Generación de música y síntesis de voz (Suno, TTS local)
- 💬 **CommandInterface**: CLI Mamba para comandos en lenguaje natural
- 🔗 **SynapseBridge**: Puente de comunicación multimodal (texto↔imagen↔audio)
- 🌐 **Cognitive Mesh**: Arquitectura preparada para cognición distribuida
- ⚛️ **QuantumBridge**: Motor de resonancia creativa (en desarrollo)

## Arquitectura

### Componentes Principales

**Framework Base:**
1. **EventBus**: Sistema de eventos asíncrono para comunicación desacoplada entre módulos
2. **CognitiveCore**: Núcleo cognitivo que implementa el ciclo perceive → think → act
3. **MemoryModule**: Sistema de memoria con persistencia JSON
4. **ReasoningEngine**: Motor de razonamiento simbólico con reglas adaptables
5. **Sensors**: Abstracciones de entrada (sensores)
6. **Actuators**: Abstracciones de salida (actuadores)

**MambaCore v2 (Multimodal):**
7. **VisionModule**: Generación y análisis de imágenes
8. **AudioModule**: Generación de audio y música
9. **CommandInterface**: CLI inteligente (MambaCLI)
10. **SynapseBridge**: Sincronización multimodal

### Flujo de Datos

```
Sensores → EventBus → CognitiveCore → ReasoningEngine → EventBus → Actuadores
                ↓                ↓
            MemoryModule    MemoryModule
```

## Instalación

### Requisitos

- Python 3.10 o superior
- No requiere dependencias externas (solo biblioteca estándar)

### Configuración

```bash
# Clonar el repositorio
git clone https://github.com/Blackmvmba88/InteligenciaArtificial.git
cd InteligenciaArtificial

# (Opcional) Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar (si hay dependencias adicionales)
pip install -r requirements.txt
```

## Uso

### Ejemplo Básico

Ejecutar el ejemplo básico que demuestra el ciclo cognitivo completo:

```bash
python3 examples_basic.py
```

Este ejemplo:
- Crea un núcleo cognitivo con memoria y razonamiento
- Configura sensores (temperatura y tiempo)
- Configura actuadores (consola y log)
- Ejecuta el ciclo cognitivo durante 15 segundos
- Muestra estadísticas al finalizar

### Ejemplo Interactivo

Ejecutar el modo interactivo para interactuar con el sistema:

```bash
python3 examples_interactive.py
```

Este ejemplo permite:
- Enviar comandos al sistema en tiempo real
- Ver cómo el núcleo cognitivo procesa la entrada
- Observar decisiones y acciones del sistema

### MambaCore v2 - Multimodal

Ejecutar el sistema multimodal con visión, audio y lenguaje:

```bash
# Demo automático con ejemplos
python3 examples_mambacore_v2.py

# Modo interactivo
python3 examples_mambacore_v2_interactive.py
```

Comandos MambaCLI:
- `vision <descripción>` - Generar imagen
- `audio <descripción>` - Generar música
- `speech <texto>` - Síntesis de voz
- `status` - Estado del sistema
- `exit` - Salir

### Crear tu Propio Sistema

```python
import asyncio
from src.core.event_bus import EventBus
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine

async def main():
    # 1. Crear bus de eventos
    event_bus = EventBus()
    
    # 2. Crear memoria
    memory = MemoryModule(memory_file="my_memory.json")
    
    # 3. Crear motor de razonamiento
    reasoning = ReasoningEngine()
    
    # Añadir tus propias reglas
    reasoning.add_rule(
        name="my_rule",
        condition=lambda ctx: ctx.get("perception_count", 0) > 5,
        action=lambda ctx: {"action": "my_action", "confidence": 0.8},
        priority=10
    )
    
    # 4. Crear núcleo cognitivo
    cognitive_core = CognitiveCore(
        event_bus=event_bus,
        memory_module=memory,
        reasoning_engine=reasoning
    )
    
    # 5. Crear tus sensores y actuadores
    # ... (ver ejemplos)
    
    # 6. Iniciar sistema
    await asyncio.gather(
        event_bus.start(),
        cognitive_core.run(cycle_interval=1.0)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Estructura del Proyecto

```
InteligenciaArtificial./
├── src/
│   ├── core/
│   │   ├── event_bus.py              # Sistema de eventos
│   │   └── cognitive_core.py         # Núcleo cognitivo
│   ├── modules/
│   │   ├── memory_module.py          # Módulo de memoria
│   │   └── reasoning_engine.py       # Motor de razonamiento
│   ├── multimodal/                   # 🧬 MambaCore v2
│   │   ├── vision_module.py          # Generación de imágenes
│   │   ├── audio_module.py           # Generación de audio
│   │   ├── command_interface.py      # CLI Mamba
│   │   └── synapse_bridge.py         # Puente multimodal
│   └── examples/
│       ├── sensor.py                 # Ejemplos de sensores
│       └── actuator.py               # Ejemplos de actuadores
├── examples_basic.py                 # Ejemplo básico
├── examples_interactive.py           # Ejemplo interactivo
├── examples_mambacore_v2.py          # 🧬 Demo MambaCore v2
├── examples_mambacore_v2_interactive.py  # 🧬 Modo interactivo v2
├── test_framework.py                 # Tests del framework base
├── test_mambacore_v2.py              # 🧬 Tests multimodales
├── requirements.txt                  # Dependencias
├── QUICKSTART.md                     # Guía rápida
└── README.md                         # Este archivo
```

## Extender el Framework

### Crear un Sensor Personalizado

```python
from src.examples.sensor import Sensor

class MySensor(Sensor):
    async def read(self):
        # Tu lógica de lectura
        return {"my_data": "value"}
```

### Crear un Actuador Personalizado

```python
from src.examples.actuator import Actuator

class MyActuator(Actuator):
    async def act(self, action):
        # Tu lógica de actuación
        print(f"Executing: {action}")
```

### Añadir Reglas de Razonamiento

```python
reasoning.add_rule(
    name="my_custom_rule",
    condition=lambda ctx: ctx["perception_count"] > 10,
    action=lambda ctx: {
        "action": "custom_action",
        "confidence": 0.9,
        "params": {"key": "value"}
    },
    priority=15
)
```

## Compatibilidad

### Plataformas Soportadas

- ✅ **macOS**: Totalmente compatible
- ✅ **Linux**: Totalmente compatible
- ✅ **Raspberry Pi**: Optimizado para hardware limitado
- ✅ **Termux (Android)**: Compatible con entornos móviles
- ✅ **Windows**: Compatible con Python 3.10+

### Requisitos de Sistema

- **CPU**: Cualquier procesador compatible con Python
- **RAM**: Mínimo 256 MB (recomendado 512 MB+)
- **Almacenamiento**: ~10 MB para el framework + espacio para memoria JSON

## Desarrollo

### Principios de Diseño

1. **Código Limpio**: Siguiendo PEP 8 y mejores prácticas de Python
2. **Modularidad**: Componentes desacoplados y reutilizables
3. **Ligereza**: Sin dependencias pesadas, solo biblioteca estándar
4. **Evolutivo**: Diseñado para crecer y adaptarse
5. **Asíncrono**: Arquitectura no bloqueante con asyncio
6. **Seguro**: Validación completa de entradas y manejo robusto de errores

### Optimizaciones y Validación

El framework incluye optimizaciones de rendimiento y validación de entrada:

- **Límites de Recursos**: Todos los módulos tienen límites configurables para prevenir crecimiento ilimitado
- **Validación de Entrada**: Validación completa de parámetros con mensajes de error claros
- **Gestión de Memoria**: Limpieza automática y límites por tipo de dato
- **Tests Completos**: 19 tests cubriendo funcionalidad, validación y seguridad

Ver [OPTIMIZATIONS.md](OPTIMIZATIONS.md) para detalles completos sobre optimizaciones implementadas.

### Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo una licencia de código abierto. Ver el archivo LICENSE para más detalles.

## Autor

**Blackmvmba88**

## Agradecimientos

Framework creado con el objetivo de democratizar la IA y hacerla accesible en cualquier plataforma.
