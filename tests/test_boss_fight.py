import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.template_engine import BatchExporter

def test_100_quests_in_5_seconds():
    start = time.time()
    BatchExporter.generate_100_quests()
    elapsed = time.time() - start
    assert elapsed < 5, f"Слишком медленно: {elapsed:.2f} сек"
    print(f"✅ Босс повержен за {elapsed:.2f} секунд! +20 XP")
