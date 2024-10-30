import {updateMarkURL, addClassSubjectTeacherURL, getStudentMarksURL, searchStudentURL, changeInfoURL, changePasswordURL} from "./document.js"
//utils

//* function to create HTML tags
export function tag(name, content, classes=[], id='') {
    //@@classes should be an Array

    const element = document.createElement(name);

    for (let CSSClass of classes) { 
        element.classList.add(CSSClass);
    }

    element.textContent = content;
    element.id = id;

    return element;
}


//** function to update student's mark
export async function updateMark(id, subjectId, semester, new_mark, mark_type)
{
    /*
     @@id is the student's id
     @@subject is the name of the subject ("Toán", "Ngữ Văn", ...)
     @@mark_type should be one of these "tx1", "tx2", "tx3", "tx4","gk", "ck"
     @@semester should be 1 or 2 (Number)   
    */
    console.log([id, subjectId, semester, new_mark, mark_type]);
    try
    {
        const response = await fetch(`${updateMarkURL}${id}`, { //-w the "/" is in the 'updateMarkURL' variable
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                subject_id: subjectId,
                semester: semester,
                new_mark: new_mark,
                mark_type: mark_type
            })
        });
        return {message: response.message, status: response.status}
    }
    catch(error)
    {
        console.error(error);
    }
}


//! only use this for change not important info
export async function changeUserInfo(property, value)
{
    try {
        const response = await fetch(changeInfoURL, {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                property: property,
                value: value
            })
        });

        return {status: response.status, message: (await response.json()).message};
    } catch (error) {
        console.error(error);
        return null;
    }
}



export async function changeUserPassword(oldPassword, newPassword) {
    if(!newPassword) throw new Error("Missing arguments");

    if(oldPassword === newPassword) throw new Error("Old password and new password cannot be the same.");

    try {
        const response = await fetch(changePasswordURL, {
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                new_password: newPassword
            })
        });
        return {status: response.status, message: (await response.json()).message};
    } catch (error) {
        console.error();
    }
}

//* a function to set a teacher to be a subject teacher of a particular class
export async function teachClass(subject_id, classroom_id, year=null) {
    //@@subject_id should be a id of a subject 

    try {
        const response = await fetch(addClassSubjectTeacherURL, { 
            method: "PUT",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: JSON.stringify({
                class_id: classroom_id,
                subject_id: subject_id,
                year: year
            })
        }); 

        //* Error in fetching lead to error in decoding JSON.
        const message = await response.json();

        return {status: response.status, message: message.message};
    } catch (error) {
        console.error(error);
    }
}


export async function getSubjectMarks(studentId, subjectId, year=null) {
    try {
        const fetchURL = `${getStudentMarksURL}${studentId}?subject_id=${subjectId}` + (year ? `&${year}` : '');
        const response = await fetch(fetchURL);
        if(response.status !== 200)
        {
            throw new Error((await response.json()).message);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error)
    }
}

export async function searchStudent(query, classroom_id='') {
    try {
        const response = await fetch(`${searchStudentURL}?name=${query}${ classroom_id? `&classroom_id=${classroom_id}` : '' }`);
        const data = await response.json();        
        if (response.status !== 200) {
            return data.message;
        } else {
            return data.search_result;
        }
    } catch (error) {
        console.error(error);
    }
}

// * This function will display a error (or success) message on a particular
export function displayMessage(divId, header, content, type, size)
{
    /*
        @@divId the id of the div that we are gonna display the message in
        @@header is the content for the header of the message, @@content is the content of the message 
        @@type will be the type of the message (valid value are 'error', 'success', 'info', ...)
        @@size is size of message (valid value are 'lg', 'md', 'sm')
    */

        const messageHeader = tag("p", header, ["header"]);
        const messageContent = tag("p", content, ["content"]);

    try {
        clear(divId);
        const messageDiv = document.getElementById(divId);
        messageDiv.classList.add(type, size)
        messageDiv.appendChild(messageHeader);
        messageDiv.appendChild(messageContent);

    } catch (error) {
        console.error(error);
    }
}


//-I Simple function to clear a content of a element
export function clear(divId) {
    const div = document.getElementById(divId);
    if(!div)
    {
        return;
    }

    div.innerHTML = '';
}


//-I simple function to get csrf token
function getCSRF() {
    const parts = document.cookie.split("csrftoken=");
    return parts.length == 2 ? parts.pop().split(";").shift() : '';
} 
