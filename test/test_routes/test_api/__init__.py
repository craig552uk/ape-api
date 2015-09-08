
import simplejson as json

def assert_success_response(testcase, response):
    """Reusable test for ensuring valid json success response format"""
    data = json.loads(response.data)
    testcase.assertIsInstance(data, dict)
    testcase.assertEqual(data['status'], 200)
    testcase.assertIn('data', data.keys())
    return data

def assert_error_response(testcase, response, exception):
    """Reusable test for ensuring valid json error response format"""
    data = json.loads(response.data)
    testcase.assertIsInstance(data, dict)
    testcase.assertEqual(data['status'], exception.code)
    testcase.assertIn('title', data['error'].keys())
    testcase.assertIn('status', data['error'].keys())
    testcase.assertIn('detail', data['error'].keys())
    testcase.assertEqual(str(exception.code), data['error']['status'])
    testcase.assertEqual(str(exception.name), data['error']['title'])
    return data