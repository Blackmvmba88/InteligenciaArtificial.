#!/usr/bin/env python3
"""
Test suite for MambaCore v2 multimodal components
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.core.event_bus import EventBus
from src.multimodal.vision_module import VisionModule
from src.multimodal.audio_module import AudioModule
from src.multimodal.command_interface import CommandInterface
from src.multimodal.synapse_bridge import SynapseBridge


async def test_vision_module():
    """Test VisionModule functionality"""
    print("\n[Test 1] VisionModule...")
    try:
        event_bus = EventBus()
        vision = VisionModule("test_vision", event_bus, backend="mock")
        
        # Test generation
        await vision.generate("test prompt")
        result = await vision.read()
        
        assert result is not None, "Vision read returned None"
        assert result["type"] == "vision", "Wrong type"
        assert "prompt" in result, "Missing prompt"
        assert result["backend"] == "mock", "Wrong backend"
        
        print("✓ VisionModule working")
        return True
    except Exception as e:
        print(f"❌ VisionModule failed: {e}")
        return False


async def test_audio_module():
    """Test AudioModule functionality"""
    print("\n[Test 2] AudioModule...")
    try:
        event_bus = EventBus()
        audio = AudioModule("test_audio", event_bus, backend="mock")
        
        # Test music generation
        await audio.generate_music("test music")
        result = await audio.read()
        
        assert result is not None, "Audio read returned None"
        assert result["type"] == "audio", "Wrong type"
        assert result["request_type"] == "music", "Wrong request type"
        assert result["backend"] == "mock", "Wrong backend"
        
        # Test speech generation
        await audio.generate_speech("test speech")
        result = await audio.read()
        
        assert result is not None, "Speech read returned None"
        assert result["request_type"] == "tts", "Wrong speech type"
        
        print("✓ AudioModule working")
        return True
    except Exception as e:
        print(f"❌ AudioModule failed: {e}")
        return False


async def test_command_interface():
    """Test CommandInterface functionality"""
    print("\n[Test 3] CommandInterface...")
    try:
        event_bus = EventBus()
        cli = CommandInterface("test_cli", event_bus, verbose=False)
        
        # Test action execution
        await cli.act({"action": "emitir_mensaje", "content": "test"})
        
        stats = cli.get_statistics()
        assert stats["actions_performed"] == 1, "Action count wrong"
        
        # Test command history
        history = cli.get_command_history()
        assert len(history) == 1, "History length wrong"
        
        print("✓ CommandInterface working")
        return True
    except Exception as e:
        print(f"❌ CommandInterface failed: {e}")
        return False


async def test_synapse_bridge():
    """Test SynapseBridge functionality"""
    print("\n[Test 4] SynapseBridge...")
    try:
        event_bus = EventBus()
        bridge = SynapseBridge(event_bus, context_window=10)
        
        # Start event bus in background
        bus_task = asyncio.create_task(event_bus.start())
        await asyncio.sleep(0.1)
        
        # Test vision sync
        await event_bus.emit("vision_data", {
            "type": "vision",
            "prompt": "test"
        })
        await asyncio.sleep(0.2)
        
        # Test audio sync
        await event_bus.emit("audio_data", {
            "type": "audio",
            "text": "test"
        })
        await asyncio.sleep(0.2)
        
        # Check statistics
        stats = bridge.get_statistics()
        assert stats["context_sizes"]["vision"] > 0, "Vision context empty"
        assert stats["context_sizes"]["audio"] > 0, "Audio context empty"
        assert stats["sync_events"] > 0, "No sync events"
        
        # Cleanup
        event_bus.stop()
        bus_task.cancel()
        await asyncio.gather(bus_task, return_exceptions=True)
        
        print("✓ SynapseBridge working")
        return True
    except Exception as e:
        print(f"❌ SynapseBridge failed: {e}")
        return False


async def test_integration():
    """Test integrated multimodal system"""
    print("\n[Test 5] Multimodal Integration...")
    try:
        event_bus = EventBus()
        
        vision = VisionModule("integration_vision", event_bus)
        audio = AudioModule("integration_audio", event_bus)
        cli = CommandInterface("integration_cli", event_bus, verbose=False)
        bridge = SynapseBridge(event_bus)
        
        # Start components
        bus_task = asyncio.create_task(event_bus.start())
        vision_task = asyncio.create_task(vision.start(interval=0.2))
        audio_task = asyncio.create_task(audio.start(interval=0.2))
        
        await asyncio.sleep(0.1)
        
        # Generate multimodal content
        await vision.generate("integration test image")
        await audio.generate_music("integration test music")
        
        await asyncio.sleep(1)
        
        # Check integration
        stats = bridge.get_statistics()
        assert stats["sync_events"] >= 2, "Not enough sync events"
        
        # Cleanup
        vision.stop()
        audio.stop()
        event_bus.stop()
        
        for task in [bus_task, vision_task, audio_task]:
            task.cancel()
        
        await asyncio.gather(bus_task, vision_task, audio_task, return_exceptions=True)
        
        print("✓ Multimodal Integration working")
        return True
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_tests():
    """Run all MambaCore v2 tests"""
    print("=" * 60)
    print("Testing MambaCore v2 Multimodal Components")
    print("=" * 60)
    
    results = []
    
    results.append(await test_vision_module())
    results.append(await test_audio_module())
    results.append(await test_command_interface())
    results.append(await test_synapse_bridge())
    results.append(await test_integration())
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ All MambaCore v2 tests passed!")
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
