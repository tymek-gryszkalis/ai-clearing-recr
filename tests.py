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

class postCarsTests(TestCase):
    def testPostCarValidBody(self):
        result = requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "civic"})
        resultBody = result.json()
        assert resultBody["id"]

    def testPostCarInvalidBody(self):
        result = requests.post(f"{URL}cars", json = {"invalidKey" : "invalidValue"})
        assert result.status_code == 400

    def testPostCarInvalidMakeInvalidModel(self):
        result = requests.post(f"{URL}cars", json = {"make" : "invalidMake", "model" : "invalidModel"})
        assert result.status_code == 404

    def testPostCarValidMakeInvalidModel(self):
        result = requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "invalidModel"})
        assert result.status_code == 404

class getCarsTests(TestCase):
    def testGetCars(self):
        result = requests.get(f"{URL}cars")
        resultBody = result.json()
        assert resultBody["cars"]

class postRateTests(TestCase):
    def testPostRateValidBody(self):
        requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "civic"})
        result = requests.post(f"{URL}rate", json = {"id" : 1, "value" : 5})
        resultBody = result.json()
        assert resultBody["id"]

    def testPostRateInvalidBody(self):
        result = requests.post(f"{URL}rate", json = {"invalidKey" : "invalidValue"})
        assert result.status_code == 400

    def testPostRateInvalidCarId(self):
        result = requests.post(f"{URL}rate", json = {"id" : -1, "value" : 5})
        assert result.status_code == 404

    def testPostRateInvalidValue(self):
        requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "civic"})
        result = requests.post(f"{URL}rate", json = {"id" : 1, "value" : 6})
        assert result.status_code == 400

if __name__ == "__main__":
    unittest.main()