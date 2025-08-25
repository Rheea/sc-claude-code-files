#!/usr/bin/env python3
"""
Test syntax fixes and code issues without requiring full dependencies
"""
import ast
import sys
import os
import re

def test_python_syntax():
    """Test that all Python files have valid syntax"""
    
    print("🔍 Testing Python syntax...")
    
    files_to_test = [
        '../dashboard.py',
        '../data_loader.py', 
        '../business_metrics.py'
    ]
    
    success = True
    
    for file_path in files_to_test:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  File not found: {file_path}")
            continue
            
        try:
            with open(full_path, 'r') as f:
                source_code = f.read()
                
            # Parse the AST to check for syntax errors
            ast.parse(source_code)
            print(f"✅ {file_path} - Valid syntax")
            
        except SyntaxError as e:
            print(f"❌ {file_path} - Syntax error: {e}")
            success = False
        except Exception as e:
            print(f"❌ {file_path} - Error: {e}")
            success = False
            
    return success


def test_plotly_method_usage():
    """Test that Plotly methods are used correctly"""
    
    print("\n🔍 Testing Plotly method usage...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    if not os.path.exists(dashboard_path):
        print("❌ dashboard.py not found")
        return False
        
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for incorrect method usage
    incorrect_methods = [
        ('update_yaxis', 'update_yaxes'),
        ('update_xaxis', 'update_xaxes')
    ]
    
    success = True
    
    for incorrect, correct in incorrect_methods:
        if incorrect in content:
            print(f"❌ Found {incorrect} - should use {correct}")
            success = False
        else:
            print(f"✅ No {incorrect} found (correct)")
            
    # Check for correct method usage
    correct_methods = ['update_yaxes', 'update_xaxes', 'update_layout']
    
    for method in correct_methods:
        if method in content:
            print(f"✅ Found {method} (correct)")
        else:
            print(f"ℹ️  {method} not found (may not be needed)")
            
    return success


def test_import_structure():
    """Test import statements for potential issues"""
    
    print("\n🔍 Testing import structure...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for required imports
    required_imports = [
        'streamlit',
        'pandas',
        'plotly.express',
        'plotly.graph_objects'
    ]
    
    success = True
    
    for import_name in required_imports:
        if import_name in content:
            print(f"✅ {import_name} import found")
        else:
            print(f"❌ {import_name} import missing")
            success = False
            
    return success


def test_function_definitions():
    """Test that all required functions are defined"""
    
    print("\n🔍 Testing function definitions...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Required functions
    required_functions = [
        'format_currency',
        'format_currency_axis', 
        'format_trend',
        'create_revenue_trend_chart',
        'create_category_chart',
        'create_state_map',
        'create_satisfaction_delivery_chart',
        'main'
    ]
    
    success = True
    
    for func_name in required_functions:
        pattern = rf'def {func_name}\s*\('
        if re.search(pattern, content):
            print(f"✅ Function {func_name} defined")
        else:
            print(f"❌ Function {func_name} missing")
            success = False
            
    return success


def test_specific_fixes():
    """Test that specific reported issues are fixed"""
    
    print("\n🔍 Testing specific fixes...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Test that AttributeError fix is applied
    if 'update_yaxis' not in content and 'update_xaxis' not in content:
        print("✅ AttributeError fix applied (no update_yaxis/update_xaxis)")
    else:
        print("❌ AttributeError fix not complete")
        return False
        
    # Test that currency formatting is implemented
    if 'format_currency_axis' in content:
        print("✅ Currency axis formatting implemented")
    else:
        print("❌ Currency axis formatting missing")
        return False
        
    # Test trend formatting
    if 'format_trend' in content and '↗' in content and '↘' in content:
        print("✅ Trend arrows implemented")  
    else:
        print("❌ Trend arrows missing")
        return False
        
    return True


def run_comprehensive_syntax_check():
    """Run all syntax and structure tests"""
    
    print("=" * 60)
    print("COMPREHENSIVE SYNTAX & STRUCTURE CHECK")
    print("=" * 60)
    
    tests = [
        ("Python Syntax", test_python_syntax),
        ("Plotly Methods", test_plotly_method_usage),
        ("Import Structure", test_import_structure),
        ("Function Definitions", test_function_definitions),
        ("Specific Fixes", test_specific_fixes)
    ]
    
    all_success = True
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        success = test_func()
        all_success &= success
        
        if success:
            print(f"✅ {test_name} - PASSED")
        else:
            print(f"❌ {test_name} - FAILED")
    
    print("\n" + "=" * 60)
    if all_success:
        print("🎉 ALL SYNTAX CHECKS PASSED!")
        print("The dashboard should now run without AttributeError issues.")
    else:
        print("⚠️  SOME CHECKS FAILED - Review issues above")
    print("=" * 60)
    
    return all_success


if __name__ == "__main__":
    success = run_comprehensive_syntax_check()
    sys.exit(0 if success else 1)