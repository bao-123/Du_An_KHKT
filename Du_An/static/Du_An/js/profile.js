import { displayMessage, getSubjectMarks, updateMark } from "./utils.js";
//* Page's constants
const displayMessageDivId = "updateMarkMessage";
const displayMarkMessageDivId = "displayMarkMessage";

document.addEventListener("DOMContentLoaded", () => {
    const subjectsSelect = document.getElementById("subjects_select");
    const updateMarkForm = document.getElementById("updateMarkForm");
    const markDisplayDiv = document.getElementById("markDisplay");
    const studentProfile = document.getElementById("studentProfile");
    
    const studentId = Number(studentProfile.dataset.studentId);

    subjectsSelect.addEventListener("change", async () => {
        try {
            const subjectData = await getSubjectMarks(studentId, Number(subjectsSelect.value)); //TODO: Add year has been selected in 'yearSelect'
            //*Display marks
            //* if this is true, the subject is a main subject
            if(subjectData.thuong_xuyen4 !== undefined)
            {
                
            }
            else if (subjectData.thuong_xuyen2 !== undefined) //* If this is true, the subject is a second subject
            {}
            else if (subjectData.is_passed !== undefined) //* If this is true, the subject is a comment subject
            {}
            else return;
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

    //*Don't code bellow this line!
    if(!updateMarkForm) return;

    updateMarkForm.addEventListener("submit", async event => {
        //* Keep the page from reloading
        event.preventDefault()

        const subjectId = Number(updateMarkForm.querySelector("#updateMarkSubjectSelect").value);
        const newMark = Number(document.getElementById("new_mark").value);
        const markType = document.getElementById("markType").value;
        const semester = Number(document.getElementById("semester").value);

        if(!markType) {
            displayMessage(displayMessageDivId,
                "Cannot update mark",
                "Chon mot cot diem de nhap diem",
                "warning",
                "medium"
            );
            return;
        }
        if(!newMark)
        {
            displayMessage(displayMessageDivId, 
                "Cannot update mark",
                "Please enter new mark",
                "warning",
                "medium"
            );
            return;
        }

        //* Call API
        const response = await updateMark(studentId, subjectId, semester, newMark, markType);

        displayMessage(displayMessageDivId,
            response.status !== 200 ? "Failed to update mark" : "Update mark successfully",
            response.message,
            response.status === 200 ? "success" : "error",
            "medium"
        ); 
    });
});