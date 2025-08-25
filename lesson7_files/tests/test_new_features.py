#!/usr/bin/env python3
"""
Test new filtering features: default year 2023, month filters, no empty months
"""
import sys
import os
import ast
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_default_year_2023():
    """Test that default year is set to 2023"""
    
    print("🔍 Testing default year setting...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for 2023 default logic
    if 'if 2023 in available_years:' in content:
        print("✅ Found 2023 default year logic")
    else:
        print("❌ 2023 default year logic missing")
        return False
        
    # Check that it's set as default_year_index
    if 'default_year_index = available_years.index(2023)' in content:
        print("✅ 2023 set as default index")
    else:
        print("❌ 2023 not set as default index")
        return False
        
    return True


def test_month_filter_added():
    """Test that month filter has been added"""
    
    print("\n🔍 Testing month filter implementation...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for month filter elements
    checks = [
        ('Month filter selectbox', 'st.selectbox.*Month'),
        ('Available months logic', 'available_months'),
        ('Month conversion', 'selected_month.*int'),
        ('Three column layout', 'st.columns.*2.*1.*1')
    ]
    
    success = True
    
    for check_name, pattern in checks:
        if re.search(pattern, content, re.DOTALL):
            print(f"✅ {check_name} found")
        else:
            print(f"❌ {check_name} missing")
            success = False
            
    return success


def test_empty_months_filtering():
    """Test that empty months are filtered out"""
    
    print("\n🔍 Testing empty months filtering...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for logic to filter months with data
    checks = [
        ('Year-specific month filtering', 'year_orders.*purchase_year.*selected_year'),
        ('Available months from data', 'available_months.*sorted.*purchase_month'),
        ('Dropna for months', 'dropna'),
        ('Month name formatting', 'Jan.*Feb.*Mar')
    ]
    
    success = True
    
    for check_name, pattern in checks:
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            print(f"✅ {check_name} found")
        else:
            print(f"❌ {check_name} missing")
            success = False
            
    return success


def test_layout_structure():
    """Test that layout structure is maintained"""
    
    print("\n🔍 Testing layout structure...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check for maintained layout elements
    layout_elements = [
        'st.title("E-commerce Analytics Dashboard")',
        'Key Performance Indicators',
        'Performance Analytics',
        'Customer Experience Metrics',
        'kpi1, kpi2, kpi3, kpi4 = st.columns(4)',
        'chart_row1_col1, chart_row1_col2 = st.columns(2)',
        'bottom_col1, bottom_col2 = st.columns(2)'
    ]
    
    success = True
    
    for element in layout_elements:
        if element in content:
            print(f"✅ Layout element: {element[:40]}...")
        else:
            print(f"❌ Missing layout element: {element[:40]}...")
            success = False
            
    return success


def test_filtering_integration():
    """Test that filtering is properly integrated"""
    
    print("\n🔍 Testing filter integration...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    with open(dashboard_path, 'r') as f:
        content = f.read()
    
    # Check that selected_month is passed to create_sales_dataset
    if 'month_filter=selected_month' in content:
        print("✅ Month filter integrated with data loading")
    else:
        print("❌ Month filter not integrated with data loading")
        return False
        
    # Check that both year and month filters are used
    if 'year_filter=selected_year' in content and 'month_filter=selected_month' in content:
        print("✅ Both year and month filters used")
    else:
        print("❌ Filters not properly used")
        return False
        
    return True


def test_syntax_still_valid():
    """Test that syntax is still valid after changes"""
    
    print("\n🔍 Testing syntax validity...")
    
    dashboard_path = os.path.join(os.path.dirname(__file__), '../dashboard.py')
    
    try:
        with open(dashboard_path, 'r') as f:
            source_code = f.read()
            
        ast.parse(source_code)
        print("✅ Dashboard syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def run_new_features_tests():
    """Run all new feature tests"""
    
    print("=" * 70)
    print("TESTING NEW DASHBOARD FEATURES")
    print("=" * 70)
    
    tests = [
        ("Default Year 2023", test_default_year_2023),
        ("Month Filter Added", test_month_filter_added),
        ("Empty Months Filtering", test_empty_months_filtering),
        ("Layout Structure", test_layout_structure),
        ("Filter Integration", test_filtering_integration),
        ("Syntax Validity", test_syntax_still_valid)
    ]
    
    all_success = True
    
    for test_name, test_func in tests:
        success = test_func()
        all_success &= success
        
        if success:
            print(f"\n✅ {test_name} - PASSED")
        else:
            print(f"\n❌ {test_name} - FAILED")
    
    print("\n" + "=" * 70)
    if all_success:
        print("🎉 ALL NEW FEATURE TESTS PASSED!")
        print("\nNew Features Summary:")
        print("✅ Default year: 2023")
        print("✅ Month filter: Only months with data")
        print("✅ Layout: Title + Year + Month filters")
        print("✅ Integration: Filters work with data loading")
    else:
        print("⚠️  SOME NEW FEATURE TESTS FAILED")
    print("=" * 70)
    
    return all_success


if __name__ == "__main__":
    success = run_new_features_tests()
    sys.exit(0 if success else 1)