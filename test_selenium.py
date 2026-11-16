import os
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = os.environ.get("APP_URL", "http://127.0.0.1:5000")


class TestWebInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        if os.environ.get("HEADLESS", "1") == "1":
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=900,700")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def submit(self, grades):
        self.driver.get(URL)
        field = self.driver.find_element(By.ID, "grades")
        field.clear()
        if grades:
            field.send_keys(grades)
        self.driver.find_element(By.ID, "calculate").click()

    def get_text(self, element_id):
        """Attend l'apparition de l'élément (rechargement de la page) puis retourne son texte."""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        return element.text

    def test_1_average_15(self):
        self.submit("12,15,18")
        self.assertEqual(self.get_text("average"), "15.0")

    def test_2_average_10(self):
        self.submit("10,10,10")
        self.assertEqual(self.get_text("average"), "10.0")

    def test_3_mention_echec(self):
        self.submit("8,8,8")
        self.assertEqual(self.get_text("mention"), "Échec")

    def test_4_mention_excellent(self):
        self.submit("18,18,18")
        self.assertEqual(self.get_text("mention"), "Excellent")

    def test_5_invalid_grade(self):
        self.submit("12,25,18")
        self.assertIn("Erreur", self.get_text("error"))

    def test_6_empty_input(self):
        self.submit("")
        self.assertIn("Erreur", self.get_text("error"))


if __name__ == "__main__":
    unittest.main()
