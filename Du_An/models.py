from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.


class Subject(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __str__(self):
        return self.name
    
    def get_teachers(self) -> list:
        return [teacher.serialize for teacher in self.teachers.all()]
    
    def teacher_count(self):
        return self.teachers.count()
    

class Teacher(User):
    #** use full_name instead because username is unique
    #** username field stored user's email (unique)
    full_name = models.CharField(max_length=200, unique=False)
    subject = models.ManyToManyField(Subject, related_name="teachers")
    contact_information = models.TextField(default="")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "email": self.email,
            #"is_boy": self.is_boy
        }
    

class Parent(User):
    #** use full_name instead because username is unique
    #** username field stored user's email (unique)
    full_name = models.CharField(max_length=200, unique=False)
    children = models.ManyToManyField("Student", related_name="parent")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "email": self.email,
        }


class MainSubject(models.Model):
    name = models.CharField(max_length=20)
    # -1.0 mean teacher doesn't submit the mark of that student yet.
    diem_thuong_xuyen1 = models.FloatField(null=True, default=None)
    diem_thuong_xuyen2 = models.FloatField(null=True, default=None)
    diem_thuong_xuyen3 = models.FloatField(null=True, default=None)
    diem_thuong_xuyen4 = models.FloatField(null=True, default=None)
    diem_giua_ki = models.FloatField(null=True, default=None)
    diem_cuoi_ki = models.FloatField(null=True, default=None)
    comment = models.TextField()

    def serialize(self):
        return {
            "thuong_xuyen1": self.diem_thuong_xuyen1,
            "thuong_xuyen2": self.diem_thuong_xuyen2,
            "thuong_xuyen3": self.diem_thuong_xuyen3,
            "thuong_xuyen4": self.diem_thuong_xuyen4,
            "giua_ki": self.diem_giua_ki,
            "cuoi_ki": self.diem_cuoi_ki,
            "teacher_comment": self.comment
        }
    
    #TODO: Add more main subjects (if needed)
    @staticmethod
    def generate_main_subjects():
        return [
            MainSubject.objects.create(name="Toán"),
            MainSubject.objects.create(name="Ngữ Văn"),
            MainSubject.objects.create(name="Tiếng Anh"),
            MainSubject.objects.create(name="KHTN"),
            MainSubject.objects.create(name="Lịch sử & địa lí")
        ]



#** Have 2 diem thuong xuyen/1 ki (35 tiet tren 1 nam)
class SecondSubject(models.Model):
    diem_thuong_xuyen1 = models.FloatField(null=True, default=None)
    diem_thuong_xuyen2 = models.FloatField(null=True, default=None)
    diem_giua_ki = models.FloatField(null=True, default=None)
    diem_cuoi_ki = models.FloatField(null=True, default=None)
    comment = models.TextField()


    @staticmethod
    def generate_second_subjects():
        #* mon co 2 diem thuong xuyen 1 hoc ki
        return [
            SecondSubject.objects.create(name="Công nghệ"),
            SecondSubject.objects.create(name="GDCD"),
            SecondSubject.objects.create(name="Tin học"),
        ]


    def serialize(self):
        return {
            "thuong_xuyen1": self.diem_thuong_xuyen1,
            "thuong_xuyen2": self.diem_thuong_xuyen2,
            "giua_ki": self.diem_giua_ki,
            "cuoi_ki": self.diem_cuoi_ki,
            "teacher_comment": self.comment
        }


#* mon hoc danh gia bang nhan xet (dat/ko dat)
class EvaluateByCommentSubject(models.Model):
    name = models.CharField(max_length=20)
    is_passed = models.BooleanField(null=True, default=None) #* Dat hay chua dat
    comment = models.TextField()


    @staticmethod
    def generate_comment_subject():
        return [
            EvaluateByCommentSubject.objects.create(name="GDTC"),
            EvaluateByCommentSubject.objects.create(name="GDĐP"),
            EvaluateByCommentSubject.objects.create(name="HĐTN-HN"),
            EvaluateByCommentSubject.objects.create(name="Mĩ Thuật"),
            EvaluateByCommentSubject.objects.create(name="Âm nhạc")
        ]

    def __str__(self):
        return f"id: {self.id}|{self.name} of {self.student}"
    

    def serialize(self):
        return {
            "is_passed": self.is_passed,
            "teacher_comment": self.comment
        }


class Student(models.Model):
    role_choices = [
        ("monitor", "Lớp trưởng"),
        ("academic", "lớp phó học tập"),
        ("art", "lớp phó văn thể mỹ"),
        ("labor", "lớp phó lao động"),
        ("student", "Học sinh")
    ]

    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=False)
    is_boy = models.BooleanField()
    classroom = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="students")
    main_subjects = models.ManyToManyField(MainSubject, default=MainSubject.generate_main_subjects, related_name="student")
    second_subjects = models.ManyToManyField(SecondSubject, default=SecondSubject.generate_second_subjects, related_name="student")
    comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, default=EvaluateByCommentSubject.generate_comment_subject, related_name="students")
    role = models.CharField(max_length=30, choices=role_choices)

    #get marks of subjects
    def get_subjects_mark(self):
        return {
            "math": self.main_subjects.filter(name="Toán").first(),
            "literature": self.main_subjects.filter(name="Ngữ Văn").first(),
            "English": self.main_subjects.filter(name="Tiếng Anh").first(),
            "KHTN": self.main_subjects.filter(name="KHTN").first(),
            "H&G": self.main_subjects.filter(name="Lịch sử & Địa Lí").first(),
            "Technology": self.main_subjects.filter(name="Công nghệ").first(),
            "IT": self.main_subjects.filter(name="Tin Học").first(),
            "GDCD": self.main_subjects.filter(name="GDCD").first(),
            "GDDP": self.main_subjects.filter(name="GDĐP").first(),
            "HDTN-HN": self.main_subjects.filter(name="HĐTN-HN").first(),
            "GDTC": self.main_subjects.filter(name="GDTC").first(),
            "Art": self.main_subjects.filter(name="Mĩ Thuật").first(),
            "Music": self.main_subjects.filter(name="Âm Nhạc").first()
        }
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "birthday": self.birthday.strftime("%d/%m/%Y"),
            "is_boy": self.is_boy,
            "classroom": self.classroom.serialize(),
            "math": [ subject.serialize() for subject in self.main_subjects.all() ]
        }


class Class(models.Model):
    form_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, default=None, related_name="form_class")
    name = models.CharField(max_length=3, unique=True)
    subject_teachers = models.ManyToManyField("ClassSubjectTeacher", related_name="classroom")

    def student_count(self) -> int:
        return self.students.count()
    
    def get_monitor(self) -> Student | None:
        return self.students.filter(role="monitor").first()
    

    def get_student_by_role(self, role: str) -> Student | None:
        return self.students.filter(role=role).first()
    

    def __str__(self):
        return self.name
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "form_teacher": self.form_teacher.serialize() if self.form_teacher else None,
            "subject_teachers": [ teacher.serialize() for teacher in self.subject_teachers.all() ],
            "monitor": self.get_monitor().serialize() if self.get_monitor() else None
        }
    
    def get_students(self):
        return [ student.serialize() for student in self.students.all() ]


class ClassSubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="classes")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="teaching_classes")

    @staticmethod
    def get_subject_teacher(subject: Subject, classroom: Class) -> Teacher | None:
        class_subject = ClassSubjectTeacher.objects.filter(classroom=classroom, subject=subject)

        return class_subject.teacher if class_subject else None
    
    @staticmethod
    def is_teaching(subject: Subject, teacher: Teacher, classroom: Class) -> bool:
        class_subject = ClassSubjectTeacher.objects.filter(subject=subject, classroom=classroom)
        if not class_subject:
            raise Exception("Unknow class (or subject) ")
        
        return class_subject.teacher == teacher


#function to create a Subject
def create_main_subject(name: str):
    subject = MainSubject.objects.create(name=name)

    return subject


#function to get a student
def get_student(id: int) -> Student | None:
    try:
        return Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return None

