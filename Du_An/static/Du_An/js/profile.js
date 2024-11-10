import { displayMessage, getSubjectMarks, tag, updateMark, clear, configFormValidtion, createStudentYearProfile, createTable } from "./utils.js";
//* Page's constants
const displayMessageDivId = "updateMarkMessage";
const displayMarkMessageDivId = "displayMarkMessage";
const markDisplayDivId = "markDisplay";

//
const markHeaderClass = "markHeader";

document.addEventListener("DOMContentLoaded", () => {
    //*Configuring bootstrap form validation
    configFormValidtion();
    //* Constants
    const subjectsSelect = document.getElementById("subjects_select");
    const updateMarkForm = document.getElementById("updateMarkForm");
    const markDisplayDiv = document.getElementById(markDisplayDivId);
    const studentProfile = document.getElementById("studentProfile");
    const showFormBtn = document.getElementById("showFormBtn");
    const createStudentYearProfileForm = document.getElementById("createProfileForm");
    const yearSelect = document.getElementById("yearSelect");
    
    const studentId = Number(studentProfile.dataset.studentId);

    subjectsSelect.addEventListener("change", async () => {
        try {
            const subjectData = await getSubjectMarks(studentId, Number(subjectsSelect.value), Number(yearSelect.value)); //TODO: Add year has been selected in 'yearSelect'
            //*Display marks
            //* if this is true, the subject is a main subject
            clear(markDisplayDivId);
            const subjectName = tag("h2", subjectData.subject, ["subjectName"]); //@@subjectData.subject is the name of the subject.

            //*Display headers
            let tableHeader = [];
            let tableBody = []
            
            if(subjectData.first_term.thuong_xuyen4 !== undefined)
            {
                tableHeader = ["Điểm thường xuyên 1", "Điểm thường xuyên 2", "Điểm thường xuyên 3",
                    "Điểm thường xuyên 4",
                    "Giữa kì",
                    "Cuối kì"
                ];

                tableBody = [
                    [tag("td", "Kì I", 'termHeader', '', {colspan: 6})], //* '6' is the total number of all columns
                    [
                        tag("td", subjectData.first_term.thuong_xuyen1 ? subjectData.first_term.thuong_xuyen1 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.thuong_xuyen2 ? subjectData.first_term.thuong_xuyen2 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.thuong_xuyen3 ? subjectData.first_term.thuong_xuyen3 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.thuong_xuyen4 ? subjectData.first_term.thuong_xuyen4 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.giua_ki ? subjectData.first_term.giua_ki : "Chưa có điểm"),
                        tag("td", subjectData.first_term.cuoi_ki ? subjectData.first_term.cuoi_ki : "Chưa có điểm"),
                    ],
                    [tag("td", "Kì II", 'termHeader', '', {colspan: 6})], //* For second term
                    [
                        tag("td", subjectData.second_term.thuong_xuyen1 ? subjectData.second_term.thuong_xuyen1 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.thuong_xuyen2 ? subjectData.second_term.thuong_xuyen2 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.thuong_xuyen3 ? subjectData.second_term.thuong_xuyen3 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.thuong_xuyen4 ? subjectData.second_term.thuong_xuyen4 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.giua_ki ? subjectData.second_term.giua_ki : "Chưa có điểm"),
                        tag("td", subjectData.second_term.cuoi_ki ? subjectData.second_term.cuoi_ki : "Chưa có điểm"),
                    ]
                ];
            }
            else if (subjectData.first_term.thuong_xuyen2 !== undefined) //* If this is true, the subject is a second subject
            {
                tableHeader = ["Điểm thường xuyên 1", "Điểm thường xuyên 2", "Giữa kì", "Cuối kì"
                ];

                tableBody = [
                    [tag("td", "Kì I", '', '', {colspan: 6})], //* '6' is the total number of all columns
                    [
                        tag("td", subjectData.first_term.thuong_xuyen1 ? subjectData.first_term.thuong_xuyen1 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.thuong_xuyen2 ? subjectData.first_term.thuong_xuyen2 : "Chưa có điểm"),
                        tag("td", subjectData.first_term.giua_ki ? subjectData.first_term.giua_ki : "Chưa có điểm"),
                        tag("td", subjectData.first_term.cuoi_ki ? subjectData.first_term.cuoi_ki : "Chưa có điểm"),
                    ],
                    [tag("td", "Kì II", '', '', {colspan: 6})], //* For second term
                    [
                        tag("td", subjectData.second_term.thuong_xuyen1 ? subjectData.second_term.thuong_xuyen1 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.thuong_xuyen2 ? subjectData.second_term.thuong_xuyen2 : "Chưa có điểm"),
                        tag("td", subjectData.second_term.giua_ki ? subjectData.second_term.giua_ki : "Chưa có điểm"),
                        tag("td", subjectData.second_term.cuoi_ki ? subjectData.second_term.cuoi_ki : "Chưa có điểm"),
                    ]
                ];
            }
            else if (subjectData.first_term.is_passed !== undefined) //* If this is true, the subject is a comment subject
            {
                tableHeader = ["Kết quả"] //* dat/ko dat
                tableBody = [
                    [tag("td", "Kì I", '', '', {colspan: 1})],

                    [
                        tag("td", subjectData.first_term.is_passed === null ? "Chưa có điểm" : (subjectData.first_term.is_passed ? "Đạt": "Không đạt"))
                    ],

                    [tag("td", "Kì II", '', '', {colspan: 1})],

                    [
                        tag("td", subjectData.second_term.is_passed === null ? "Chưa có điểm" : (subjectData.second_term.is_passed? "Đạt": "Không đạt"))
                    ]
                ];
            }
            else throw new Error("Lỗi khi lấy dữ liệu");

            //* Display table
            const markTable = createTable(tableHeader, tableBody);

            markDisplayDiv.appendChild(subjectName);
            markDisplayDiv.appendChild(markTable);

        } catch (error) {
            displayMessage(displayMarkMessageDivId,
                error.message,
                "Please try again",
                "error",
                "lg"
            );
            console.error(error);
        }
    });

    //* for create new student year profile
    if(createStudentYearProfileForm) {
        showFormBtn.addEventListener("click", () => {
            createStudentYearProfileForm.classList.toggle("show");
        });

        createStudentYearProfileForm.addEventListener("submit", async event => {
            event.preventDefault();
            const response = await createStudentYearProfile(studentId, createStudentYearProfileForm);
            if(response.status === 200)
            {
                displayMessage(displayMessageDivId, "Đã thêm hồ sơ năm học", "Thêm hồ sơ năm học mới thành công", "alert alert-success", "lg");
                return;
            }
            displayMessage(displayMarkMessageDivId, "Lỗi", "Đã xảy ra lỗi, vui lòng thử lại sau", "alert alert-danger", "lg");
        });
    }
    

    //*Don't code bellow this line!
    if(!updateMarkForm) return;

    updateMarkForm.addEventListener("submit", async event => {
        //* Keep the page from reloading
        event.preventDefault()

        const subjectId = Number(updateMarkForm.querySelector("#updateMarkSubjectSelect").value);
        const newMark = Number(document.getElementById("new_mark").value);
        const markType = document.getElementById("markType").value;
        const semester = Number(document.getElementById("semester").value);
        const year = Number(yearSelect.value);

        if(!markType || isNaN(newMark) || !subjectId || !year )
        {
            displayMessage(displayMarkMessageDivId, "Lỗi", "Vui lòng nhập đầy đủ thông tin", "alert alert-danger", "md");
            return;
        }
        

        //* Call API
        const response = await updateMark(studentId, subjectId, semester, newMark, markType, year);

        displayMessage(displayMessageDivId,
            response.status !== 200 ? "Failed to update mark" : "Update mark successfully",
            response.message,
            response.status === 200 ? "success" : "error",
            "medium"
        ); 
    });
});