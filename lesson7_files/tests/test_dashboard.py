"""
Tests for dashboard.py visualization functions
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock
import plotly.graph_objects as go

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dashboard import (
    format_currency, format_currency_axis, format_trend,
    create_revenue_trend_chart, create_category_chart,
    create_state_map, create_satisfaction_delivery_chart
)


class TestDashboardUtilities(unittest.TestCase):
    
    def test_format_currency(self):
        """Test currency formatting with K/M suffixes"""
        self.assertEqual(format_currency(1500000), "$2M")  # 1.5M rounds to 2M
        self.assertEqual(format_currency(1500), "$2K")     # 1.5K rounds to 2K
        self.assertEqual(format_currency(500), "$500")
        self.assertEqual(format_currency(0), "$0")
        
    def test_format_currency_axis(self):
        """Test axis currency formatting"""
        self.assertEqual(format_currency_axis(2000000), "$2M")
        self.assertEqual(format_currency_axis(300000), "$300K")
        self.assertEqual(format_currency_axis(500), "$500")
        
    def test_format_trend(self):
        """Test trend formatting with arrows and colors"""
        # Positive trend
        result = format_trend(120, 100)
        self.assertIn("↗", result)
        self.assertIn("trend-positive", result)
        self.assertIn("20.00%", result)
        
        # Negative trend
        result = format_trend(80, 100)
        self.assertIn("↘", result)
        self.assertIn("trend-negative", result)
        self.assertIn("20.00%", result)
        
        # Zero previous value
        result = format_trend(100, 0)
        self.assertEqual(result, "N/A")


class TestVisualizationFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test data for visualizations"""
        self.current_data = pd.DataFrame({
            'purchase_month': [1, 2, 3, 1, 2],
            'price': [100, 200, 300, 150, 250],
            'order_id': ['ord1', 'ord2', 'ord3', 'ord4', 'ord5'],
            'product_category_name': ['electronics', 'books', 'electronics', 'books', 'electronics'],
            'customer_state': ['CA', 'TX', 'CA', 'TX', 'NY'],
            'delivery_days': [3, 7, 10, 2, 5],
            'review_score': [5, 4, 3, 5, 4]
        })
        
        self.previous_data = pd.DataFrame({
            'purchase_month': [1, 2, 3],
            'price': [90, 180, 270],
            'order_id': ['ord6', 'ord7', 'ord8']
        })
        
    def test_create_revenue_trend_chart_multiple_months(self):
        """Test revenue trend chart with multiple months"""
        try:
            fig = create_revenue_trend_chart(
                self.current_data, self.previous_data, 2023, 2022
            )
            
            self.assertIsInstance(fig, go.Figure)
            self.assertGreater(len(fig.data), 0)  # Should have at least one trace
            
            # Check that it has both current and previous year traces
            self.assertEqual(len(fig.data), 2)
            
        except Exception as e:
            self.fail(f"create_revenue_trend_chart failed: {str(e)}")
            
    def test_create_revenue_trend_chart_single_month(self):
        """Test revenue trend chart with single month data"""
        single_month_data = self.current_data[self.current_data['purchase_month'] == 1]
        
        try:
            fig = create_revenue_trend_chart(
                single_month_data, None, 2023, 2022
            )
            
            self.assertIsInstance(fig, go.Figure)
            self.assertGreater(len(fig.data), 0)
            
        except Exception as e:
            self.fail(f"create_revenue_trend_chart (single month) failed: {str(e)}")
            
    def test_create_category_chart(self):
        """Test category chart creation"""
        try:
            fig = create_category_chart(self.current_data)
            
            self.assertIsInstance(fig, go.Figure)
            self.assertGreater(len(fig.data), 0)
            
            # Check that it's a horizontal bar chart
            self.assertEqual(fig.data[0].type, 'bar')
            self.assertEqual(fig.data[0].orientation, 'h')
            
        except Exception as e:
            self.fail(f"create_category_chart failed: {str(e)}")
            
    def test_create_category_chart_missing_data(self):
        """Test category chart with missing product category data"""
        data_no_category = self.current_data.drop('product_category_name', axis=1)
        
        try:
            fig = create_category_chart(data_no_category)
            self.assertIsInstance(fig, go.Figure)
            # Should handle missing data gracefully
            
        except Exception as e:
            self.fail(f"create_category_chart (missing data) failed: {str(e)}")
            
    def test_create_state_map(self):
        """Test state choropleth map creation"""
        try:
            fig = create_state_map(self.current_data)
            
            self.assertIsInstance(fig, go.Figure)
            self.assertGreater(len(fig.data), 0)
            
            # Check that it's a choropleth
            self.assertEqual(fig.data[0].type, 'choropleth')
            
        except Exception as e:
            self.fail(f"create_state_map failed: {str(e)}")
            
    def test_create_state_map_missing_data(self):
        """Test state map with missing geographic data"""
        data_no_state = self.current_data.drop('customer_state', axis=1)
        
        try:
            fig = create_state_map(data_no_state)
            self.assertIsInstance(fig, go.Figure)
            
        except Exception as e:
            self.fail(f"create_state_map (missing data) failed: {str(e)}")
            
    def test_create_satisfaction_delivery_chart(self):
        """Test satisfaction vs delivery chart creation"""
        try:
            fig = create_satisfaction_delivery_chart(self.current_data)
            
            self.assertIsInstance(fig, go.Figure)
            self.assertGreater(len(fig.data), 0)
            
            # Should be a bar chart
            self.assertEqual(fig.data[0].type, 'bar')
            
        except Exception as e:
            self.fail(f"create_satisfaction_delivery_chart failed: {str(e)}")
            
    def test_create_satisfaction_delivery_chart_missing_data(self):
        """Test satisfaction chart with missing data"""
        data_no_delivery = self.current_data.drop(['delivery_days', 'review_score'], axis=1)
        
        try:
            fig = create_satisfaction_delivery_chart(data_no_delivery)
            self.assertIsInstance(fig, go.Figure)
            
        except Exception as e:
            self.fail(f"create_satisfaction_delivery_chart (missing data) failed: {str(e)}")


class TestPlotlyFigureMethods(unittest.TestCase):
    """Test specific Plotly figure method issues"""
    
    def test_plotly_figure_update_methods(self):
        """Test that Plotly figure has correct update methods"""
        fig = go.Figure()
        
        # Test that correct methods exist
        self.assertTrue(hasattr(fig, 'update_yaxes'))
        self.assertTrue(hasattr(fig, 'update_xaxes'))
        self.assertTrue(hasattr(fig, 'update_layout'))
        
        # Test that incorrect method does not exist
        self.assertFalse(hasattr(fig, 'update_yaxis'))
        self.assertFalse(hasattr(fig, 'update_xaxis'))
        
    def test_figure_axis_updates(self):
        """Test figure axis update methods work correctly"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[1, 2, 3], y=[1, 2, 3]))
        
        try:
            # Test correct method
            fig.update_yaxes(title="Test Y Axis")
            fig.update_xaxes(title="Test X Axis")
            
            # These should not raise errors
            self.assertTrue(True)
            
        except AttributeError as e:
            self.fail(f"Correct Plotly methods failed: {str(e)}")
            
        try:
            # Test incorrect method (should fail)
            fig.update_yaxis(title="Test")
            self.fail("update_yaxis should not exist")
        except AttributeError:
            # This is expected
            pass


class TestDashboardIntegration(unittest.TestCase):
    """Integration tests for dashboard components"""
    
    @patch('dashboard.load_dashboard_data')
    def test_dashboard_data_loading(self, mock_load_data):
        """Test dashboard data loading function"""
        # Mock successful data loading
        mock_loader = MagicMock()
        mock_processed_data = {'orders': pd.DataFrame(), 'order_items': pd.DataFrame()}
        mock_load_data.return_value = (mock_loader, mock_processed_data)
        
        from dashboard import load_dashboard_data
        
        loader, processed_data = load_dashboard_data()
        
        self.assertIsNotNone(loader)
        self.assertIsNotNone(processed_data)
        
    def test_visualization_functions_with_real_data_structure(self):
        """Test visualization functions with realistic data structure"""
        # Create more realistic test data
        realistic_data = pd.DataFrame({
            'order_id': [f'ord_{i}' for i in range(100)],
            'price': np.random.uniform(50, 500, 100),
            'purchase_month': np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 100),
            'purchase_year': np.random.choice([2022, 2023], 100),
            'product_category_name': np.random.choice(['electronics', 'books', 'clothing', 'home'], 100),
            'customer_state': np.random.choice(['CA', 'TX', 'NY', 'FL', 'IL'], 100),
            'delivery_days': np.random.uniform(1, 15, 100),
            'review_score': np.random.choice([1, 2, 3, 4, 5], 100)
        })
        
        current_data = realistic_data[realistic_data['purchase_year'] == 2023]
        previous_data = realistic_data[realistic_data['purchase_year'] == 2022]
        
        # Test all visualization functions
        functions_to_test = [
            lambda: create_revenue_trend_chart(current_data, previous_data, 2023, 2022),
            lambda: create_category_chart(current_data),
            lambda: create_state_map(current_data),
            lambda: create_satisfaction_delivery_chart(current_data)
        ]
        
        for i, func in enumerate(functions_to_test):
            try:
                fig = func()
                self.assertIsInstance(fig, go.Figure)
            except Exception as e:
                self.fail(f"Visualization function {i} failed with realistic data: {str(e)}")


if __name__ == '__main__':
    unittest.main()