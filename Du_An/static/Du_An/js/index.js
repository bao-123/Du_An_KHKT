import { changeUserInfo, displayMessage } from "./utils.js";

const displayMessageDivId = "displayMessage"; //-i the id of the div that will display messages.

document.addEventListener("DOMContentLoaded", () => {
    //*show change infomation when hover
    const userInfoDivs = document.querySelectorAll(".userInfo");
    const changeUsernameForm = document.getElementById("changeFullNameForm");
    const userFullName = document.getElementById("userFullName");

    userInfoDivs.forEach(element => {
        element.addEventListener("mouseenter", () => {
            element.querySelector(".changeInfoForm").classList.add("show");
        });

        element.addEventListener("mouseleave", () => {
            element.querySelector(".changeInfoForm").classList.remove("show");
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
            document.getElementById("userFullName").textContent = `Chào ${newFullName}`;
        }
    });
});