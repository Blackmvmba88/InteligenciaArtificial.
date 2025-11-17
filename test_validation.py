#!/usr/bin/env python3
"""
Test suite for input validation and optimization features
Tests that all validation checks work correctly
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.event_bus import EventBus, Event
from src.core.cognitive_core import CognitiveCore
from src.modules.memory_module import MemoryModule
from src.modules.reasoning_engine import ReasoningEngine
from src.multimodal.vision_module import VisionModule
from src.multimodal.audio_module import AudioModule
from src.multimodal.command_interface import CommandInterface
from src.multimodal.synapse_bridge import SynapseBridge


async def test_eventbus_validation():
    """Test EventBus input validation"""
    print("\n[Test 1] EventBus Validation...")
    
    try:
        # Test invalid max_queue_size
        try:
            EventBus(max_queue_size=0)
            assert False, "Should raise ValueError for max_queue_size=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        # Test valid initialization
        event_bus = EventBus(max_queue_size=100)
        
        # Test subscribe with invalid event_type
        try:
            event_bus.subscribe("", lambda e: None)
            assert False, "Should raise ValueError for empty event_type"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test subscribe with invalid callback
        try:
            event_bus.subscribe("test", "not_callable")
            assert False, "Should raise ValueError for non-callable"
        except ValueError as e:
            assert "callable" in str(e)
        
        # Test emit with invalid event_type
        try:
            await event_bus.emit("", {"data": "test"})
            assert False, "Should raise ValueError for empty event_type"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test publish with invalid event
        try:
            await event_bus.publish("not_an_event")
            assert False, "Should raise ValueError for non-Event"
        except ValueError as e:
            assert "Event" in str(e)
        
        print("✓ EventBus validation working")
        return True
    except Exception as e:
        print(f"❌ EventBus validation failed: {e}")
        return False


async def test_memory_validation():
    """Test MemoryModule input validation"""
    print("\n[Test 2] MemoryModule Validation...")
    
    try:
        # Test invalid max_short_term
        try:
            MemoryModule(max_short_term=0)
            assert False, "Should raise ValueError for max_short_term=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        # Test invalid memory_file
        try:
            MemoryModule(memory_file="")
            assert False, "Should raise ValueError for empty memory_file"
        except ValueError as e:
            assert "vacío" in str(e)
        
        # Test valid initialization
        memory = MemoryModule(memory_file="test_validation_memory.json", max_short_term=50)
        
        # Test store with invalid memory_type
        try:
            await memory.store("", {"data": "test"})
            assert False, "Should raise ValueError for empty memory_type"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test recall with invalid limit
        try:
            await memory.recall("test", limit=0)
            assert False, "Should raise ValueError for limit=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        await memory.clear()
        print("✓ MemoryModule validation working")
        return True
    except Exception as e:
        print(f"❌ MemoryModule validation failed: {e}")
        return False


async def test_reasoning_validation():
    """Test ReasoningEngine input validation"""
    print("\n[Test 3] ReasoningEngine Validation...")
    
    try:
        # Test invalid max_rules
        try:
            ReasoningEngine(max_rules=0)
            assert False, "Should raise ValueError for max_rules=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        # Test valid initialization
        reasoning = ReasoningEngine(max_rules=5)
        
        # Test add_rule with invalid name
        try:
            reasoning.add_rule("", lambda ctx: True, lambda ctx: {}, priority=1)
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test add_rule with invalid condition
        try:
            reasoning.add_rule("test", "not_callable", lambda ctx: {}, priority=1)
            assert False, "Should raise ValueError for non-callable condition"
        except ValueError as e:
            assert "callable" in str(e)
        
        # Test add_rule with invalid action
        try:
            reasoning.add_rule("test", lambda ctx: True, "not_callable", priority=1)
            assert False, "Should raise ValueError for non-callable action"
        except ValueError as e:
            assert "callable" in str(e)
        
        # Add valid rules
        reasoning.add_rule("rule1", lambda ctx: True, lambda ctx: {"action": "test1"}, priority=1)
        
        # Test duplicate rule name
        try:
            reasoning.add_rule("rule1", lambda ctx: True, lambda ctx: {"action": "test2"}, priority=1)
            assert False, "Should raise ValueError for duplicate rule name"
        except ValueError as e:
            assert "existe" in str(e)
        
        # Test max_rules limit
        for i in range(2, 6):
            reasoning.add_rule(f"rule{i}", lambda ctx: True, lambda ctx: {"action": f"test{i}"}, priority=i)
        
        try:
            reasoning.add_rule("rule6", lambda ctx: True, lambda ctx: {"action": "test6"}, priority=6)
            assert False, "Should raise RuntimeError for exceeding max_rules"
        except RuntimeError as e:
            assert "máximo" in str(e)
        
        print("✓ ReasoningEngine validation working")
        return True
    except Exception as e:
        print(f"❌ ReasoningEngine validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cognitive_validation():
    """Test CognitiveCore input validation"""
    print("\n[Test 4] CognitiveCore Validation...")
    
    try:
        # Test invalid event_bus
        try:
            CognitiveCore(None)
            assert False, "Should raise ValueError for None event_bus"
        except ValueError as e:
            assert "None" in str(e)
        
        # Test valid initialization
        event_bus = EventBus()
        core = CognitiveCore(event_bus)
        
        # Test perceive with invalid source
        try:
            await core.perceive({"data": "test"}, source="")
            assert False, "Should raise ValueError for empty source"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test run with invalid cycle_interval
        try:
            # Create a task that will run but we'll cancel it immediately
            run_task = asyncio.create_task(core.run(cycle_interval=0))
            await asyncio.sleep(0.1)
            core.stop()
            await run_task
            assert False, "Should raise ValueError for cycle_interval=0"
        except ValueError as e:
            assert "positivo" in str(e)
        except asyncio.CancelledError:
            pass
        
        print("✓ CognitiveCore validation working")
        return True
    except Exception as e:
        print(f"❌ CognitiveCore validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_vision_validation():
    """Test VisionModule input validation"""
    print("\n[Test 5] VisionModule Validation...")
    
    try:
        event_bus = EventBus()
        
        # Test invalid name
        try:
            VisionModule("", event_bus)
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test invalid event_bus
        try:
            VisionModule("test", None)
            assert False, "Should raise ValueError for None event_bus"
        except ValueError as e:
            assert "None" in str(e)
        
        # Test invalid backend
        try:
            VisionModule("test", event_bus, backend="invalid")
            assert False, "Should raise ValueError for invalid backend"
        except ValueError as e:
            assert "no soportado" in str(e)
        
        # Test valid initialization
        vision = VisionModule("test_vision", event_bus, backend="mock")
        
        # Test generate with invalid prompt
        try:
            await vision.generate("")
            assert False, "Should raise ValueError for empty prompt"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test analyze_image with invalid path
        try:
            await vision.analyze_image("")
            assert False, "Should raise ValueError for empty image_path"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        print("✓ VisionModule validation working")
        return True
    except Exception as e:
        print(f"❌ VisionModule validation failed: {e}")
        return False


async def test_audio_validation():
    """Test AudioModule input validation"""
    print("\n[Test 6] AudioModule Validation...")
    
    try:
        event_bus = EventBus()
        
        # Test invalid name
        try:
            AudioModule("", event_bus)
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test invalid event_bus
        try:
            AudioModule("test", None)
            assert False, "Should raise ValueError for None event_bus"
        except ValueError as e:
            assert "None" in str(e)
        
        # Test invalid backend
        try:
            AudioModule("test", event_bus, backend="invalid")
            assert False, "Should raise ValueError for invalid backend"
        except ValueError as e:
            assert "no soportado" in str(e)
        
        # Test valid initialization
        audio = AudioModule("test_audio", event_bus, backend="mock")
        
        # Test generate_music with invalid description
        try:
            await audio.generate_music("")
            assert False, "Should raise ValueError for empty description"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test generate_speech with invalid text
        try:
            await audio.generate_speech("")
            assert False, "Should raise ValueError for empty text"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test generate_sound with invalid description
        try:
            await audio.generate_sound("")
            assert False, "Should raise ValueError for empty description"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        print("✓ AudioModule validation working")
        return True
    except Exception as e:
        print(f"❌ AudioModule validation failed: {e}")
        return False


async def test_synapse_validation():
    """Test SynapseBridge input validation"""
    print("\n[Test 7] SynapseBridge Validation...")
    
    try:
        # Test invalid event_bus
        try:
            SynapseBridge(None)
            assert False, "Should raise ValueError for None event_bus"
        except ValueError as e:
            assert "None" in str(e)
        
        # Test invalid context_window
        try:
            SynapseBridge(EventBus(), context_window=0)
            assert False, "Should raise ValueError for context_window=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        # Test valid initialization
        bridge = SynapseBridge(EventBus(), context_window=10)
        
        # Test get_context_by_modality with invalid limit
        try:
            bridge.get_context_by_modality("vision", limit=0)
            assert False, "Should raise ValueError for limit=0"
        except ValueError as e:
            assert "positivo" in str(e)
        
        print("✓ SynapseBridge validation working")
        return True
    except Exception as e:
        print(f"❌ SynapseBridge validation failed: {e}")
        return False


async def test_command_validation():
    """Test CommandInterface input validation"""
    print("\n[Test 8] CommandInterface Validation...")
    
    try:
        event_bus = EventBus()
        
        # Test invalid name
        try:
            CommandInterface("", event_bus)
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        # Test invalid event_bus
        try:
            CommandInterface("test", None)
            assert False, "Should raise ValueError for None event_bus"
        except ValueError as e:
            assert "None" in str(e)
        
        # Test valid initialization
        cli = CommandInterface("test_cli", event_bus, verbose=False)
        
        # Test execute_command with invalid command
        try:
            await cli.execute_command("")
            assert False, "Should raise ValueError for empty command"
        except ValueError as e:
            assert "no vacía" in str(e)
        
        print("✓ CommandInterface validation working")
        return True
    except Exception as e:
        print(f"❌ CommandInterface validation failed: {e}")
        return False


async def run_tests():
    """Run all validation tests"""
    print("=" * 60)
    print("Testing Input Validation and Optimization Features")
    print("=" * 60)
    
    results = []
    
    results.append(await test_eventbus_validation())
    results.append(await test_memory_validation())
    results.append(await test_reasoning_validation())
    results.append(await test_cognitive_validation())
    results.append(await test_vision_validation())
    results.append(await test_audio_validation())
    results.append(await test_synapse_validation())
    results.append(await test_command_validation())
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ All validation tests passed!")
        print("=" * 60)
        return True
    else:
        failed = sum(1 for r in results if not r)
        print(f"❌ {failed}/{len(results)} tests failed")
        print("=" * 60)
        return False


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
