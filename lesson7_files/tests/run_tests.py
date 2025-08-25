#!/usr/bin/env python3
"""
Test runner for dashboard components
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def run_all_tests():
    """Run all test suites and report results"""
    
    print("=" * 60)
    print("DASHBOARD COMPONENT TESTING")
    print("=" * 60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    
    # Load test suites
    test_suites = []
    test_modules = [
        'test_data_loader',
        'test_business_metrics', 
        'test_dashboard'
    ]
    
    for module_name in test_modules:
        try:
            suite = loader.loadTestsFromName(module_name)
            test_suites.append((module_name, suite))
            print(f"✅ Loaded tests from {module_name}")
        except Exception as e:
            print(f"❌ Failed to load tests from {module_name}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("RUNNING TESTS")
    print("=" * 60)
    
    # Run each test suite separately to get detailed results
    all_results = []
    
    for module_name, suite in test_suites:
        print(f"\n🧪 Testing {module_name}...")
        print("-" * 40)
        
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        all_results.append((module_name, result))
        
        # Print summary for this module
        if result.wasSuccessful():
            print(f"✅ {module_name}: ALL TESTS PASSED")
        else:
            print(f"❌ {module_name}: {len(result.failures)} failures, {len(result.errors)} errors")
    
    # Print overall summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for module_name, result in all_results:
        total_tests += result.testsRun
        total_failures += len(result.failures)
        total_errors += len(result.errors)
        
        status = "PASS" if result.wasSuccessful() else "FAIL"
        print(f"{module_name:<25} {result.testsRun:>3} tests  {status}")
    
    print("-" * 60)
    print(f"TOTAL: {total_tests} tests, {total_failures} failures, {total_errors} errors")
    
    if total_failures == 0 and total_errors == 0:
        print("🎉 ALL TESTS PASSED!")
        return True
    else:
        print("⚠️  SOME TESTS FAILED - See details above")
        return False


def run_specific_test(test_module, test_class=None, test_method=None):
    """Run specific test for debugging"""
    
    if test_class and test_method:
        test_name = f"{test_module}.{test_class}.{test_method}"
    elif test_class:
        test_name = f"{test_module}.{test_class}"
    else:
        test_name = test_module
    
    print(f"Running specific test: {test_name}")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_name)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_args = sys.argv[1].split('.')
        if len(test_args) == 3:
            success = run_specific_test(test_args[0], test_args[1], test_args[2])
        elif len(test_args) == 2:
            success = run_specific_test(test_args[0], test_args[1])
        else:
            success = run_specific_test(test_args[0])
    else:
        # Run all tests
        success = run_all_tests()
    
    sys.exit(0 if success else 1)