
import simplejson as json

def test_json_response_format(testcase, response):
    """Reusable test for ensuring valid json response format"""
    data = json.loads(response.data)
    testcase.assertIsInstance(data, dict)
    # TODO make this test more comprehensive