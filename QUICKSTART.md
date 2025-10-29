# Guía de Inicio Rápido - InteligenciaArtificial

## Instalación en 30 segundos

```bash
# Clonar el repositorio
git clone https://github.com/Blackmvmba88/InteligenciaArtificial.git
cd InteligenciaArtificial.

# Ejecutar pruebas
python3 test_framework.py

# Ejecutar ejemplo básico
python3 examples_basic.py
```

## Primeros Pasos

### 1. Ejecutar el Ejemplo Básico

```bash
python3 examples_basic.py
```

Verás:
- Sistema cognitivo inicializándose
- Sensores capturando datos (temperatura, tiempo)
- Núcleo cognitivo tomando decisiones
- Actuadores ejecutando acciones
- Estadísticas al finalizar

### 2. Modo Interactivo

```bash
python3 examples_interactive.py
```

Escribe comandos y observa cómo el sistema responde en tiempo real.

### 3. Tu Primer Agente de IA

Crea `mi_agente.py`:

```python
import asyncio
from src.core.event_bus import EventBus
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine
from src.examples.sensor import RandomSensor
from src.examples.actuator import ConsoleActuator

async def main():
    # Configurar componentes
    bus = EventBus()
    memoria = MemoryModule("mi_memoria.json")
    razonamiento = ReasoningEngine()
    
    # Añadir tu lógica
    razonamiento.add_rule(
        name="mi_regla",
        condition=lambda ctx: ctx.get("perception_count", 0) > 2,
        action=lambda ctx: {
            "action": "procesar",
            "confidence": 0.9
        },
        priority=10
    )
    
    # Crear núcleo cognitivo
    nucleo = CognitiveCore(bus, memoria, razonamiento)
    
    # Añadir sensor y actuador
    sensor = RandomSensor("mi_sensor", bus)
    actuador = ConsoleActuator("mi_actuador", bus)
    
    # Ejecutar
    await asyncio.gather(
        bus.start(),
        nucleo.run(cycle_interval=1.0),
        sensor.start(interval=0.5)
    )

if __name__ == "__main__":
    asyncio.run(main())
```

## Arquitectura en 3 Líneas

1. **Sensores** → capturan información
2. **Núcleo Cognitivo** → percibe, piensa, decide
3. **Actuadores** → ejecutan acciones

## Componentes Principales

| Componente | Descripción | Archivo |
|------------|-------------|---------|
| EventBus | Sistema de eventos | `src/core/event_bus.py` |
| CognitiveCore | Ciclo perceive→think→act | `src/core/cognitive_core.py` |
| MemoryModule | Memoria persistente JSON | `src/modules/memory_module.py` |
| ReasoningEngine | Razonamiento simbólico | `src/modules/reasoning_engine.py` |
| Sensors | Entrada de datos | `src/examples/sensor.py` |
| Actuators | Salida de acciones | `src/examples/actuator.py` |

## Casos de Uso

### 🏠 Automatización del Hogar
```python
# Sensor de temperatura → Razonamiento → Actuador de clima
temp_sensor = RandomSensor("temperatura", bus, 18, 28)
climate_actuator = StateActuator("clima", bus)
```

### 🤖 Bot Conversacional
```python
# Sensor de entrada → Razonamiento con reglas → Actuador de respuesta
input_sensor = InputSensor("usuario", bus)
response_actuator = ConsoleActuator("respuesta", bus)
```

### 📊 Monitoreo de Sistema
```python
# Múltiples sensores → Memoria de métricas → Alertas
cpu_sensor = RandomSensor("cpu", bus, 0, 100)
memory_sensor = RandomSensor("ram", bus, 0, 16)
alert_actuator = LogActuator("alertas", bus)
```

## Plataformas Compatibles

✅ **macOS** - Totalmente compatible  
✅ **Linux** - Totalmente compatible  
✅ **Raspberry Pi** - Optimizado para ARM  
✅ **Termux (Android)** - Compatible móvil  
✅ **Windows** - Python 3.10+

## Recursos

- **README.md** - Documentación completa
- **examples_basic.py** - Ejemplo básico funcional
- **examples_interactive.py** - Ejemplo interactivo
- **test_framework.py** - Suite de pruebas

## Siguiente Paso

Lee el [README.md](README.md) completo para documentación detallada.

## Soporte

¿Problemas? Abre un issue en GitHub.

---

**¡Framework listo para crear IA evolutiva! 🚀**
