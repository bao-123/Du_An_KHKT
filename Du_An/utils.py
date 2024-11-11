from .models import *
from datetime import date
from django.core.files import File
from typing import Iterable
import pandas as pd
import os
from .exceptions import *
#import pandas as pd

#*Contants
COL_NAME: list[str] = ["STT", "Họ và tên", "Mã học sinh", "TX1", "TX2", "TX3", "TX4", "ĐĐGgk", "ĐĐGck", """ĐTB 
mhk""", "Nhận xét" ] #? ĐTBmhk có dấu cách ??? 
#-i columns that have to store some data
REQUIRED_COL: list[str] = ["STT", "Họ và tên"]


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

    @classmethod
    def check_class_dataframe(cls, df: pd.DataFrame, stundent_count) -> None:
        """
        Validates the structure and content of a DataFrame representing class data.

        Parameters:
        - df (pd.DataFrame): The DataFrame containing class data to be validated.
        - stundent_count (int): The expected number of students (rows) in the DataFrame.

        Raises:
        - InvalidColumn: If any column in the DataFrame is not recognized.
        - MissingIndex: If the number of rows in the DataFrame does not match the expected student count.
        - DfNotClean: If any row in the DataFrame is completely empty.
        - MissingInfo: If any required column contains missing information in any row.

        Returns:
        - None
        """

        for column in df.columns:
            if column not in COL_NAME:
                raise InvalidColumn(f"{column} is not valid!")
        if df.index.size != stundent_count:
            raise MissingIndex(f"The index is not correct")

        for index in df.index:
            row = df.iloc[index]

            if not row.any():
                raise DfNotClean(f"{index} is empty!")

            for col in REQUIRED_COL:
                if pd.isna(row[col]):
                    raise MissingInfo(f"Missing info in {col}")

            
        
            
            

    @staticmethod
    def read_excel_file(file: File, student_count: int = 0) -> dict:
        """
        This function reads an excel file and processes it to extract student information.

        Parameters:
        - file (File): The excel file to be read.
        - student_count (int, optional): The expected number of students in the file. Default is 0.

        Returns:
        - dict: A dictionary containing student information. Each key is a student's full name, and the value is another dictionary containing the student's marks and other relevant information.

        Raises:
        - Exception: If the file is not an excel file.
        - IndexError: If the student count, class, or the information in the file does not match.
        """

        if not file.name.endswith('.xlsx') and not file.name.endswith('.xls'):
            raise Exception("Only read excel files")
        dataf = pd.read_excel(file)
        #*Clean the dataf and only return useful data

        #*Rename columns
        for column in dataf.columns:
            column_renamed = False

            #* Don't remove the column if it is next to the "Họ và tên" column
            previous_column = dataf.columns.get_indexer([column])[0] - 1 
            try:
                if dataf.columns[previous_column] == "Họ và tên":
                    column_renamed = True
            except IndexError:
                continue

            for row in dataf.index:

                for name in COL_NAME:
                    if name.lower() == str(dataf[column][row]).lower():
                        dataf.rename(columns={column: name}, inplace=True)
                        column_renamed = True
                        break

                if column_renamed:
                    break

            if not column_renamed:
                dataf.pop(column)

        #* Rename the column next to the "Họ và tên" column
        name_column = dataf.columns.get_indexer(["Họ và tên"])[0] + 1
        dataf.rename(columns={dataf.columns[name_column]: "tên"}, inplace=True)

        empty_rows = []
        for row in dataf.index:
            if not dataf.iloc[row].any():
                empty_rows.append(row)

        #*Drop empty lines and useless lines
        dataf.drop(empty_rows, inplace=True)

        dataf.reset_index(drop=True, inplace=True)

        dataf.drop(range(0,5), inplace=True)
        #*Remove some useless lines at the end of the dataframe

        dataf.reset_index(drop=True, inplace=True)

        #! This can raise IndexError if student count or class or the info in the file is not match with others.
        dataf.drop(range(student_count, dataf.index.size), inplace=True)
        dataf.reset_index(drop=True, inplace=True)

        #* Merge the 'Họ và tên' column which contains only the surname and the middle name with the 'tên column
        for row in dataf.index:
            dataf.at[row, "Họ và tên"] = f"{dataf.at[row, "Họ và tên"]} {dataf.at[row, "tên"]}"

        dataf.pop("tên")
        #!Can raise some exceptions
        ViewUtils.check_class_dataframe(dataf, student_count)

        result_dict = {}
        #*Convert dataframe to dict
        for index in dataf.index:
            result_dict[dataf["Họ và tên"][index]] = {}

            for col in dataf.columns:
                if col in ["Họ và tên", "Mã học sinh", "Nhận xét", "ĐTB \nmhk"]:
                    continue
                result_dict[dataf["Họ và tên"][index]][col] = dataf[col][index] if not pd.isna(dataf[col][index]) else None

        return result_dict


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
        
