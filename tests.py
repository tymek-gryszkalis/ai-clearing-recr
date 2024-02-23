import unittest
from unittest import TestCase
import requests

URL = "http://127.0.0.1:5000/"
NOT_FOUND_CODE = 404
INVALID_REQUEST_CODE = 400

class postCarsTests(TestCase):
    def testPostCarValidBody(self):
        result = requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "civic"})
        resultBody = result.json()
        assert resultBody["id"]

    def testPostCarInvalidBody(self):
        result = requests.post(f"{URL}cars", json = {"invalidKey" : "invalidValue"})
        assert result.status_code == INVALID_REQUEST_CODE

    def testPostCarInvalidMakeInvalidModel(self):
        result = requests.post(f"{URL}cars", json = {"make" : "invalidMake", "model" : "invalidModel"})
        assert result.status_code == NOT_FOUND_CODE

    def testPostCarValidMakeInvalidModel(self):
        result = requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "invalidModel"})
        assert result.status_code == NOT_FOUND_CODE

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
        assert result.status_code == INVALID_REQUEST_CODE

    def testPostRateInvalidCarId(self):
        result = requests.post(f"{URL}rate", json = {"id" : -1, "value" : 5})
        assert result.status_code == NOT_FOUND_CODE

    def testPostRateInvalidValue(self):
        requests.post(f"{URL}cars", json = {"make" : "honda", "model" : "civic"})
        result = requests.post(f"{URL}rate", json = {"id" : 1, "value" : 6})
        assert result.status_code == INVALID_REQUEST_CODE

class getPopularTests(TestCase):
    def testGetPopularValidBody(self):
        result = requests.get(f"{URL}popular", json = {"amount" : 1})
        resultBody = result.json()
        assert resultBody["cars"]

    def testGetPopularInvalidBody(self):
        result = requests.post(f"{URL}rate", json = {"invalidKey" : "invalidValue"})
        assert result.status_code == INVALID_REQUEST_CODE

    def testGetPopularInvalidAmount(self):
        result = requests.get(f"{URL}popular", json = {"amount" : -1})
        assert result.status_code == INVALID_REQUEST_CODE
        
if __name__ == "__main__":
    unittest.main()