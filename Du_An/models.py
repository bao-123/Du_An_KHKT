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

    
class Student(models.Model):
    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=False)
    is_boy = models.BooleanField()
    main_subjects = models.ManyToManyField("MainSubject", related_name="student")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "birthday": self.birthday.strftime("%d/%m/%Y"),
            "is_boy": self.is_boy,
            "classroom": self.classroom.first().serialize(),
            "math": [ subject.serialize() for subject in self.main_subjects.all() ]
        }


class Class(models.Model):
    form_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, default=None, related_name="form_class")
    name = models.CharField(max_length=3, unique=True)
    students = models.ManyToManyField(Student, blank=True, related_name="classroom")
    subject_teachers = models.ManyToManyField("ClassSubjectTeacher", related_name="classroom")

    def student_count(self) -> int:
        return self.students.count()

    
    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "form_teacher": self.form_teacher.serialize() if self.form_teacher else None,
            "subject_teachers": [ teacher.serialize() for teacher in self.subject_teachers.all() ]
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


