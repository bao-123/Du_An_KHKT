//-i JS for 'teaching_classes.html' is the page that shows all of the user's teaching classes

document.addEventListener("DOMContentLoaded", () => {
    const classes = document.querySelectorAll(".classroom");

    classes.forEach(element => {
        const showStudentBtn = element.querySelector(".showStudentBtn");
        const btnIcon = showStudentBtn.querySelector("i");

        showStudentBtn.addEventListener("click", () =>{
            const studentsDiv = element.querySelector(".student_list");

            if(studentsDiv.style.display === "none")
            { //TODO: add animation
                studentsDiv.style.display = "block";
                btnIcon.className = "fa-solid fa-angle-down";
            }
            else
            {
                studentsDiv.style.display = "none";
                btnIcon.className = "fa-solid fa-angle-up";
            }
        });
    });
    
});