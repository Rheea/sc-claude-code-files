"""
Tests for data_loader.py functionality
"""
import unittest
import pandas as pd
import numpy as np
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_loader import EcommerceDataLoader, load_and_process_data, categorize_delivery_speed


class TestDataLoader(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_data_path = 'test_data/'
        
        # Create mock dataframes
        self.mock_orders = pd.DataFrame({
            'order_id': ['ord1', 'ord2', 'ord3'],
            'customer_id': ['cust1', 'cust2', 'cust3'],
            'order_status': ['delivered', 'delivered', 'canceled'],
            'order_purchase_timestamp': ['2023-01-01 10:00:00', '2023-02-01 11:00:00', '2023-03-01 12:00:00'],
            'order_delivered_customer_date': ['2023-01-05 10:00:00', '2023-02-08 11:00:00', None]
        })
        
        self.mock_order_items = pd.DataFrame({
            'order_id': ['ord1', 'ord2', 'ord3'],
            'order_item_id': [1, 1, 1],
            'product_id': ['prod1', 'prod2', 'prod3'],
            'price': [100.0, 200.0, 300.0],
            'freight_value': [10.0, 20.0, 30.0],
            'seller_id': ['sell1', 'sell2', 'sell3'],
            'shipping_limit_date': ['2023-01-03 10:00:00', '2023-02-03 11:00:00', '2023-03-03 12:00:00']
        })
        
        self.mock_products = pd.DataFrame({
            'product_id': ['prod1', 'prod2', 'prod3'],
            'product_category_name': ['electronics', 'books', 'electronics']
        })
        
        self.mock_customers = pd.DataFrame({
            'customer_id': ['cust1', 'cust2', 'cust3'],
            'customer_state': ['CA', 'TX', 'NY'],
            'customer_city': ['LA', 'Austin', 'NYC']
        })
        
        self.mock_reviews = pd.DataFrame({
            'order_id': ['ord1', 'ord2'],
            'review_score': [5, 4]
        })
    
    @patch('data_loader.pd.read_csv')
    @patch('data_loader.os.path.exists')
    def test_load_raw_data_success(self, mock_exists, mock_read_csv):
        """Test successful data loading"""
        mock_exists.return_value = True
        mock_read_csv.side_effect = [
            self.mock_orders,
            self.mock_order_items,
            self.mock_products,
            self.mock_customers,
            self.mock_reviews,
            pd.DataFrame()  # payments
        ]
        
        loader = EcommerceDataLoader(self.test_data_path)
        result = loader.load_raw_data()
        
        self.assertIn('orders', result)
        self.assertIn('order_items', result)
        self.assertEqual(len(result['orders']), 3)
        
    def test_clean_orders_data(self):
        """Test orders data cleaning"""
        loader = EcommerceDataLoader(self.test_data_path)
        loader.raw_data = {'orders': self.mock_orders}
        
        cleaned = loader.clean_orders_data()
        
        # Check timestamp conversion
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned['order_purchase_timestamp']))
        
        # Check date components
        self.assertIn('purchase_year', cleaned.columns)
        self.assertIn('purchase_month', cleaned.columns)
        self.assertEqual(cleaned['purchase_year'].iloc[0], 2023)
        self.assertEqual(cleaned['purchase_month'].iloc[0], 1)
        
    def test_clean_order_items_data(self):
        """Test order items data cleaning"""
        loader = EcommerceDataLoader(self.test_data_path)
        loader.raw_data = {'order_items': self.mock_order_items}
        
        cleaned = loader.clean_order_items_data()
        
        # Check total item value calculation
        self.assertIn('total_item_value', cleaned.columns)
        expected_total = 100.0 + 10.0  # price + freight
        self.assertEqual(cleaned['total_item_value'].iloc[0], expected_total)
        
    @patch('data_loader.pd.read_csv')
    @patch('data_loader.os.path.exists')
    def test_create_sales_dataset(self, mock_exists, mock_read_csv):
        """Test sales dataset creation"""
        mock_exists.return_value = True
        mock_read_csv.side_effect = [
            self.mock_orders,
            self.mock_order_items,
            self.mock_products,
            self.mock_customers,
            self.mock_reviews,
            pd.DataFrame()
        ]
        
        loader = EcommerceDataLoader(self.test_data_path)
        loader.load_raw_data()
        loader.process_all_data()
        
        # Test with year filter
        sales_data = loader.create_sales_dataset(year_filter=2023, status_filter='delivered')
        
        self.assertGreater(len(sales_data), 0)
        self.assertTrue(all(sales_data['purchase_year'] == 2023))
        self.assertTrue(all(sales_data['order_status'] == 'delivered'))
        
    def test_categorize_delivery_speed(self):
        """Test delivery speed categorization"""
        self.assertEqual(categorize_delivery_speed(2), '1-3 days')
        self.assertEqual(categorize_delivery_speed(5), '4-7 days')
        self.assertEqual(categorize_delivery_speed(10), '8+ days')
        self.assertEqual(categorize_delivery_speed(np.nan), 'Unknown')


class TestDataLoaderIntegration(unittest.TestCase):
    """Integration tests that require actual data files"""
    
    def setUp(self):
        self.data_path = 'ecommerce_data/'
        
    def test_data_files_exist(self):
        """Test that required data files exist"""
        required_files = [
            'orders_dataset.csv',
            'order_items_dataset.csv',
            'products_dataset.csv',
            'customers_dataset.csv',
            'order_reviews_dataset.csv'
        ]
        
        for filename in required_files:
            filepath = os.path.join(self.data_path, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing data file: {filename}")
    
    @patch('builtins.print')  # Suppress print statements during tests
    def test_load_and_process_data_integration(self, mock_print):
        """Test full data loading and processing pipeline"""
        try:
            loader, processed_data = load_and_process_data(self.data_path)
            
            # Check that loader is returned
            self.assertIsInstance(loader, EcommerceDataLoader)
            
            # Check that processed data contains expected keys
            expected_keys = ['orders', 'order_items']
            for key in expected_keys:
                self.assertIn(key, processed_data)
                self.assertIsInstance(processed_data[key], pd.DataFrame)
                self.assertGreater(len(processed_data[key]), 0)
                
        except Exception as e:
            self.fail(f"Integration test failed: {str(e)}")


if __name__ == '__main__':
    unittest.main()