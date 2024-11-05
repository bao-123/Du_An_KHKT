from .models import *
from datetime import date
from django.core.files import File
from typing import Iterable
import os
#import pandas as pd


#Utils functions for views
class ViewUtils():

    @staticmethod
    def get_form_class(teacher: Teacher):
        try:
            return teacher.form_class
        except Teacher.form_class.RelatedObjectDoesNotExist:
            return None
    
    def create_class_profile(classroom: Class, year, form_teacher: Teacher | None = None):
        try:
            class_profile = ClassYearProfile.objects.create(classroom=classroom, year=year, form_teacher=form_teacher)
        except:
            return None
        return class_profile
    
    """def read_excel_data(file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File {file_path} not found.")
            return pd.read_excel(file_path)
        except Exception as e:
            print(e)"""

    #-i ChatGPT API
    def get_advice(student: Student):
        student_marks = student.get_subjects_mark()
        prompt = f"""
        Please give some advice for this Vietnamese student, this is {"his" if student.is_boy else "her"} marks:
        main subjects:
            {"\n".join([f"""{subject["first_term"].name}:
                        first term:
                            {"\n".join([f"Regular mark {i}: {getattr(subject["first_term"], f"diem_thuong_xuyen{i}")}" for i in range(4)])}
                            Mid term mark: {subject["first_term"].diem_giua_ki}
                            Final mark: {subject["first_term"].diem_cuoi_ki}
                            teacher comment: {subject["first_term"].comment} 
                        second term:
                            {"\n".join([f"Regular mark {i}: {getattr(subject["second_term"], f"diem_thuong_xuyen{i}")}" for i in range(4)])}
                            Mid term mark: {subject["second_term"].diem_giua_ki}
                            Final mark: {subject["second_term"].diem_cuoi_ki}
                            teacher comment: {subject["second_term"].comment}""" for subject in student_marks["main"]])}

        second subjects:
            {"\n".join([f"""{subject["name"]}:
                        first term:
                                {"\n".join([f"Regular mark {i}: {getattr(subject["first_term"], f'diem_thuong_xuyen{i}')}" for i in range(2)])}
                                Mid term mark: {subject["first_term"].diem_giua_ki}
                                Final mark: {subject["first_term"].diem_cuoi_ki}
                                teacher comment: {subject["first_term"].comment}
                        second term: 
                                {"\n".join([f"Regular mark {i}: {getattr(subject["second_term"], f"diem_thuong_xuyen{i}")}" for i in range(2)])}
                                Mid term mark: {subject["second_term"].diem_giua_ki}
                                Final mark: {subject["second_term"].diem_cuoi_ki}
                                teacher comment: {subject["second_term"].comment}""" for subject in student_marks["second"]])}
        Evaluate by comment subjects:
            {"\n".join([f"""{subject["first_term"].name}:
                        first term: {"passed" if subject["first_term"].is_passed else "not passed"}
                        teacher comment: {subject["first_term"].comment}
                        second term: {"passed" if subject["second_term"].is_passed else "not passed"}
                        teacher comment: {subject["second_term"].comment}""" for subject in student_marks["comment"]])} """
        return prompt #*TODO: Tam thoi

    
        

#TODO:!
#** functions for testing purpose
class TestUtils():

    #! Only use these functions for testing purpose!
    @staticmethod
    def create_subjects(names: list[str]):
        subjects = []
        for name in names:
            subjects.append(Subject.objects.create(name=name))
        return subjects
    
    @staticmethod
    def create_classroom(name: str, form_teacher: Teacher | None = None, subject_teachers: Iterable[Teacher] = [], year: int = this_year ):
        classroom = Class.objects.create(name=name)
        profile = ClassYearProfile.objects.create(classroom=classroom, form_teacher=form_teacher, year=year)

        for teacher in subject_teachers:
            #*Subject of teachers should be different, this just for testing purpose!
            ClassSubjectTeacher.objects.create(subject=teacher.subject.first(), teacher=teacher, classroom=profile) 
        
        return {"classroom": classroom, "profile": profile}
    

    @staticmethod
    def create_student(name: str, classroom: Class,
                       role: str | None = None, is_boy: bool | None = None,
                       birthday: date | None = None
                       ) -> dict[Student, StudentYearProfile]:
        student = Student.objects.create(full_name=name, is_boy=is_boy, birthday=birthday)

        student_profile = StudentYearProfile.create_profile(student, role, classroom)

        return {"student": student, "profile": student_profile}


    @staticmethod
    def create_user(type: str | None = None, 
                    email: str | None = None, 
                    password: str | None = None, 
                    full_name: str | None = None,
                    children: list[Student] | None = None,
                    subjects: list[Subject] | None = None,
                    contact_info : str = ''
                    ) -> Parent | Teacher | None:
        try:
            if type == "teacher":
                teacher = Teacher.objects.create(username=email, full_name=full_name, contact_information=contact_info)
                teacher.set_password(password)
                if subjects:
                    teacher.subject.set(subjects)
                
                teacher.save(force_update=True)
                return teacher
            elif type == "parent":
                parent = Parent.objects.create(username=email, full_name=full_name, contact_information=contact_info)
                parent.set_password(password)
                if children:
                    parent.children.set(children)

                parent.save(force_update=True)

                return parent
            else:
                raise Exception("Unknow user type")
        except Exception as e:
            print(e)
            return None
        
        
"""
#TODO: Complete reading Excel file function
df = ViewUtils.read_excel_data(r"E:\BaoBao\vscodeProject\Du_An_KHKT\Du_An\Schedule.xlsx")

print(df.head(len(df.columns)))
for i in df.index:
    print(df.at[i, df.columns[2]]) """

