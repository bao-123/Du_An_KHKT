//-i JS for 'teaching_classes.html' is the page that shows all of the user's teaching classes

document.addEventListener("DOMContentLoaded", () => {
    const classes = document.querySelectorAll(".classroom");

    classes.forEach(element => {
        const showStudentBtn = element.querySelector(".showStudentBtn");
        const btnIcon = showStudentBtn.querySelector("i");
        const studentsDiv = element.querySelector(".student_list");

        //* Toggle the display of the students list when the button is clicked.
        showStudentBtn.addEventListener("click", () =>{

            //* Toggle the icon and the display of the students list.
            if(studentsDiv.style.display === "none")
            { //TODO: add animation
                studentsDiv.style.display = "block";
                studentsDiv.style.animation = "height-appear 0.5s ease-in-out";
                btnIcon.className = "fa-solid fa-angle-down";
            }
            else
            {
                //studentsDiv.childNodes.forEach(node => {node.style? node.style.display = "none" : '';});
                studentsDiv.style.animation = "height-disappear 0.5s ease-in-out";
                studentsDiv.addEventListener("animationend", function hideDiv() {
                    studentsDiv.style.display = "none";
                    studentsDiv.removeEventListener("animationend", hideDiv);
                });

                btnIcon.className = "fa-solid fa-angle-up";
            }
        });
    });
    
});