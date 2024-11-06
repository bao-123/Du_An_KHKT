import { displayMessage, getSubjectMarks, tag, updateMark, clear, configFormValidtion, createStudentYearProfile } from "./utils.js";
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
            const headersDiv = tag("div", "", ["headerContainer"]);
            const firstTermDiv = tag("div", "", ["firstTerm"]);
            const secondTermHeader = tag("h2", "Kì 2", ["termHeader"]);
            const secondTermDiv = tag("div", "", ["secondTerm"]);
            const marksDiv = tag("div", "", ["markContainer"]);

            
            if(subjectData.first_term.thuong_xuyen4 !== undefined)
            {
                //*Display headers
                [
                    tag("h3", "Điểm thường xuyên 1", [markHeaderClass]), //!Classes must be placed in an Array!!!
                    tag("h3", "Điểm thường xuyên 2", [markHeaderClass]),
                    tag("h3", "Điểm thường xuyên 3", [markHeaderClass]),
                    tag("h3", "Điểm thường xuyên 4", [markHeaderClass]),
                    tag("h3", "Giữa kì", [markHeaderClass]),
                    tag("h3", "Cuối kì", [markHeaderClass]),
                ].forEach(element => headersDiv.appendChild(element));


                [
                    tag("p", subjectData.first_term.thuong_xuyen1 ? subjectData.first_term.thuong_xuyen1 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.thuong_xuyen2 ? subjectData.first_term.thuong_xuyen2 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.thuong_xuyen3 ? subjectData.first_term.thuong_xuyen3 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.thuong_xuyen4 ? subjectData.first_term.thuong_xuyen4 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.giua_ki ? subjectData.first_term.giua_ki : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.cuoi_ki ? subjectData.first_term.cuoi_ki : "Chưa có điểm", ["diem"]),
                ].forEach(element => firstTermDiv.appendChild(element));

                [
                    tag("p", subjectData.second_term.thuong_xuyen1 ? subjectData.second_term.thuong_xuyen1 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.thuong_xuyen2 ? subjectData.second_term.thuong_xuyen2 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.thuong_xuyen3 ? subjectData.second_term.thuong_xuyen3 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.thuong_xuyen4 ? subjectData.second_term.thuong_xuyen4 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.giua_ki ? subjectData.second_term.giua_ki : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.cuoi_ki ? subjectData.second_term.cuoi_ki : "Chưa có điểm", ["diem"]),
                ].forEach(element => secondTermDiv.appendChild(element));

                marksDiv.classList.add("mainSubject");
                marksDiv.classList.remove("secondSubject");
                marksDiv.classList.remove("commentSubject");

            }
            else if (subjectData.first_term.thuong_xuyen2 !== undefined) //* If this is true, the subject is a second subject
            {
                [
                    tag("h3", "Điểm thường xuyên 1", [markHeaderClass]), //!Classes must be placed in an Array!!!
                    tag("h3", "Điểm thường xuyên 2", [markHeaderClass]),
                    tag("h3", "Giữa kì", [markHeaderClass]),
                    tag("h3", "Cuối kì", [markHeaderClass]),
                ].forEach(element => headersDiv.appendChild(element));

                [
                    tag("p", subjectData.first_term.thuong_xuyen1 ? subjectData.first_term.thuong_xuyen1 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.thuong_xuyen2 ? subjectData.first_term.thuong_xuyen2 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.giua_ki ? subjectData.first_term.giua_ki : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.first_term.cuoi_ki ? subjectData.first_term.cuoi_ki : "Chưa có điểm", ["diem"]),   
                ].forEach(element => firstTermDiv.appendChild(element));

                [
                    tag("p", subjectData.second_term.thuong_xuyen1 ? subjectData.second_term.thuong_xuyen1 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.thuong_xuyen2 ? subjectData.second_term.thuong_xuyen2 : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.giua_ki ? subjectData.second_term.giua_ki : "Chưa có điểm", ["diem"]),
                    tag("p", subjectData.second_term.cuoi_ki ? subjectData.second_term.cuoi_ki : "Chưa có điểm", ["diem"]),   
                ].forEach(element => secondTermDiv.appendChild(element));

                marksDiv.classList.remove("mainSubject");
                marksDiv.classList.remove("commentSubject");
                marksDiv.classList.add("secondSubject");
            }
            else if (subjectData.first_term.is_passed !== undefined) //* If this is true, the subject is a comment subject
            {
                headersDiv.appendChild(tag("h2", "Kết quả", [markHeaderClass])); //* dat/ko dat

                if(subjectData.first_term.is_passed === null)
                {
                    firstTermDiv.appendChild(tag("p", "Chưa có kết quả", ["diem"]));
                }
                else
                {
                    firstTermDiv.appendChild(tag("p", subjectData.first_term.is_passed ? "Đạt" : "Không đạt", ["diem"] ));
                }
                if(subjectData.second_term.is_passed === null)
                {
                    secondTermDiv.appendChild(tag("p", "Chưa có kết quả", ["diem"]));
                }
                else
                {
                    secondTermDiv.appendChild(tag("p", subjectData.second_term.is_passed ? "Đạt" : "Không đạt", ["diem"]));
                }

                marksDiv.classList.add("commentSubject");
                marksDiv.classList.remove("mainSubject");
                marksDiv.classList.remove("secondSubject");
            }
            else return;

            marksDiv.appendChild(firstTermDiv);
            marksDiv.appendChild(secondTermHeader);
            marksDiv.appendChild(secondTermDiv);

            markDisplayDiv.appendChild(subjectName);
            markDisplayDiv.appendChild(headersDiv);
            markDisplayDiv.appendChild(marksDiv);

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

        if(!markType || !newMark || !subjectId || !year ) return;
        

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