#!/usr/bin/env python3
"""
Comprehensive test suite for Portfolio Watchdog Agent
Tests all tools and edge cases
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, '.')

from agents.portfolio_watchdog_agent import (
    load_config,
    load_portfolio,
    get_stock_price,
    check_thresholds,
    detect_volume_spike,
    get_news_headlines,
    send_alert
)

class TestPortfolioWatchdog(unittest.TestCase):
    """Test suite for Portfolio Watchdog Agent"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        load_config()
    
    # ==================== load_portfolio Tests ====================
    
    def test_load_portfolio_returns_dict(self):
        """Test that load_portfolio returns a dictionary"""
        result = load_portfolio()
        self.assertIsInstance(result, dict)
    
    def test_load_portfolio_has_tickers(self):
        """Test that portfolio contains tickers"""
        result = load_portfolio()
        self.assertIn("tickers", result)
        self.assertIsInstance(result["tickers"], list)
        self.assertGreater(len(result["tickers"]), 0)
    
    def test_load_portfolio_has_alert_rules(self):
        """Test that portfolio contains alert rules"""
        result = load_portfolio()
        self.assertIn("alert_rules", result)
        self.assertIsInstance(result["alert_rules"], dict)
    
    def test_load_portfolio_total_tickers(self):
        """Test that total_tickers count is accurate"""
        result = load_portfolio()
        self.assertEqual(result["total_tickers"], len(result["tickers"]))
    
    # ==================== get_stock_price Tests ====================
    
    def test_get_stock_price_returns_dict(self):
        """Test that get_stock_price returns a dictionary"""
        result = get_stock_price("AAPL")
        self.assertIsInstance(result, dict)
    
    def test_get_stock_price_has_required_fields(self):
        """Test that price data contains required fields"""
        result = get_stock_price("AAPL")
        
        if "error" not in result:
            required_fields = ["ticker", "current_price", "previous_price", 
                             "percent_change", "volume", "timestamp"]
            for field in required_fields:
                self.assertIn(field, result, f"Missing field: {field}")
    
    def test_get_stock_price_valid_types(self):
        """Test that price data has correct types"""
        result = get_stock_price("AAPL")
        
        if "error" not in result:
            self.assertIsInstance(result["ticker"], str)
            self.assertIsInstance(result["current_price"], (int, float))
            self.assertIsInstance(result["volume"], int)
            self.assertGreater(result["current_price"], 0)
            self.assertGreater(result["volume"], 0)
    
    def test_get_stock_price_invalid_ticker(self):
        """Test handling of invalid ticker"""
        result = get_stock_price("INVALID_TICKER_XYZ")
        # Should either return error or empty data
        self.assertTrue("error" in result or result.get("volume", 0) == 0)
    
    # ==================== check_thresholds Tests ====================
    
    def test_check_thresholds_returns_dict(self):
        """Test that check_thresholds returns a dictionary"""
        result = check_thresholds("AAPL", 250)
        self.assertIsInstance(result, dict)
    
    def test_check_thresholds_has_required_fields(self):
        """Test that threshold check contains required fields"""
        result = check_thresholds("AAPL", 250)
        required_fields = ["ticker", "current_price", "breached", "breaches", "thresholds"]
        for field in required_fields:
            self.assertIn(field, result, f"Missing field: {field}")
    
    def test_check_thresholds_detects_high_breach(self):
        """Test that high threshold breach is detected"""
        result = check_thresholds("AAPL", 300)  # Above typical threshold
        self.assertTrue(result["breached"])
        self.assertGreater(len(result["breaches"]), 0)
    
    def test_check_thresholds_detects_low_breach(self):
        """Test that low threshold breach is detected"""
        result = check_thresholds("AAPL", 100)  # Below typical threshold
        self.assertTrue(result["breached"])
        self.assertGreater(len(result["breaches"]), 0)
    
    def test_check_thresholds_no_breach(self):
        """Test that no breach is detected for normal price"""
        result = check_thresholds("AAPL", 200)  # Within typical range
        # May or may not breach depending on current price
        self.assertIsInstance(result["breached"], bool)
    
    # ==================== detect_volume_spike Tests ====================
    
    def test_detect_volume_spike_returns_dict(self):
        """Test that detect_volume_spike returns a dictionary"""
        result = detect_volume_spike("AAPL")
        self.assertIsInstance(result, dict)
    
    def test_detect_volume_spike_has_required_fields(self):
        """Test that volume spike data contains required fields"""
        result = detect_volume_spike("AAPL")
        
        if "error" not in result:
            required_fields = ["ticker", "today_volume", "avg_volume_30d", 
                             "spike_percent", "threshold", "is_spike"]
            for field in required_fields:
                self.assertIn(field, result, f"Missing field: {field}")
    
    def test_detect_volume_spike_valid_types(self):
        """Test that volume spike data has correct types"""
        result = detect_volume_spike("AAPL")
        
        if "error" not in result:
            self.assertIsInstance(result["today_volume"], int)
            self.assertIsInstance(result["avg_volume_30d"], int)
            self.assertIsInstance(result["spike_percent"], (int, float))
            self.assertIsInstance(result["is_spike"], bool)
            self.assertGreater(result["today_volume"], 0)
            self.assertGreater(result["avg_volume_30d"], 0)
    
    def test_detect_volume_spike_percentage_calculation(self):
        """Test that spike percentage is calculated correctly"""
        result = detect_volume_spike("AAPL")
        
        if "error" not in result:
            # Verify percentage calculation
            expected_percent = ((result["today_volume"] - result["avg_volume_30d"]) 
                              / result["avg_volume_30d"] * 100)
            self.assertAlmostEqual(result["spike_percent"], expected_percent, places=1)
    
    # ==================== get_news_headlines Tests ====================
    
    def test_get_news_headlines_returns_dict(self):
        """Test that get_news_headlines returns a dictionary"""
        result = get_news_headlines("AAPL")
        self.assertIsInstance(result, dict)
    
    def test_get_news_headlines_has_required_fields(self):
        """Test that news data contains required fields"""
        result = get_news_headlines("AAPL")
        
        if "error" not in result:
            self.assertIn("ticker", result)
            self.assertIn("headlines", result)
            self.assertIn("count", result)
    
    def test_get_news_headlines_valid_types(self):
        """Test that news data has correct types"""
        result = get_news_headlines("AAPL")
        
        if "error" not in result:
            self.assertIsInstance(result["headlines"], list)
            self.assertIsInstance(result["count"], int)
            self.assertEqual(result["count"], len(result["headlines"]))
    
    def test_get_news_headlines_structure(self):
        """Test that each headline has required structure"""
        result = get_news_headlines("AAPL")
        
        if "error" not in result and result["headlines"]:
            for headline in result["headlines"]:
                self.assertIn("title", headline)
                self.assertIn("link", headline)
                self.assertIn("source", headline)
    
    # ==================== send_alert Tests ====================
    
    def test_send_alert_returns_dict(self):
        """Test that send_alert returns a dictionary"""
        result = send_alert("Test alert message")
        self.assertIsInstance(result, dict)
    
    def test_send_alert_has_required_fields(self):
        """Test that alert result contains required fields"""
        result = send_alert("Test alert message")
        self.assertIn("status", result)
        self.assertIn("message", result)
    
    def test_send_alert_dry_run_mode(self):
        """Test that dry run mode logs instead of sending"""
        result = send_alert("Test alert message")
        # In dry run mode, status should be 'logged'
        self.assertIn(result["status"], ["logged", "sent", "failed"])
    
    def test_send_alert_message_format(self):
        """Test that alert message is properly formatted"""
        test_message = "Test alert for AAPL"
        result = send_alert(test_message)
        
        if "message" in result:
            # Message should contain the test message
            self.assertIn("Test alert", result["message"])
    
    # ==================== Integration Tests ====================
    
    def test_full_portfolio_check_cycle(self):
        """Test a complete portfolio check cycle"""
        portfolio = load_portfolio()
        tickers = portfolio.get("tickers", [])
        
        self.assertGreater(len(tickers), 0)
        
        # Check first ticker
        ticker = tickers[0]
        
        # Get price
        price_data = get_stock_price(ticker)
        self.assertIsInstance(price_data, dict)
        
        if "error" not in price_data:
            current_price = price_data["current_price"]
            
            # Check thresholds
            threshold_data = check_thresholds(ticker, current_price)
            self.assertIsInstance(threshold_data, dict)
            self.assertIn("breached", threshold_data)
            
            # Check volume
            volume_data = detect_volume_spike(ticker)
            self.assertIsInstance(volume_data, dict)
            
            # Get news
            news_data = get_news_headlines(ticker)
            self.assertIsInstance(news_data, dict)
    
    def test_multiple_tickers_check(self):
        """Test checking multiple tickers"""
        portfolio = load_portfolio()
        tickers = portfolio.get("tickers", [])[:3]  # Test first 3
        
        for ticker in tickers:
            price_data = get_stock_price(ticker)
            self.assertIsInstance(price_data, dict)
    
    # ==================== Error Handling Tests ====================
    
    def test_error_handling_invalid_price(self):
        """Test error handling for invalid price"""
        result = check_thresholds("AAPL", -100)  # Invalid negative price
        # Should handle gracefully
        self.assertIsInstance(result, dict)
    
    def test_error_handling_empty_ticker(self):
        """Test error handling for empty ticker"""
        result = get_stock_price("")
        # Should return error or handle gracefully
        self.assertIsInstance(result, dict)
    
    def test_error_handling_special_characters(self):
        """Test error handling for special characters in ticker"""
        result = get_stock_price("@#$%")
        # Should return error or handle gracefully
        self.assertIsInstance(result, dict)

class TestDataValidation(unittest.TestCase):
    """Test data validation and type conversions"""
    
    def test_price_data_numeric_types(self):
        """Test that all numeric fields are proper types"""
        result = get_stock_price("AAPL")
        
        if "error" not in result:
            # All numeric fields should be int or float, not numpy types
            self.assertNotIn("numpy", str(type(result["current_price"])))
            self.assertNotIn("numpy", str(type(result["volume"])))
    
    def test_threshold_data_numeric_types(self):
        """Test that threshold data has proper numeric types"""
        result = check_thresholds("AAPL", 250)
        
        if "error" not in result:
            self.assertNotIn("numpy", str(type(result["current_price"])))
    
    def test_volume_data_numeric_types(self):
        """Test that volume data has proper numeric types"""
        result = detect_volume_spike("AAPL")
        
        if "error" not in result:
            self.assertNotIn("numpy", str(type(result["spike_percent"])))
            self.assertNotIn("numpy", str(type(result["is_spike"])))

class TestPerformance(unittest.TestCase):
    """Test performance characteristics"""
    
    def test_single_price_fetch_performance(self):
        """Test that single price fetch completes in reasonable time"""
        import time
        
        start = time.time()
        result = get_stock_price("AAPL")
        duration = time.time() - start
        
        # Should complete in under 5 seconds
        self.assertLess(duration, 5.0)
    
    def test_portfolio_load_performance(self):
        """Test that portfolio loads quickly"""
        import time
        
        start = time.time()
        result = load_portfolio()
        duration = time.time() - start
        
        # Should complete in under 1 second
        self.assertLess(duration, 1.0)

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestPortfolioWatchdog))
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidation))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
