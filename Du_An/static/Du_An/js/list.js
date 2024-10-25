document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("classSearchBox");
    const classes = document.querySelectorAll(".class");

    searchForm.addEventListener("submit", event => {
        event.preventDefault();

        const className = searchForm.querySelector("#className").value;

        classes.forEach(element => {
            if( element.dataset.name.split(className).length > 1 ) //*Check if the class's name contains the query
            {
                element.style.display = "block";
            }
            else
            {
                element.style.display = "none";
            }
        });

    });
});