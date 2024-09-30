document.addEventListener("DOMContentLoaded", () => {
    const subjectsSelect = document.getElementById("subjects_select");

    subjectsSelect.addEventListener("change", () => {

        //* clear the marks display
        for(let child of document.querySelector(".subjectMark").children)
        {
            child.style.display = "none";
        }

        document.getElementById(subjectsSelect.value).style.display = "block";
    });
});