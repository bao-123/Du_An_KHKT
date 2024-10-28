from openai import OpenAI
from .models import *

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
                    teacher comment: {subject["second_term"].comment}""" for subject in student_marks["comment"]])}

"""
    print(prompt)

#TODO: Debug this function and research read excel file function.


