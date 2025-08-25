"""
Tests for business_metrics.py functionality
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from business_metrics import BusinessMetricsCalculator, MetricsVisualizer, format_currency, format_percentage


class TestBusinessMetricsCalculator(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.test_sales_data = pd.DataFrame({
            'order_id': ['ord1', 'ord1', 'ord2', 'ord3', 'ord4'],
            'price': [100.0, 50.0, 200.0, 300.0, 150.0],
            'purchase_year': [2023, 2023, 2023, 2022, 2022],
            'purchase_month': [1, 1, 2, 1, 2],
            'product_category_name': ['electronics', 'books', 'electronics', 'books', 'electronics'],
            'customer_state': ['CA', 'CA', 'TX', 'CA', 'TX'],
            'review_score': [5, 5, 4, 3, 4],
            'delivery_days': [3, 3, 7, 10, 5]
        })
        
    def test_metrics_calculator_initialization(self):
        """Test BusinessMetricsCalculator initialization"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        self.assertIsNotNone(calc.sales_data)
        self.assertEqual(len(calc.sales_data), 5)
        
    def test_validation_missing_columns(self):
        """Test validation with missing required columns"""
        invalid_data = pd.DataFrame({'invalid_col': [1, 2, 3]})
        
        with self.assertRaises(ValueError):
            BusinessMetricsCalculator(invalid_data)
            
    def test_calculate_revenue_metrics_current_year_only(self):
        """Test revenue metrics calculation for current year only"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        metrics = calc.calculate_revenue_metrics(current_year=2023)
        
        self.assertEqual(metrics['total_revenue'], 350.0)  # 100 + 50 + 200
        self.assertEqual(metrics['total_orders'], 2)  # ord1, ord2
        self.assertEqual(metrics['total_items_sold'], 3)  # 3 items in 2023
        
        # Average order value: (150 + 200) / 2 = 175
        expected_aov = (150.0 + 200.0) / 2
        self.assertEqual(metrics['average_order_value'], expected_aov)
        
    def test_calculate_revenue_metrics_with_comparison(self):
        """Test revenue metrics with year-over-year comparison"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        metrics = calc.calculate_revenue_metrics(current_year=2023, previous_year=2022)
        
        # Check growth calculations
        self.assertIn('revenue_growth_rate', metrics)
        self.assertIn('order_growth_rate', metrics)
        self.assertIn('aov_growth_rate', metrics)
        
        # 2023: 350, 2022: 450, growth = (350-450)/450 * 100 = -22.22%
        expected_growth = ((350.0 - 450.0) / 450.0) * 100
        self.assertAlmostEqual(metrics['revenue_growth_rate'], expected_growth, places=2)
        
    def test_calculate_monthly_trends(self):
        """Test monthly trends calculation"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        monthly_trends = calc.calculate_monthly_trends(year=2023)
        
        self.assertIsInstance(monthly_trends, pd.DataFrame)
        self.assertIn('month', monthly_trends.columns)
        self.assertIn('revenue', monthly_trends.columns)
        self.assertIn('orders', monthly_trends.columns)
        self.assertIn('revenue_growth', monthly_trends.columns)
        
        # Check specific values
        month1_data = monthly_trends[monthly_trends['month'] == 1]
        self.assertEqual(month1_data['revenue'].iloc[0], 150.0)  # 100 + 50
        
    def test_analyze_product_performance(self):
        """Test product performance analysis"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        performance = calc.analyze_product_performance(year=2023, top_n=5)
        
        self.assertIn('all_categories', performance)
        self.assertIn('top_categories', performance)
        
        all_categories = performance['all_categories']
        self.assertIn('product_category_name', all_categories.columns)
        self.assertIn('total_revenue', all_categories.columns)
        self.assertIn('revenue_share', all_categories.columns)
        
    def test_analyze_geographic_performance(self):
        """Test geographic performance analysis"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        geo_performance = calc.analyze_geographic_performance(year=2023)
        
        self.assertIsInstance(geo_performance, pd.DataFrame)
        self.assertIn('state', geo_performance.columns)
        self.assertIn('revenue', geo_performance.columns)
        self.assertIn('orders', geo_performance.columns)
        
    def test_analyze_customer_satisfaction(self):
        """Test customer satisfaction analysis"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        satisfaction = calc.analyze_customer_satisfaction(year=2023)
        
        self.assertIn('avg_review_score', satisfaction)
        self.assertIn('total_reviews', satisfaction)
        self.assertIn('score_5_percentage', satisfaction)
        self.assertIn('score_4_plus_percentage', satisfaction)
        
        # Check calculation: reviews for 2023 are [5, 5, 4], avg = 4.67
        expected_avg = (5 + 5 + 4) / 3
        self.assertAlmostEqual(satisfaction['avg_review_score'], expected_avg, places=2)
        
    def test_analyze_delivery_performance(self):
        """Test delivery performance analysis"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        delivery = calc.analyze_delivery_performance(year=2023)
        
        self.assertIn('avg_delivery_days', delivery)
        self.assertIn('median_delivery_days', delivery)
        self.assertIn('fast_delivery_percentage', delivery)
        self.assertIn('slow_delivery_percentage', delivery)
        
    def test_generate_comprehensive_report(self):
        """Test comprehensive report generation"""
        calc = BusinessMetricsCalculator(self.test_sales_data)
        
        report = calc.generate_comprehensive_report(current_year=2023, previous_year=2022)
        
        expected_keys = [
            'analysis_period', 'comparison_period', 'revenue_metrics',
            'monthly_trends', 'product_performance', 'geographic_performance',
            'customer_satisfaction', 'delivery_performance'
        ]
        
        for key in expected_keys:
            self.assertIn(key, report)
            
        self.assertEqual(report['analysis_period'], 2023)
        self.assertEqual(report['comparison_period'], 2022)


class TestMetricsVisualizer(unittest.TestCase):
    
    def setUp(self):
        """Set up test report data"""
        self.test_report = {
            'analysis_period': 2023,
            'comparison_period': 2022,
            'monthly_trends': pd.DataFrame({
                'month': [1, 2, 3],
                'revenue': [1000, 1200, 1100],
                'orders': [10, 12, 11]
            }),
            'product_performance': {
                'top_categories': pd.DataFrame({
                    'product_category_name': ['electronics', 'books', 'clothing'],
                    'total_revenue': [5000, 3000, 2000],
                    'revenue_share': [50.0, 30.0, 20.0]
                })
            },
            'geographic_performance': pd.DataFrame({
                'state': ['CA', 'TX', 'NY'],
                'revenue': [5000, 3000, 2000],
                'orders': [50, 30, 20]
            }),
            'customer_satisfaction': {
                'avg_review_score': 4.2,
                'score_5_percentage': 40.0,
                'score_4_plus_percentage': 80.0,
                'score_1_2_percentage': 5.0
            }
        }
        
    def test_visualizer_initialization(self):
        """Test MetricsVisualizer initialization"""
        visualizer = MetricsVisualizer(self.test_report)
        self.assertEqual(visualizer.report_data, self.test_report)
        self.assertIsNotNone(visualizer.color_palette)
        
    def test_plot_revenue_trend(self):
        """Test revenue trend plot creation"""
        visualizer = MetricsVisualizer(self.test_report)
        
        try:
            fig = visualizer.plot_revenue_trend()
            self.assertIsNotNone(fig)
            # Test that it returns a matplotlib figure
            self.assertTrue(hasattr(fig, 'savefig'))
        except Exception as e:
            self.fail(f"plot_revenue_trend failed: {str(e)}")
            
    def test_plot_category_performance(self):
        """Test category performance plot creation"""
        visualizer = MetricsVisualizer(self.test_report)
        
        try:
            fig = visualizer.plot_category_performance(top_n=3)
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"plot_category_performance failed: {str(e)}")
            
    def test_plot_geographic_heatmap(self):
        """Test geographic heatmap creation"""
        visualizer = MetricsVisualizer(self.test_report)
        
        try:
            fig = visualizer.plot_geographic_heatmap()
            self.assertIsNotNone(fig)
            # This should return a plotly figure
            self.assertTrue(hasattr(fig, 'show'))
        except Exception as e:
            self.fail(f"plot_geographic_heatmap failed: {str(e)}")
            
    def test_plot_review_distribution(self):
        """Test review distribution plot creation"""
        visualizer = MetricsVisualizer(self.test_report)
        
        try:
            fig = visualizer.plot_review_distribution()
            self.assertIsNotNone(fig)
        except Exception as e:
            self.fail(f"plot_review_distribution failed: {str(e)}")


class TestUtilityFunctions(unittest.TestCase):
    
    def test_format_currency(self):
        """Test currency formatting function"""
        self.assertEqual(format_currency(1234.56), "$1,234.56")
        self.assertEqual(format_currency(0), "$0.00")
        self.assertEqual(format_currency(-500.75), "$-500.75")
        
    def test_format_percentage(self):
        """Test percentage formatting function"""
        self.assertEqual(format_percentage(25.0), "25.0%")
        self.assertEqual(format_percentage(0.0), "0.0%")
        self.assertEqual(format_percentage(-5.5), "-5.5%")
        self.assertEqual(format_percentage(33.333, decimals=2), "33.33%")


if __name__ == '__main__':
    unittest.main()