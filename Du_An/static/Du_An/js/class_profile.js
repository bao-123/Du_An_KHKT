document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".nav-link").forEach(button => {
        button.onclick = () => {
            if(document.querySelector(".active"))
            {
                document.querySelector(".active").classList.remove("active");
            }
            document.getElementById("infoDisplay").childNodes.forEach(element => {
                if(element.style)
                {
                    element.style.display = "none";
                }
            });
            if (button.id === "teacherTab") 
            {
                document.getElementById("subjectTeachersDisplay").style.display = "block";
            }
            else if(button.id === "studentTab")
            {
                document.getElementById("students").style.display = "block";
            }
            else
            {
                document.getElementById("classDetails").style.display = "block";
            }

            button.classList.add("active");
        };
    });
});