from unittest import TestCase, main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from subprocess import run

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
        run("python manage.py runserver")
        print("set up finished.")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        run("^C")
        print("clearing...")
        super().tearDownClass()

    def test_welcome(self):
        self.driver.get(BASE_URL)
        background_image = self.driver.find_element(by=By.TAG_NAME, value="img")

        self.assertEqual("fixed", background_image.value_of_css_property("position"))
        print("test welcome page finished!")
    


if __name__ == "__main__":
    main()