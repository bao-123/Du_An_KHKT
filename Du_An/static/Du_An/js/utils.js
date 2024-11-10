import {updateMarkURL, addClassSubjectTeacherURL, getStudentMarksURL, searchStudentURL, changeInfoURL, changePasswordURL, newStudentYearProfileURL, mainSubjects, secondSubjects, commentSubjects} from "./document.js"
//-i utils


/**
 * Creates an HTML table element with the specified headers and body content.
 *
 * @param {Array} thead - An array of strings representing the table headers.
 * @param {Array} tbody - An array of arrays, where each sub-array represents a row of table cells (elements).
 * @returns {HTMLElement} - The constructed HTML table element.
 * 
 */
export function createTable(thead, tbody) {
    const table = tag("table", '', "table");
    const tHead = tag("thead", '' );
    const tBodyElement = tag("tbody", '');

    //*Loops through the table's header
    for (let i = 0; i < thead.length; i++) {
        tHead.appendChild(tag("th", thead[i], 'markTableHeader', '', {scope: "col"}));
    }
    
    //*Loops through the rows in the table's body
    for (let i = 0; i < tbody.length; i++) {
        const tRow =  tag("tr", '', '');
        tbody[i].forEach(element => tRow.appendChild(element));

        tBodyElement.appendChild(tRow);
    }

    table.appendChild(tHead);
    table.appendChild(tBodyElement);

    return table;
}


//* function to create HTML tags
export function tag(name, content, classes=[], id='', attr={}) {
    //@@classes should be an Array

    const element = document.createElement(name);

    if(Array.isArray(classes))
    {
        element.className = classes.join(' ');
    }
    else
    {
        element.className = classes;
    }


    if(attr)
    {
        Object.entries(attr).forEach(([key, value]) => element.setAttribute(key, value));
    }

    element.textContent = content;
    element.id = id;

    return element;
}


//* For bootstrap form validtion
export function configFormValidtion() {
    document.querySelectorAll(".needs-validation").forEach(form => {
        form.addEventListener("submit", event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add("was-validated");
        });
    });
}


//** function to update student's mark
export async function updateMark(id, subjectId, semester, new_mark, mark_type, year=null)
{
    /*
     @@id is the student's id
     @@subjectId is the id of the subject
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
                mark_type: mark_type,
                year: year
            })
        });
        return {message: response.message, status: response.status};
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
        const fetchURL = `${getStudentMarksURL}${studentId}?subject_id=${subjectId}` + (year ? `&year=${year}` : '');
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


export async function createStudentYearProfile(studentId, form) { 
    //@@form should be a HTML form element

    try {
        const response = await fetch(`${newStudentYearProfileURL}${studentId}`, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRF()
            },
            body: new FormData(form)
        });
    } catch (error) {
        console.error(error);
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
        messageDiv.className = `${type} ${size}`;
        messageDiv.appendChild(messageHeader);
        messageDiv.appendChild(messageContent);

    } catch (error) {
        console.error(error);
    }
}



/*
 -i This function retrieves the list of mark types for a given subject.
  
  @@param {string} subjectName - The name of the subject.
  @@returns {Array} - An array of mark types for the subject.
  
  -w throws {Error} - Throws an error if the subject name is invalid.
  
  *example
  * getSubjectMarkColumn("Toán") // ["tx1", "tx2", "tx3", "tx4", "gk", "ck"]
  * getSubjectMarkColumn("Văn") // ["tx1", "tx2", "gk", "ck"]
  * getSubjectMarkColumn("Sinh") // ["gk", "ck"]
  * getSubjectMarkColumn("Lịch Sử") // Throws an error: Invalid subject name: Lịch Sử    
 */
export function getSubjectMarkColumn(subjectName) {

    const tx1 = {value: "tx1", display: "Điểm thường xuyên 1"};
    const tx2 = {value: "tx2", display: "Điểm thường xuyên 2"};
    const tx3 = {value: "tx3", display: "Điểm thường xuyên 3"};
    const tx4 = {value: "tx4", display: "Điểm thường xuyên 4"};
    const gk = {value: "gk", display: "Điểm giữa kì"};
    const ck = {value: "ck", display: "Điểm cuối kì"};

    if(mainSubjects.includes(subjectName) ) return [tx1, tx2 , tx3,
                                            tx4, gk, ck];
    else if(secondSubjects.includes(subjectName)) return [tx1, tx2, gk, ck];
    else if(commentSubjects.includes(subjectName)) return [ck]; //* elevualate-by-comment subject only have one mark column
    else throw new Error("Invalid subject name:" + subjectName);
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


export function removeAll(elemetClass){
    const elements = document.querySelectorAll("." + elemetClass);

    if(!elements)
    {
        return;
    }
    elements.forEach(element => element.remove());
}

//-I simple function to create a element with given tag and content

//-I simple function to get csrf token
function getCSRF() {
    const parts = document.cookie.split("csrftoken=");
    return parts.length == 2 ? parts.pop().split(";").shift() : '';
} 
