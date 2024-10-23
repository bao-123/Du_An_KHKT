from unittest import TestCase, main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')

BASE_URL = "http://127.0.0.1:8000/"
#! Remember to run the server before run the test!
class ProjectTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome(options=options)
        super().setUpClass()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("All test finished!")
        super().tearDownClass()

    def test_welcome(self):
        self.driver.get(BASE_URL)

        print("setup finish!")
    


if __name__ == "__main__":
    main()