from django.test import TestCase, Client
from django.urls import reverse
from .utils import TestUtils
from .models import *

# Create your tests here.

class ProjectTest(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        #create some subjects
        self.subjects = TestUtils.create_subjects(["Toán", "Ngữ Văn", "Tiếng Anh"])

        #create some classes
        self.classes = TestUtils.create_classes(["6a1", "6a2", "6a3"])

        #create some teachers
        self.teacher1 = TestUtils.create_user(type="teacher", email="teacher1@teacher.com",
                                              password="teacher1", full_name="Nguyễn Văn A",
                                              subjects=self.subjects[0])
        self.teacher2 = TestUtils.create_user(type="teacher", email="teacher2@teacher.com", 
                                              password="teacher2", full_name="Nguyễn Văn B", 
                                              subjects=[self.subjects[0], self.subjects[1]])
        
        #TODO: create some students to test register page

    def test_welcome_page(self):
        response = self.client.get(reverse(""))

        self.assertEqual(response.status_code, 200)
        print("Test welcome page finished. ✔")

    def test_login_page(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        print("test login page finished. ✔")
    
    def test_register_page(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["subjects"].count(), 3)
        self.assertEqual(response.context["classes"].count(), 3)
        print("Test register page finished. ✔")
