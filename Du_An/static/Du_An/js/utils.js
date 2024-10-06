import {updateMarkURL} from "./document.js"
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
//*! Chưa code xog */
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