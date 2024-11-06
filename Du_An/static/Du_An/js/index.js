import { changeUserInfo, displayMessage } from "./utils.js";

const displayMessageDivId = "displayMessage"; //-i the id of the div that will display messages.

document.addEventListener("DOMContentLoaded", () => {
    //*show change infomation when hover
    const userInfoDivs = document.querySelectorAll(".userInfo");
    const changeUsernameForm = document.getElementById("changeFullNameForm");
    const userFullName = document.getElementById("userFullName");
    const showClassesIcon = document.getElementById("showClassesIcon");
    const classes = document.querySelector(".classes");

    userInfoDivs.forEach(element => {
        let timeOutId = null;
        element.addEventListener("mouseenter", () => {
            timeOutId = setTimeout(() => {element.querySelector(".changeInfoForm").classList.add("show"), timeOutId = null},
                             350); //* timeout for showing change info form when hovering over the user info div.
        });

        element.addEventListener("mouseleave", () => {
            if(timeOutId)
            {
                clearTimeout(timeOutId);
                timeOutId = null;
                return;
            }
            setTimeout(() => element.querySelector(".changeInfoForm").classList.remove("show"), 400);
        }); 
    });


    changeUsernameForm.addEventListener("submit", async event => {
        event.preventDefault();

        const newFullName = changeUsernameForm.querySelector("#fullNameInput").value;
        const response = await changeUserInfo("full_name", newFullName);
        if(!response)
        {
            displayMessage(displayMessageDivId,
                "Lỗi",
                "Lỗi xảy ra khi thay đổi họ tên, vui lòng thử lại sau",
                "error",
                "md");
            return;
        }

        displayMessage(displayMessageDivId,
            response.status === 200 ? "Thành công" : "Lỗi",
            response.message,
            response.status === 200? "success" : "error",
            "md"
        );

        if(response.status === 200)
        {
            userFullName.textContent = `Chào ${newFullName}`;
        }
    });

    //*Check if user is a teacher (show classes icon only appear on the page when the user is a teacher)
    if(showClassesIcon)
    {
        showClassesIcon.onclick = () => {
            showClassesIcon.className = classes.classList.contains("show") ? "fa-solid fa-angle-up" : "fa-solid fa-angle-down";
            classes.classList.toggle("show");
            void classes.offsetWidth; // Trigger a reflow or repaint
        };
    }
    
});