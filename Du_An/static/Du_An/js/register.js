import { clear, displayMessage, searchStudent, tag } from "./utils.js"

const searchFormDivId = "searchFormMessage";

document.addEventListener("DOMContentLoaded", () => {
    const childrenSelect = document.getElementById("childrenSelect"); //* The select element
    const childrenSearchSubmit = document.getElementById("childrenSearchSubmit");

    childrenSearchSubmit.addEventListener("click", async () => {

        const query = document.getElementById("childrenName").value;
        if(!query)
        {
            displayMessage(searchFormDivId, "Lỗi", "Nhập tên của học sinh để tìm!", "error", "md");
            return;
        }
        const classroomId = document.getElementById("childrenClassroom").value;
        
        //* call API
        const result = await searchStudent(query, 
            classroomId ? classroomId : ''
        );
        if(typeof(result) === String)
        {
            displayMessage(searchFormDivId, result, "Vui lòng thử lại sau", "error", "md");
            return;
        }

        clear(childrenSelect.id);
        result.forEach(element => {
            const childOption = tag("option", element.student.name);
            childOption.value = element.student.id;
            childrenSelect.appendChild(childOption);
        });
    });
})