from django.test import TestCase, Client
from django.urls import reverse
from .utils import TestUtils
from .models import *
from datetime import date

# Create your tests here.
#TODO: fix
class ProjectTest(TestCase):

    @classmethod
    def setUp(self):
        self.client = Client()

        #* create some subjects
        self.subjects = TestUtils.create_subjects(["Toán", "Ngữ Văn", "Tiếng Anh"])


        #* create some teachers
        self.teacher1 = TestUtils.create_user(type="teacher", email="teacher1@teacher.com",
                                              password="teacher1", full_name="Nguyễn Văn A",
                                              subjects=[self.subjects[0],])
        self.teacher2 = TestUtils.create_user(type="teacher", email="teacher2@teacher.com", 
                                              password="teacher2", full_name="Nguyễn Văn B", 
                                              subjects=[self.subjects[0], self.subjects[1]])
        
        self.teacher3 = TestUtils.create_user(type="teacher", email="teacher3@teacher.com",
                                              password="teacher3", full_name="Nguyễn Thiên Bảo",
                                              subjects=[self.subjects[1], self.subjects[2]])
        
        self.classroom1 = TestUtils.create_classroom("6a1", form_teacher=self.teacher1, subject_teachers=[self.teacher2,])
        self.classroom2 = TestUtils.create_classroom("6a2", form_teacher=self.teacher3, subject_teachers=[self.teacher1, self.teacher2])

        
        #* create some students to test register page
        self.student1 = TestUtils.create_student(name="Nguyen Thien Bao", role="monitor",
                                                  is_boy=True, classroom=self.classes[0],
                                                  birthday=date.today())
        self.student2 = TestUtils.create_student(name="Tran Hoang Loc", role="art",
                                                  is_boy=True, classroom=self.classes[0],
                                                  birthday=date.today())
        self.student3 = TestUtils.create_student(name="Vo Trong Tin", is_boy=False,
                                                  role="monitor", classroom=self.classes[1],
                                                  birthday=date.today())



    def test_welcome_page(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        print("Test welcome page finished. ✔")

    def test_login_page(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        print("test login page finished. ✔")
    
    def test_register_page(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["subjects"]), 3)
        self.assertEqual(len(response.context["classes"]), 3)
        self.assertEqual(len(response.context["children"]), 3)
        print("Test register page finished. ✔")
    
