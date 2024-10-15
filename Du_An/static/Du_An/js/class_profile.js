const displayMessageId = "addSubjectTeacherMessageDisplay";

import {clear, displayMessage, teachClass} from "./utils.js"
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
    
    document.getElementById("teachClass").addEventListener("click", async () => {
        const subjectSelector = document.getElementById("subjectSelect");
        const subject_id = subjectSelector.value; //* id of selected subject
        const class_id = subjectSelector.dataset.classid; //* id of the class
        

        if(!subject_id)
        {
            displayMessage(displayMessageId,
                 "Please choose a subject", //* Header of the message
                 "Choose a subject that you want to teach this class", // *message's content
                 "error", //* message type
                 "medium"); //* message size
            return;
        }
        //* call API
        try {
            const response = await teachClass(subject_id, class_id);
            clear(displayMessageId); //* clear existed message.
            displayMessage(displayMessageId,
                response.status !== 200 ? "Error occurs" : "Successfully",
                response.message,
                response.status !== 200 ? "error" : "success",
                "medium"
            );
        } catch (error) {
            console.error(error);
        }
    });
});