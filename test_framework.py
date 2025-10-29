#!/usr/bin/env python3
"""
Test script to verify framework functionality
Compatible with Python 3.10+
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.event_bus import EventBus
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine
from src.examples.sensor import RandomSensor
from src.examples.actuator import ConsoleActuator


async def run_tests():
    """Run framework tests"""
    print("=" * 60)
    print("Testing InteligenciaArtificial Framework")
    print("=" * 60)
    
    # Check Python version
    version = sys.version_info
    print(f"\nPython version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        return False
    
    print("✓ Python version compatible")
    
    # Test 1: EventBus
    print("\n[Test 1] EventBus...")
    try:
        event_bus = EventBus()
        test_results = []
        
        def handler(event):
            test_results.append(event.data)
        
        event_bus.subscribe("test_event", handler)
        
        # Start EventBus in background
        bus_task = asyncio.create_task(event_bus.start())
        await asyncio.sleep(0.1)  # Let it start
        
        await event_bus.emit("test_event", "test_data")
        await asyncio.sleep(0.2)  # Wait for processing
        
        event_bus.stop()
        bus_task.cancel()
        await asyncio.gather(bus_task, return_exceptions=True)
        
        assert len(test_results) == 1, f"EventBus handler not called (results: {test_results})"
        print("✓ EventBus working")
    except Exception as e:
        print(f"❌ EventBus failed: {e}")
        return False
    
    # Test 2: MemoryModule
    print("\n[Test 2] MemoryModule...")
    try:
        memory = MemoryModule(memory_file="test_framework_memory.json")
        await memory.store("test_type", {"value": 42})
        result = await memory.recall("test_type")
        
        assert result is not None, "Memory recall returned None"
        assert len(result) > 0, "Memory recall empty"
        assert result[0]["data"]["value"] == 42, "Memory data mismatch"
        
        stats = await memory.get_statistics()
        assert stats["short_term_count"] > 0, "Short term memory empty"
        
        await memory.clear()
        print("✓ MemoryModule working")
    except Exception as e:
        print(f"❌ MemoryModule failed: {e}")
        return False
    
    # Test 3: ReasoningEngine
    print("\n[Test 3] ReasoningEngine...")
    try:
        reasoning = ReasoningEngine()
        
        # Add test rule (context is nested in reasoning_context)
        reasoning.add_rule(
            name="test_rule",
            condition=lambda ctx: ctx.get("context", {}).get("test_flag", False),
            action=lambda ctx: {"action": "test_action", "confidence": 0.9},
            priority=10
        )
        
        # Test with condition met
        decision = await reasoning.reason([], {"test_flag": True})
        assert decision["action"] == "test_action", f"Wrong action: {decision['action']}"
        assert decision["confidence"] == 0.9, "Wrong confidence"
        
        # Test with condition not met (should use default)
        decision = await reasoning.reason([], {"test_flag": False})
        assert "action" in decision, "No action in decision"
        
        stats = await reasoning.get_statistics()
        assert stats["total_rules"] == 1, "Wrong rule count"
        
        print("✓ ReasoningEngine working")
    except Exception as e:
        print(f"❌ ReasoningEngine failed: {e}")
        return False
    
    # Test 4: CognitiveCore
    print("\n[Test 4] CognitiveCore...")
    try:
        event_bus = EventBus()
        memory = MemoryModule(memory_file="test_cognitive_memory.json")
        reasoning = ReasoningEngine()
        
        reasoning.add_rule(
            name="simple_rule",
            condition=lambda ctx: True,
            action=lambda ctx: {"action": "observe", "confidence": 0.5},
            priority=1
        )
        
        core = CognitiveCore(event_bus, memory, reasoning)
        
        # Test perception
        await core.perceive({"sensor": "test", "value": 100})
        
        # Test thinking
        thoughts = await core.think()
        assert thoughts is not None, "Thinking returned None"
        assert "decision" in thoughts, "No decision in thoughts"
        
        # Test action
        await core.act({"action": "test_action"})
        
        await memory.clear()
        print("✓ CognitiveCore working")
    except Exception as e:
        print(f"❌ CognitiveCore failed: {e}")
        return False
    
    # Test 5: Sensors
    print("\n[Test 5] Sensors...")
    try:
        event_bus = EventBus()
        sensor = RandomSensor("test_sensor", event_bus, 0, 100)
        
        value = await sensor.read()
        assert 0 <= value <= 100, f"Sensor value out of range: {value}"
        
        print("✓ Sensors working")
    except Exception as e:
        print(f"❌ Sensors failed: {e}")
        return False
    
    # Test 6: Actuators
    print("\n[Test 6] Actuators...")
    try:
        event_bus = EventBus()
        actuator = ConsoleActuator("test_actuator", event_bus, verbose=False)
        
        await actuator.act({"action": "test", "confidence": 0.8})
        
        stats = actuator.get_statistics()
        assert stats["actions_performed"] == 1, "Wrong action count"
        
        print("✓ Actuators working")
    except Exception as e:
        print(f"❌ Actuators failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)
    print("\nFramework is ready to use!")
    print("Try running: python3 examples_basic.py")
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(run_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
