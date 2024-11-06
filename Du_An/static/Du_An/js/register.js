import { clear, configFormValidtion, displayMessage, searchStudent, tag } from "./utils.js"

const searchFormDivId = "searchFormMessage";

document.addEventListener("DOMContentLoaded", () => {
    //* Configure Bootstrap form validation.
    configFormValidtion();

    //*Constants
    const childrenSelect = document.getElementById("childrenSelect"); //* The select element
    const childrenSearchSubmit = document.getElementById("childrenSearchSubmit");
    const teacherRadio = document.getElementById("teacher");
    const parentRadio = document.getElementById("parent");   
    const teacherInputDiv = document.getElementById("for_teacher");
    const parentInputDiv = document.getElementById("for_parent")

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

    teacherRadio.addEventListener("click", () => {
        if(teacherRadio.checked)
        {
            if(!parentInputDiv.classList.contains("show")) {
                teacherInputDiv.classList.add("show"); 
                return;
            }

            parentInputDiv.classList.remove("show");
            //* Wait for the parent input div disappeared
            setTimeout(() => {
                teacherInputDiv.classList.add("show");
            }, 900);  
        }
    });

    parentRadio.addEventListener("click", () => {
        if(parentRadio.checked)
        {
            if(!teacherInputDiv.classList.contains("show"))
            {
                parentInputDiv.classList.add("show");
                return;
            }

            teacherInputDiv.classList.remove("show");
            //* Wait for the teacher input div disappeared
            setTimeout(() => {
                parentInputDiv.classList.add("show");
            }, 900); 
        }
    });
    
});