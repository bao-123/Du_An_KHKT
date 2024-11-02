from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

#-I CONSTANTs
#* students's roles
STUDENT_ROLE: list[str] = ["monitor", "academic", "art", "labor", "student"]
role_choices = [
        ("monitor", "Lớp trưởng"),
        ("academic", "lớp phó học tập"),
        ("art", "lớp phó văn thể mỹ"),
        ("labor", "lớp phó lao động"),
        ("student", "Học sinh")
    ]

#-W The names here must be correct with the names of 'Subject' instances
MAIN_SUBJECTS: list[str] = ["Toán", "Tiếng Anh", "Ngữ Văn", "Lịch Sử & Địa Lí", "KHTN"]
SECOND_SUBJECTS: list[str] = ["Tin Học", "GDCD", "Công Nghệ"]
COMMENT_SUBJECTS: list[str] = ["GDĐP", "GDTC", "HĐTN-HN", "Mĩ Thuật", "Âm Nhạc"]
this_year: int = date.today().year


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
        return [teacher.serialize() for teacher in self.teachers.all()]
    

class Teacher(User):
    #** use full_name instead because username is unique
    #** username field stored user's email (unique)
    full_name = models.CharField(max_length=200, unique=False)
    subject = models.ManyToManyField(Subject, related_name="teachers")
    contact_information = models.TextField(default="")


    def get_teaching_classes(self):
        teaching_classes = [ subject_class.classroom.classroom for subject_class in self.teaching_classes.all() ]
        teaching_classes = set(teaching_classes) #*Remove duplicates
        return [{"classroom": classroom, "profile": classroom.get_profile()} for classroom in teaching_classes]
    
            
            

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "email": self.email,
            "contact_info": self.contact_information
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
            "contact_info": self.contact_information
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

    full_name = models.CharField(max_length=200)
    birthday = models.DateField(blank=False)
    is_boy = models.BooleanField()
    #TODO: fix
    #* Replaced!
    """ 
    //main_subjects = models.ManyToManyField(MainSubject, related_name="student")
    //second_subjects = models.ManyToManyField(SecondSubject, related_name="student")
    //comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="student")
    //second_term_main_subjects = models.ManyToManyField(MainSubject, related_name="second_term_student")
    //second_term_second_subjects = models.ManyToManyField(SecondSubject, related_name="second_term_student")
    //second_term_comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="second_term_student") 
    """
    #! Using porperty 'profiles' insteads.

    def __str__(self):
        profile = self.get_profile()
        return f"{self.id}| {self.full_name}| {profile.get_classroom().name} | {profile.role}"

    #* Get the profile of this year
    def get_profile(self, year: int = this_year):
        try:
            return self.profiles.get(year=year)
        except StudentYearProfile.DoesNotExist:
            return None
    
    def get_years(self):
        return [{"year": f"{profile.year}-{profile.year+1}" , "id": profile.id} for profile in self.profiles.all()]

    #*get marks of subjects
    def get_subjects_mark(self, year: int = this_year, serialize: bool=False):
        profile = self.get_profile(year=year)
        if not profile:
            return None
        
        def get_subject_mark(name, subjects, serialize: bool = serialize): #* serialize in the outer function
            subject = subjects.filter(name=name).first()
            return subject.serialize() if serialize and subject else subject #-i return None if 'subject' is None

        return {
            "main": [
                {"first_term": get_subject_mark(name, profile.main_subjects),
                  "second_term": get_subject_mark(name, profile.second_term_main_subjects)}
                for name in MAIN_SUBJECTS
            ],
            "second": [
                {"first_term": get_subject_mark(name, profile.second_subjects),
                  "second_term": get_subject_mark(name, profile.second_term_second_subjects)}
                for name in SECOND_SUBJECTS
            ],
            #TODO:
            "comment": [
                {"first_term": get_subject_mark(name, profile.comment_subjects),
                 "second_term": get_subject_mark(name, profile.second_term_comment_subjects) }
                for name in COMMENT_SUBJECTS
            ]
        }
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "birthday": self.birthday.strftime("%d/%m/%Y"),
            #"profiles": [ profile.serialize() for profile in self.profiles.all() ]
        }
    


#-I Implement to store student data (mark) by years (năm học)
class StudentYearProfile(models.Model):


    year = models.PositiveSmallIntegerField(blank=False, default=this_year)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="profiles") #-W profile with 's'
    classroom = models.ForeignKey("ClassYearProfile", on_delete=models.CASCADE, related_name="students")
    role = models.CharField(max_length=30, choices=role_choices)
    main_subjects = models.ManyToManyField(MainSubject, related_name="student")
    second_subjects = models.ManyToManyField(SecondSubject, related_name="student")
    comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="student")
    second_term_main_subjects = models.ManyToManyField(MainSubject, related_name="second_term_student")
    second_term_second_subjects = models.ManyToManyField(SecondSubject, related_name="second_term_student")
    second_term_comment_subjects = models.ManyToManyField(EvaluateByCommentSubject, related_name="second_term_student")

    def serialize(self):
        return {
            "id": self.id,
            "year": self.year,
            "classroom": self.classroom.serialize(),
            "role": self.role,
        }
    

    def get_classroom(self, year: int = this_year):
        try:
            return self.classroom.classroom
        except:
            return None
        

    @staticmethod
    def create_profile(student: Student, role: str, classroom, year: int = this_year): #@@classroom should be a 'Class' instance
        profile = StudentYearProfile(
            student=student,
            year=year,
            classroom=classroom.profiles.get(year=year), #-I The year of the profile must be equal to the year of the classroom's profile
            role=role,
        )

        profile.full_clean() #! Can raise ValidationError if data is invalid
        profile.save()

        profile.main_subjects.set(MainSubject.generate_main_subjects())
        profile.second_term_main_subjects.set(MainSubject.generate_main_subjects())
        profile.second_subjects.set(SecondSubject.generate_second_subjects())
        profile.second_term_second_subjects.set(SecondSubject.generate_second_subjects())
        profile.comment_subjects.set(EvaluateByCommentSubject.generate_comment_subject())
        profile.second_term_comment_subjects.set(EvaluateByCommentSubject.generate_comment_subject())

        profile.save(force_update=True) #* Ensure

        return profile


class Class(models.Model):
    name = models.CharField(max_length=3, unique=True)
    

    def __str__(self):
        return self.name
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "profiles": [ profile.serialize() for profile in self.profiles.all() ]
        }
    

    #* get the profile of this year
    def get_profile(self, year: int =this_year):
        try:
            return self.profiles.get(year=year)
        except ClassYearProfile.DoesNotExist:
            return None
        
        
    def get_students(self, year: int = this_year):
        return [ student_profile.student.serialize() for student_profile in self.profiles.get(year=year).students.all() ] #* self.students is 'StudentYearProfile'



#TODO: Finish
#-I Store class's data by years
class ClassYearProfile(models.Model):
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="profiles") #-W profile with 's'
    year = models.PositiveSmallIntegerField(blank=False, default=date.today().year)
    form_teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="form_class")


    def __str__(self):
        return f"{self.id}| {self.classroom.name}| {self.year}"

    def get_class_staff_committee(self):
        try:
            return self.students.exclude(role="student").all()
        except:
            return None
    

    def get_teachers(self):
        return set([subject_teacher.teacher for subject_teacher in self.subject_teachers.all() ]) #*Remove duplicates
    

    def get_student_by_role(self, role: str) -> StudentYearProfile | None:
        try:
            return self.students.get(role=role) #-W self.students is a ManyToManyRelatedManager (to StudentYearProfile)
        except StudentYearProfile.DoesNotExist:
            return None
        

    def serialize(self):
        return {
            "id": self.id,
            "year": self.year,
            "form_teacher": self.form_teacher.serialize() if self.form_teacher else None,
            "subject_teachers": [ teacher.teacher.serialize() for teacher in self.subject_teachers.all() ]
        }


class ClassSubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="classes")
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="teaching_classes")
    classroom = models.ForeignKey(ClassYearProfile, on_delete=models.CASCADE, related_name="subject_teachers")

    @staticmethod
    def get_subject_teacher(subject: Subject, classProfile: ClassYearProfile) -> Teacher | None:
        try:
            return ClassSubjectTeacher.objects.get(subject=subject, classroom=classProfile).teacher
        except ClassSubjectTeacher.DoesNotExist:
            return None
    
    @staticmethod
    def is_teaching(subject: Subject, teacher: Teacher, classroom: ClassYearProfile) -> bool:
        class_subject = ClassSubjectTeacher.objects.filter(subject=subject, classroom=classroom).first()
        if not class_subject:
            raise Exception("Unknow class (or subject)")
        
        return class_subject.teacher == teacher
