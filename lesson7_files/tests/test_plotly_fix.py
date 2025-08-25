#!/usr/bin/env python3
"""
Focused test for the specific Plotly AttributeError issue
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_plotly_methods():
    """Test Plotly figure methods to identify the specific AttributeError"""
    
    try:
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import plotly: {e}")
        return False
    
    # Create a test figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 4, 2]))
    
    print("\n🔍 Testing Plotly Figure methods:")
    
    # Test methods that should exist
    methods_to_test = [
        ('update_layout', True),
        ('update_yaxes', True), 
        ('update_xaxes', True),
        ('update_yaxis', False),  # This should NOT exist
        ('update_xaxis', False)   # This should NOT exist
    ]
    
    for method_name, should_exist in methods_to_test:
        has_method = hasattr(fig, method_name)
        
        if should_exist:
            if has_method:
                print(f"✅ {method_name} - EXISTS (correct)")
            else:
                print(f"❌ {method_name} - MISSING (should exist)")
                return False
        else:
            if has_method:
                print(f"⚠️  {method_name} - EXISTS (should not exist)")
            else:
                print(f"✅ {method_name} - MISSING (correct)")
    
    # Test the specific methods that were causing issues
    print("\n🧪 Testing problematic method calls:")
    
    try:
        # This should work
        fig.update_yaxes(title="Test Y Axis")
        print("✅ fig.update_yaxes() - SUCCESS")
    except AttributeError as e:
        print(f"❌ fig.update_yaxes() - FAILED: {e}")
        return False
    
    try:
        # This should fail if using correct method names
        fig.update_yaxis(title="Test")
        print("⚠️  fig.update_yaxis() - UNEXPECTEDLY SUCCEEDED")
    except AttributeError:
        print("✅ fig.update_yaxis() - CORRECTLY FAILED (method doesn't exist)")
    
    return True


def test_dashboard_import():
    """Test importing dashboard module to identify specific issues"""
    
    print("\n🔍 Testing dashboard module import:")
    
    try:
        # Try to import just the functions we need
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        
        # Test basic imports first
        import plotly.graph_objects as go
        print("✅ plotly.graph_objects imported")
        
        # Now try the dashboard functions
        from dashboard import format_currency, format_currency_axis, format_trend
        print("✅ Dashboard utility functions imported")
        
        # Test the functions
        result1 = format_currency(1500000)
        print(f"✅ format_currency(1500000) = {result1}")
        
        result2 = format_trend(120, 100)
        print(f"✅ format_trend(120, 100) = {result2}")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_figure_creation():
    """Test creating the specific figure that's failing"""
    
    print("\n🧪 Testing figure creation with problematic code:")
    
    try:
        import plotly.graph_objects as go
        
        # Create a simple figure like in the dashboard
        fig = go.Figure()
        fig.add_trace(go.Bar(x=['A', 'B', 'C'], y=[1, 2, 3]))
        
        # Test the problematic axis update
        try:
            # This is probably the line causing the error
            fig.update_yaxis(title="Test")
            print("⚠️  update_yaxis worked (unexpected)")
        except AttributeError as e:
            print(f"✅ update_yaxis failed as expected: {e}")
            
            # Try the correct method
            fig.update_yaxes(title="Test")
            print("✅ update_yaxes worked correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Figure creation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("FOCUSED PLOTLY DASHBOARD TESTING")
    print("=" * 60)
    
    success = True
    
    success &= test_plotly_methods()
    success &= test_dashboard_import() 
    success &= test_figure_creation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL FOCUSED TESTS PASSED!")
    else:
        print("⚠️  SOME FOCUSED TESTS FAILED")
    print("=" * 60)
    
    sys.exit(0 if success else 1)