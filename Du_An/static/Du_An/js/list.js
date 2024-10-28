//-i JS for 'teaching_classes.html' is the page that shows all of the user's teaching classes

document.addEventListener("DOMContentLoaded", () => {
    const classes = document.querySelectorAll(".classroom");

    classes.forEach(element => {
        const showStudentBtn = element.querySelector(".showStudentBtn");
        const btnIcon = showStudentBtn.querySelector("i");
        const studentsDiv = element.querySelector(".student_list");
        const classroomHeader = element.querySelector(".classroom_info");

        //* Toggle the display of the students list when the button is clicked.
        showStudentBtn.addEventListener("click", () =>{

            //* Toggle the icon and the display of the students list.
            btnIcon.className = studentsDiv.classList.contains("show")? "fa fa-angle-up" : "fa fa-angle-down";

            classroomHeader.classList.toggle("show-shadow");
            setTimeout(() => studentsDiv.classList.toggle("show"), 250);

            void studentsDiv.offsetWidth;
        });
    });
    
});