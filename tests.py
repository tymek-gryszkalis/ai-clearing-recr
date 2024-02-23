import unittest
from unittest import TestCase
import requests

URL = "http://127.0.0.1:5000/"

class APIStructureTests(TestCase):
    def testStatusOfCode200(self):
        result = requests.get(f"{URL}cars")
        assert result.status_code == 200

    def testStatusOfCode400(self):
        result = requests.get(f"{URL}popular", json = {"invalidKey" : "invalidValue"})
        assert result.status_code == 400

    def testStatusOfCode404(self):
        result = requests.get(f"{URL}doesNotExist")
        assert result.status_code == 404

if __name__ == "__main__":
    unittest.main()