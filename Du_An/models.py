from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#**CONSTANTs
#* students's roles
STUDENT_ROLE: list[str] = ["monitor", "academic", "art", "labor"]
#-W The names here must be correct with the names of 'Subject' instances
MAIN_SUBJECTS: list[str] = ["Toán", "Tiếng Anh", "Ngữ Văn", "Lịch Sử & Địa Lí", "KHTN"]
SECOND_SUBJECTS: list[str] = ["Tin Học", "GDCD", "Công Nghệ"]
COMMENT_SUBJECTS: list[str] = ["GDĐP", "HĐTN-HN", "Mĩ Thuật", "Âm Nhạc"]


#**name of instances of this models must be not different from the name of subjects in MainSubject, SecondSubject and EveluateByCommentSubject
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
    contact_information = models.TextField(default='')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "email": self.email,
        }

#** ensure that a MainSubject (or SecondSubject,...) object only point to a student
class MainSubject(models.Model):
    name = models.CharField(max_length=20) #! Shouldn't set 'blank' to True in a CharField
    # -1.0 mean teacher doesn't submit the mark of that student yet.
    diem_thuong_xuyen1 = models.FloatField(null=True, blank=True, default=None)
    diem_thuong_xuyen2 = models.FloatField(null=True, blank=True, default=None)
    diem_thuong_xuyen3 = models.FloatField(null=True, blank=True, default=None)
    diem_thuong_xuyen4 = models.FloatField(null=True, blank=True, default=None)
    diem_giua_ki = models.FloatField(null=True, blank=True, default=None)
    diem_cuoi_ki = models.FloatField(null=True, blank=True, default=None)
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
  
  
    @staticmethod
    def generate_main_subjects():
        return [ MainSubject.objects.create(name=subject_name) for subject_name in MAIN_SUBJECTS]



#** Have 2 diem thuong xuyen/1 ki (35 tiet tren 1 nam)
class SecondSubject(models.Model):
    name = models.CharField(max_length=20)
    diem_thuong_xuyen1 = models.FloatField(null=True, blank=True, default=None)
    diem_thuong_xuyen2 = models.FloatField(null=True, blank=True, default=None)
    diem_giua_ki = models.FloatField(null=True, blank=True, default=None)
    diem_cuoi_ki = models.FloatField(null=True, blank=True, default=None)
    comment = models.TextField(blank=True)

    @staticmethod
    def generate_second_subjects():
        #* mon co 2 diem thuong xuyen 1 hoc ki
        return [SecondSubject.objects.create(name=subject) for subject in SECOND_SUBJECTS]


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
    is_passed = models.BooleanField(null=True, blank=True, default=None) #* Dat hay chua dat
    comment = models.TextField()


    @staticmethod
    def generate_comment_subject():
        return [EvaluateByCommentSubject.objects.create(name=subject) for subject in COMMENT_SUBJECTS]

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
    #TODO: fix
    main_subjects = models.ManyToManyField(MainSubject, related_name="student")
    second_subjects = models.ManyToManyField(SecondSubject, related_name="student")
    comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="student")
    second_term_main_subjects = models.ManyToManyField(MainSubject, related_name="second_term_student")
    second_term_second_subjects = models.ManyToManyField(SecondSubject, related_name="second_term_student")
    second_term_comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="second_term_student")

    role = models.CharField(max_length=30, choices=role_choices)

    def __str__(self):
        return f"{self.id}| {self.full_name}| {self.classroom.name} | {self.role}"


    #*get marks of subjects
    def get_subjects_mark(self):
        return {
            "main": [
                {"first_term": self.main_subjects.filter(name="Toán").first(), "second_term": self.second_term_main_subjects.filter(name="Toán").first()},
                {"first_term": self.main_subjects.filter(name="Ngữ Văn").first(), "second_term": self.second_term_main_subjects.filter(name="Ngữ Văn").first()},
                {"first_term": self.main_subjects.filter(name="Tiếng Anh").first(), "second_term": self.second_term_main_subjects.filter(name="Tiếng Anh").first()},
                {"first_term": self.main_subjects.filter(name="KHTN").first(), "second_term": self.second_term_main_subjects.filter(name="KHTN").first()},
                {"first_term": self.main_subjects.filter(name="Lịch Sử & Địa Lí").first(), "second_term": self.second_term_main_subjects.filter(name="Lịch Sử & Địa Lí").first()},
            ],
            "second": [
                {"first_term": self.second_subjects.filter(name="Tin Học").first(), "second_term": self.second_term_second_subjects.filter(name="Tin Học").first()},
                {"first_term": self.second_subjects.filter(name="Công Nghệ").first(), "second_term": self.second_term_second_subjects.filter(name="Công Nghệ").first()},
                {"first_term": self.second_subjects.filter(name="GDCD").first(), "second_term": self.second_term_second_subjects.filter(name="GDCD").first()}
            ],
            "comment": [
                {"first_term": self.comment_subjects.filter(name="GDĐP").first(), "second_term": self.second_term_comment_subjects.filter(name="GDĐP").first()},
                {"first_term": self.comment_subjects.filter(name="HĐTN-HN").first(), "second_term": self.second_term_comment_subjects.filter(name="HĐTN-HN").first()},
                {"first_term": self.comment_subjects.filter(name="GDTC").first(), "second_term": self.second_term_comment_subjects.filter(name="GDTC").first()},
                {"first_term": self.comment_subjects.filter(name="Mĩ Thuật").first(), "second_term": self.second_term_comment_subjects.filter(name="Mĩ Thuật").first()},
                {"first_term": self.comment_subjects.filter(name="Âm Nhạc").first(), "second_term": self.second_term_comment_subjects.filter(name="Âm Nhạc").first()}
            ]
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
    
    def get_class_staff_committee(self):
        return self.students.filter(role__in=STUDENT_ROLE)

    def get_student_by_role(self, role: str) -> Student | None:
        try:
            return self.students.get(role=role)
        except Student.DoesNotExist:
            return None
    

    def __str__(self):
        return self.name
    

    def serialize(self):
        monitor = self.get_student_by_role(role="monitor")
        return {
            "id": self.id,
            "name": self.name,
            "form_teacher": self.form_teacher.serialize() if self.form_teacher else None,
            "subject_teachers": [ teacher.serialize() for teacher in self.subject_teachers.all() ],
            "monitor": monitor if monitor else None
        }
    
    def get_students(self):
        return [ student.serialize() for student in self.students.all() ]
    
    def get_teachers(self):
        return [ teacher.teacher for teacher in self.subject_teachers.all() ]


class ClassSubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="classes")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="teaching_classes")

    @staticmethod
    def get_subject_teacher(subject: Subject, classroom: Class) -> Teacher | None:
        try:
            return ClassSubjectTeacher.objects.get(subject=subject, classroom=classroom)
        except ClassSubjectTeacher.DoesNotExist:
            return None
    
    @staticmethod
    def is_teaching(subject: Subject, teacher: Teacher, classroom: Class) -> bool:
        class_subject = ClassSubjectTeacher.objects.filter(subject=subject, classroom=classroom).first()
        if not class_subject:
            raise Exception("Unknow class (or subject)")
        
        return class_subject.teacher == teacher


#function to create a Subject
def create_main_subject(name: str):
    subject = MainSubject.objects.create(name=name)

    return subject
