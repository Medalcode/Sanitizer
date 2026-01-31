
import sys
import os

# Add root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests import test_validation, test_slugify

def run_tests():
    modules = [test_validation, test_slugify]
    total = 0
    passed = 0
    failed = 0
    
    print("Running Minimal Test Suite...")
    
    for module in modules:
        for name in dir(module):
            if name.startswith("test_"):
                func = getattr(module, name)
                total += 1
                try:
                    func()
                    print(f"PASS: {name}")
                    passed += 1
                except AssertionError as e:
                    print(f"FAIL: {name}")
                    failed += 1
                except Exception as e:
                    print(f"ERROR: {name} -> {e}")
                    failed += 1
                    
    print(f"\nResumen: {passed}/{total} pasados. {failed} fallidos.")
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
