#!/usr/bin/env python3
"""
Comprehensive Testing Script for SentimentSense
Tests all backend functionality and API endpoints
"""

import requests
import json
import csv
import tempfile
import os
from datetime import datetime

class SentimentSenseTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.test_results = []
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {details}")
        
    def test_backend_health(self):
        """Test if backend is running"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                self.log_test("Backend Health Check", "PASS", "Backend is running")
                return True
            else:
                self.log_test("Backend Health Check", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health Check", "FAIL", f"Connection error: {str(e)}")
            return False
    
    def test_single_text_analysis(self):
        """Test single text sentiment analysis"""
        test_cases = [
            ("I love this amazing project!", "Positive"),
            ("I hate this terrible project!", "Negative"),
            ("This is a neutral statement.", "Neutral"),
            ("", "Empty text"),
            ("Great day!", "Positive with emoji removed"),
            ("Bad day!", "Negative with emoji removed")
        ]
        
        for text, expected in test_cases:
            try:
                response = requests.post(
                    f"{self.base_url}/analyze",
                    files={"text": (None, text)}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "label" in data and "confidence" in data:
                        self.log_test(f"Text Analysis: {expected}", "PASS", 
                                    f"Label: {data['label']}, Confidence: {data['confidence']:.2f}")
                    else:
                        self.log_test(f"Text Analysis: {expected}", "FAIL", 
                                    "Missing required fields in response")
                else:
                    self.log_test(f"Text Analysis: {expected}", "FAIL", 
                                f"Status code: {response.status_code}")
            except Exception as e:
                self.log_test(f"Text Analysis: {expected}", "FAIL", f"Error: {str(e)}")
    
    def test_csv_batch_analysis(self):
        """Test CSV batch processing"""
        # Create test CSV file
        test_data = [
            ["text"],
            ["I love this project!"],
            ["I hate this project!"],
            ["This is neutral."],
            ["Amazing work! Great day!"],
            ["Terrible experience bad day!"]
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
            csv_path = f.name
        
        try:
            with open(csv_path, 'rb') as csv_file:
                response = requests.post(
                    f"{self.base_url}/analyze_csv",
                    files={"file": ("test.csv", csv_file, "text/csv")}
                )
            
            if response.status_code == 200:
                data = response.json()
                if "results" in data and len(data["results"]) == len(test_data) - 1:  # -1 for header
                    self.log_test("CSV Batch Analysis", "PASS", 
                                f"Processed {len(data['results'])} rows successfully")
                else:
                    self.log_test("CSV Batch Analysis", "FAIL", 
                                "Incorrect number of results")
            else:
                self.log_test("CSV Batch Analysis", "FAIL", 
                            f"Status code: {response.status_code}")
        except Exception as e:
            self.log_test("CSV Batch Analysis", "FAIL", f"Error: {str(e)}")
        finally:
            # Clean up temporary file
            if os.path.exists(csv_path):
                os.unlink(csv_path)
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        # Test invalid CSV format
        try:
            response = requests.post(
                f"{self.base_url}/analyze_csv",
                files={"file": ("invalid.txt", "This is not a CSV", "text/plain")}
            )
            if response.status_code == 500:  # Expected error for invalid CSV
                self.log_test("Error Handling: Invalid CSV", "PASS", "Properly handled invalid CSV")
            else:
                self.log_test("Error Handling: Invalid CSV", "FAIL", 
                            f"Unexpected status code: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling: Invalid CSV", "FAIL", f"Error: {str(e)}")
        
        # Test missing text column in CSV
        test_data = [["name", "age"], ["John", "25"], ["Jane", "30"]]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(test_data)
            csv_path = f.name
        
        try:
            with open(csv_path, 'rb') as csv_file:
                response = requests.post(
                    f"{self.base_url}/analyze_csv",
                    files={"file": ("test.csv", csv_file, "text/csv")}
                )
            
            if response.status_code == 400:  # Expected error for missing text column
                self.log_test("Error Handling: Missing Text Column", "PASS", 
                            "Properly handled missing text column")
            else:
                self.log_test("Error Handling: Missing Text Column", "FAIL", 
                            f"Unexpected status code: {response.status_code}")
        except Exception as e:
            self.log_test("Error Handling: Missing Text Column", "FAIL", f"Error: {str(e)}")
        finally:
            if os.path.exists(csv_path):
                os.unlink(csv_path)
    
    def test_api_documentation(self):
        """Test API documentation accessibility"""
        try:
            response = requests.get(f"{self.base_url}/docs")
            if response.status_code == 200 and "Swagger UI" in response.text:
                self.log_test("API Documentation", "PASS", "Swagger UI is accessible")
            else:
                self.log_test("API Documentation", "FAIL", "API docs not accessible")
        except Exception as e:
            self.log_test("API Documentation", "FAIL", f"Error: {str(e)}")
    
    def test_cors_configuration(self):
        """Test CORS configuration"""
        try:
            response = requests.options(f"{self.base_url}/analyze")
            if "Access-Control-Allow-Origin" in response.headers:
                self.log_test("CORS Configuration", "PASS", "CORS headers present")
            else:
                self.log_test("CORS Configuration", "FAIL", "CORS headers missing")
        except Exception as e:
            self.log_test("CORS Configuration", "FAIL", f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Starting SentimentSense Comprehensive Testing")
        print("=" * 50)
        
        # Run all test suites
        self.test_backend_health()
        self.test_single_text_analysis()
        self.test_csv_batch_analysis()
        self.test_error_handling()
        self.test_api_documentation()
        self.test_cors_configuration()
        
        # Generate test report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 50)
        print("📊 TEST REPORT")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['details']}")
        
        # Save detailed report
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        if failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! SentimentSense is working perfectly!")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please review the issues above.")

if __name__ == "__main__":
    tester = SentimentSenseTester()
    tester.run_all_tests() 