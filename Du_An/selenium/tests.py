from unittest import TestCase, main
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import Popen
import signal
import time
import os


options = Options()
#*Configurations for Chrome
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

BASE_URL = "http://127.0.0.1:8000/"
#! Remember to run the server before run the test!
class ProjectTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server_process = Popen(["python", "manage.py", "runserver", "127.0.0.1:8000"])
        time.sleep(3) #* Ensure that the server will be started before the test run.

        cls.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        super().setUpClass()
        print("set up finished.")
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

        if os.name == "nt": #* If the os is Window
            cls.server_process.terminate()
        else: #* For unix-like
            cls.server_process.send_signal(signal.SIGINT)

        cls.server_process.wait()

        print("clearing...")
        super().tearDownClass()

    def test_welcome(self):
        self.driver.get(BASE_URL)
        background_image = self.driver.find_element(by=By.ID, value="background-image")

        self.assertEqual("flex", background_image.value_of_css_property("display"))
        print("test welcome page finished!")
    


if __name__ == "__main__":
    main()