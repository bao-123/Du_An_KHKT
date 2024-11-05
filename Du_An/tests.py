from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .utils import TestUtils
from .utils import ViewUtils
from .models import *
from datetime import date

def printGreen(text):
    print(f"\033[92m {text}")

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
        
        self.teacher_count = 3


        self.classroom1 = TestUtils.create_classroom("6a1", form_teacher=self.teacher1, subject_teachers=[self.teacher2,])
        self.classroom2 = TestUtils.create_classroom("6a2", form_teacher=self.teacher3, subject_teachers=[self.teacher1, self.teacher3])
        self.classroom3 = TestUtils.create_classroom("6a3", subject_teachers=[self.teacher2, ]) #* This class don't have a form teacher
        self.classroom4 = TestUtils.create_classroom("5a1", subject_teachers=[self.teacher3, ])

        self.classroom_count = 4
        #* For testing create student's profile API
        self.profile4 = ViewUtils.create_class_profile(classroom=self.classroom4["classroom"], year=2023) #*this profile didn't have a form_teacher
        
        #* create some students to test register page
        self.student1 = TestUtils.create_student(name="Nguyen Thien Bao", role="monitor",
                                                  is_boy=True, classroom=self.classroom1["classroom"],
                                                  birthday=date.today())
        self.student2 = TestUtils.create_student(name="Tran Hoang Loc", role="art",
                                                  is_boy=True, classroom=self.classroom1["classroom"],
                                                  birthday=date.today())
        self.student3 = TestUtils.create_student(name="Vo Trong Tin", is_boy=False,
                                                  role="monitor", classroom=self.classroom2["classroom"],
                                                  birthday=date.today())
        
        #* Create some parents
        self.parent1 = TestUtils.create_user(type="parent", email="parent1@parent.com",
                                             password="parent1", full_name="Nguyễn Văn C",
                                             children=[self.student1["student"], self.student2["student"]],
                                             contact_info="abc")
        
        self.parent2 = TestUtils.create_user(type="parent", email="parent2@parent.com",
                                             password="parent2", full_name="Nguyễn Văn D", 
                                             children=[self.student3["student"], ],
                                             contact_info="xyz")
    
    @classmethod
    def tearDownClass(self):
        print("Cleaning...")
        super().tearDownClass()
        

    def test_welcome_page(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        print("Test welcome page finished. ✔")

    def test_view_login(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        print("test login view finished. ✔")

    #! email of a teacher or a parent is stored in 'username' field
    def test_login_teacher(self):
        #* Shouldn't use self.client.teacher2.password because it's hashed.
        response = self.client.post(reverse("login"), {"email": self.teacher2.username, "password": "teacher2", "role": "teacher"}) #* Try to log client to teacher2

        self.assertEqual(response.status_code, 302) #* User should be redirected
        self.assertIs(response.wsgi_request.user.__class__, Teacher) #* User should be log in as a teacher
        self.assertEqual(response.wsgi_request.user.teacher, self.teacher2)

        print("Test login functionalities for teachers! ✔")
        self.client.logout()

    def test_login_parent(self):
        response = self.client.post(reverse("login"), {"email": self.parent1.username, "password": "parent1", "role": "parent"})

        self.assertEqual(response.status_code, 302) #* Redirected
        self.assertIs(response.wsgi_request.user.__class__, Parent)
        self.assertEqual(response.wsgi_request.user.parent, self.parent1)

        print("Test login for parents finished! ✔")
        self.client.logout()

    def test_logout(self):
        self.client.login(username=self.teacher1.username)

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 302) #* User should be redirected.
        self.assertIs(response.wsgi_request.user.__class__, AnonymousUser)
        print("test login finished. ✔")

    def test_view_register(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["subjects"]), 3)
        self.assertEqual(len(response.context["classes"]), 4)
        self.assertEqual(len(response.context["children"]), 3)
        print("Test register page finished. ✔")

    def test_register_teacher(self):
        response = self.client.post(reverse("register"), {"full_name": "testUser", "email": "test@test.com",
                                                           "password": "test", "contact_info": "mnp",
                                                           "user_type": "teacher", "subjects[]": [ self.subjects[0].id, self.subjects[1].id ],
                                                           "form_class": self.classroom3["classroom"].id }) #* Only 6a3 don't have a form teacher yet
        
        self.assertEqual(response.status_code, 302) #*User should be redirected
        self.assertIs(response.wsgi_request.user.__class__, Teacher)
        test_user = Teacher.objects.get(username="test@test.com") #* Ensure that the new user is created
        self.assertEqual(response.wsgi_request.user, test_user)
        self.assertEqual(test_user.full_name, "testUser")
        self.assertTrue(test_user.check_password("test"))
        self.assertEqual(test_user.contact_information, "mnp")
        self.assertQuerySetEqual(test_user.subject.all(), Subject.objects.filter(pk__in=[self.subjects[0].id, self.subjects[1].id]), ordered=False)
        self.assertEqual(test_user.form_class, self.classroom3["profile"])

        print("Test register for teachers finished!. ✔")

        self.client.logout()

    
    def test_dashboard(self):
        #*Test with teacher
        self.client.login(username=self.teacher1.username)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.client.logout()

        self.client.login(username=self.parent1.username)

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)

        print("test dashboard finished.✔")
        self.client.logout()



    def test_create_profile(self):
        self.client.force_login(self.teacher1)

        response = self.client.post(reverse("create_profile", args=(self.student1["student"].id, )), {"year": 2023,
                                                                                     "classroom_name": self.classroom4["classroom"].name,
                                                                                     "role": "monitor"})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(StudentYearProfile.objects.get(student=self.student1["student"], year=2023))
        self.assertEqual(data["profile"]["classroom"]["id"], self.classroom4["classroom"].get_profile(year=2023).id)

        printGreen("test create student profile finished. ✔")
        
    
    def test_student_page(self):
        self.client.force_login(self.teacher1)

        with self.subTest("View student 1"):
            response = self.client.get(reverse("view_student", args=(self.student1["student"].id, )))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["student"], self.student1["student"])
            self.assertEqual(response.context["student_profile"], self.student1["profile"])
            self.assertEqual(response.context["subjects"].count(), len(self.subjects))
            self.assertEqual(response.context["classes"].count(), self.classroom_count)
        
        with self.subTest("View student 2"):
            response = self.client.get(reverse("view_student", args=(self.student2["student"].id, )))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["student"], self.student2["student"])
            self.assertEqual(response.context["student_profile"], self.student2["profile"])
            self.assertEqual(response.context["subjects"].count(), len(self.subjects))
            self.assertEqual(response.context["classes"].count(), self.classroom_count)
        
        print("Test student view page finished ✔")

        self.client.logout()
            

    def test_teacher_page(self):
        self.client.force_login(self.parent1)

        with self.subTest("View teacher 1"):
            response = self.client.get(reverse("view_teacher", args=(self.teacher1.id, )))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["teacher"], self.teacher1)
        
        with self.subTest("View teacher 2"):
            response = self.client.get(reverse("view_teacher", args=(self.teacher2.id, )))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["teacher"], self.teacher2)

        print("Test view teacher page finished.✔")
        self.client.logout()


    def test_teachers(self):
        response = self.client.get(reverse("view_teachers"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["teachers"].count(), self.teacher_count)

        print("Test view teachers finished.✔")

