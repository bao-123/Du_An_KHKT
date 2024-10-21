from unittest import TestCase, main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')

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

    def test_test(self):
        self.driver.get("http://127.0.0.1:8000/")

        print("setup finish!")


if __name__ == "__main__":
    main()