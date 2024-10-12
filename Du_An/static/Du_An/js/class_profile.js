console.log(".");
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".nav-link").forEach(button => {
        button.onclick = () => {
            if(document.querySelector(".active"))
            {
                const activated_button = document.querySelector(".active");
                activated_button.classList.remove("active");
                activated_button.classList.add("link-secondary");
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
            button.classList.remove("link-secondary");
        };
    });
});