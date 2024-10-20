/* Tài liệu ở đây

    SKIBIDI
    
    ! danger
    ? ???
    ** alo alo
    TODO: TODO ae
    -I Importain notes
    -W Warning notes
*/

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


