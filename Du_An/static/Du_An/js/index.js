document.addEventListener("DOMContentLoaded", () => {
    //*show change infomation when hover
    const userInfoDivs = document.querySelectorAll(".userInfo");

    userInfoDivs.forEach(element => {
        element.addEventListener("mouseenter", () => {
            element.querySelector(".changeInfoForm").classList.add("show");
        });

        element.addEventListener("mouseleave", () => {
            element.querySelector(".changeInfoForm").classList.remove("show");
        }); 

    });

});