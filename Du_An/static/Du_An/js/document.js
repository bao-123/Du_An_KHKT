/* Tài liệu ở đây
    
    ! danger
    ? ???
    * alo alo
    TODO: TODO ae
    -I Importain notes
    -W Warning notes

*/

//-i Cần đồng bộ hóa với back-end
export const mainSubjects = ["Toán", "Tiếng Anh", "Ngữ Văn", "Lịch Sử & Địa Lí", "KHTN"];
export const secondSubjects = ["Tin Học", "GDCD", "Công Nghệ"];
export const commentSubjects = ["GDĐP", "GDTC", "HĐTN-HN", "Mĩ Thuật", "Âm Nhạc"];


const baseURL = "http://127.0.0.1:8000/"

// -I Gửi PUT request đến đây để cập nhập điểm của học sinh
export const updateMarkURL = baseURL + "student/" // -W Thêm id của học sinh vào phía sau */

// -I Gửi PUT request đến đây để thêm giáo viên vào danh sách giáo viên bộ môn của lớp
export const addClassSubjectTeacherURL = baseURL + "classes" //-W Don't need '/'

//-i Gửi GET request đến đây để lấy điểm của 1 môn học nào đó của học sinh.
export const getStudentMarksURL = baseURL + "student/marks/"; //-w add student id
/*
    *parameters
    @@year if not provide will be this year
    @@subject_id is the id of the subject
*/


//-i Gửi GET request đến đây để search học sinh theo tên (và lớp nếu có )
export const searchStudentURL = baseURL + "search_student";
/*
    -I API parameters
    @@name for the name of the student (query)
    @@classroom_id if not choosen just don't send (result will be students from all the classes)
     
    -i If there are not any error occur, API will return a object with porperty 'search_result' is a Array.
    -i If there are errors occur (e.g classroom's id is not valid), API will return a object will 'message' porperty contains error message
*/


// -i  Gửi PUT request đến đây để thay đổi info của user (info ko quan trọng và ko phải khóa ngoại)
export const changeInfoURL = baseURL + "change_info"; 
/*
    -I API parameters
    @@request.body: 
        @@property is the porperty that needs to change
        @@value: new value
    
    -i return status 200 if sucessful, otherwise return status 400
*/

//-i Gửi PUT request đến đây để đổi mật khẩu của user
export const changePasswordURL = baseURL + "change_password"; 


//-i Gửi POST request đến đây để thêm hồ sơ năm học mới cho học sinh
export const newStudentYearProfileURL = baseURL + "new_profile/"; //-w Thêm id của học sinh ở phía sau và ko cần '/'

/*
    *parameters
    @@classroom_id is the id of the classroom
    @@year for the year of the new profile
    @@role is the role of the student in the classroom (e.g. monitor, student) default is student
*/

