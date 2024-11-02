import {mainSubjects, secondSubjects, commentSubjects} from "./document.js";
import { tag } from "./utils.js";

//-i JS for 'teaching_classes.html' is the page that shows all of the user's teaching classes
let current_subject;
document.addEventListener("DOMContentLoaded", () => {
    const classes = document.querySelectorAll(".classroom");

    classes.forEach(element => {
        const showStudentBtn = element.querySelector(".showStudentBtn");
        const btnIcon = showStudentBtn.querySelector("i");
        const studentsDiv = element.querySelector(".student_list");
        const classroomHeader = element.querySelector(".classroom_info");
        const updateMarkBtns = element.querySelectorAll(".updateMarkBtn");

        //* Toggle the display of the students list when the button is clicked.
        showStudentBtn.addEventListener("click", () =>{

            //* Toggle the icon and the display of the students list.
            btnIcon.className = studentsDiv.classList.contains("show")? "fa fa-angle-up" : "fa fa-angle-down";

            classroomHeader.classList.toggle("show-shadow");
            setTimeout(() => studentsDiv.classList.toggle("show"), 250);

            void studentsDiv.offsetWidth;
        });
    });

        updateMarkBtns.forEach(btn => {
            //*Display a form for teacher can update the mark of the student
            btn.addEventListener("click", event => {
                const form = tag("form", '', "updateMarkForm", '', )
            });
        });
});