import {updateMarkURL, addClassSubjectTeacherURL} from "./document.js"
//utils

//* function to create HTML tags
function tag(name, content, classes, id='') {
    const element = document.createElement(name);

    for (let CSSClass of classes) { //** classes should be a array.
        element.classList.add(CSSClass);
    }

    element.textContent = content;
    if(id)
    {
        element.id = id;
    }
    return element;
}


//** function to update student's mark
async function updateMark(id, subject, semester, new_mark, mark_type)
{
    /*
     @@id is the student's id
     @@subject is the name of the subject ("Toán", "Ngữ Văn", ...)
     @@mark_type should be one of these "tx1", "tx2", "tx3", "tx4","gk", "ck"
     @@semester should be 1 or 2 (Number)   
    */
      
    try
    {
        const response = await fetch(`${updateMarkURL}/${id}`, {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                id: id,
                subject: subject,
                semester: semester,
                new_mark: new_mark,
                mark_type: mark_type //* mark_type should be something like 'thuong_xuyen1', 'thuong_xuyen2', 'giua_ki',...
            })
        });
        return {message: response.message, status: response.status}
    }
    catch(error)
    {
        console.error(error);
    }
}


//* a function to set a teacher to be a subject teacher of a particular class
async function teachClass(subject_id, classroom_id) {
    //@@subject_id should be a id of a subject 

    try {
        const response = await fetch(addClassSubjectTeacherURL, {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                class_id: classroom_id,
                subject_id: subject_id
            })
        });
        return {status: response.status, message: (await response.json()).message};
    } catch (error) {
        console.error(error);
    }
}

// * This function will display a error (or success) message on a particular
function displayMessage(divId, header, content, type, size)
{
    /*
        @@divId the id of the div that we are gonna display the message in
        @@header is the content for the header of the message, @@content is the content of the message 
        @@type will be the type of the message (valid value are 'error', 'success', 'info', ...)
        @@size is size of message (valid value are 'lg', 'md', 'sm')
    */

    const messageDiv = document.createElement("div");
    const messageHeader = document.createElement("p");
    const messageContent = document.createElement("p");

    messageDiv.classList.add(type, size);
    messageHeader.classList.add("header");
    messageContent.classList.add("content");

    messageDiv.appendChild(messageHeader);
    messageDiv.appendChild(messageContent);

    try {
        document.getElementById(divId).appendChild(messageDiv);
    } catch (error) {
        console.error(error);
    }
}


//-I simple function to get csrf token
function getCSRF() {
    const parts = document.cookie.split("csrftoken=");
    return parts.length == 2 ? parts.pop().split(";").shift() : '';
}