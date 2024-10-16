import { displayMessage, updateMark } from "./utils.js";
//* Page's constants
const displayMessageDivId = "updateMarkMessage";

document.addEventListener("DOMContentLoaded", () => {
    const subjectsSelect = document.getElementById("subjects_select");
    const updateMarkForm = document.getElementById("updateMarkForm");

    subjectsSelect.addEventListener("change", () => {

        //* clear the marks display
        for(let child of document.querySelector(".subjectMark").children)
        {
            child.style.display = "none";
        }

        document.getElementById(subjectsSelect.value).style.display = "block";
    });

    updateMarkForm.addEventListener("submit", async event => {
        //* Keep the page from reloading
        event.preventDefault()

        const studentId = Number(updateMarkForm.dataset.studentId);
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