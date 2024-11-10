import { displayMessage, getSubjectMarkColumn, updateMark, removeAll, tag } from "./utils.js";

const displayMessageDivId = "displayMessage"; //the id of the div that we use to display messages
//-i JS for 'teaching_classes.html' is the page that shows all of the user's teaching classes
let current_subject;
document.addEventListener("DOMContentLoaded", () => {
    const classes = document.querySelectorAll(".classroom");
    const subjectSelect = document.getElementById("subjectSelect");

    classes.forEach(element => {
        const showStudentBtn = element.querySelector(".showStudentBtn");
        const btnIcon = showStudentBtn.querySelector("i");
        const studentsDiv = element.querySelector(".student_list");
        const classroomHeader = element.querySelector(".classroom_info");
        const updateMarkBtns = element.querySelectorAll(".updateMarkBtn");

        //* Toggle the display of the students list when the button is clicked.
        showStudentBtn.addEventListener("click", () =>{

            //* Toggle the icon and the display of the students list.
            btnIcon.className = studentsDiv.classList.contains("show")? "fa fa-angle-up" : "fa fa-angle-down";

            classroomHeader.classList.toggle("show-shadow");
            setTimeout(() => studentsDiv.classList.toggle("show"), 250);

            void studentsDiv.offsetWidth;
        });

        updateMarkBtns.forEach(btn => {
            //*Display a form for teacher can update the mark of the student
            btn.addEventListener("click", event => {
                if(!subjectSelect.value)
                {
                    displayMessage(displayMessageDivId, "Không thể cập nhập điểm",
                         "Xin hãy chọn một môn học trước khi nhập điểm", "alert alert-danger", "md");
                    return;
                }
                const studentId = Number(btn.parentElement.dataset.id);
                const subjectInfo = subjectSelect.value.split(",");
                const subjectName = subjectInfo[1];
                const subjectId = subjectInfo[0];

                const form = tag("form", '', "updateMarkForm needs-validation", '', {novalidate: true});
                const inputDiv = tag("div", '', "form-floating");

                const newMarkInput = tag("input", '', "form-control", 'newMark', {placeholder: "Nhập điểm mới",
                                                                                        type: "number",
                                                                                        min: 0,
                                                                                        max: 10,
                                                                                        step: '0.01',
                                                                                        required: true
                });
                const inputLabel = tag("label", "Điểm", [], '', {for: 'newMark'});

                //* Append elements into floating input div
                inputDiv.appendChild(newMarkInput);
                inputDiv.appendChild(inputLabel);
                
                const markTypeSelector = tag("select", '', "form-select", 'markType', {required: true});
                //*Default option
                markTypeSelector.innerHTML = '<option selected disable value="">Chọn cột điểm</option>';

                try {

                    getSubjectMarkColumn(subjectName).forEach(column => markTypeSelector.innerHTML += `\n <option value=${column.value}>${column.display}</option>`);   
                } catch (error) {
                    console.error(error);
                    return;
                }

                const semesterSelect = tag("select", '', "form-select w-auto", 'semesterSelect', {size: 2});

                //*Options
                semesterSelect.appendChild(new Option("Kì 1", "1", true, true))
                semesterSelect.appendChild(new Option("Kì 2", "2"));
                
                
                const submitBtn = tag("button", 'Nhập điểm', "btn btn-primary", '', {type: "submit"});

                //* Append elements into form
                form.appendChild(inputDiv);
                form.appendChild(markTypeSelector);
                form.appendChild(semesterSelect);
                form.appendChild(submitBtn);

                //-i In CSS form's attribute 'position' in CSS should be 'absolute'
                form.style.top = event.pageY + "px";
                form.style.left = event.pageX + "px";

                //* Remove all of the update mark forms on screen
                removeAll("updateMarkForm");

                //*Add event listeners for form
                form.addEventListener("submit", async (event) => {
                   event.preventDefault();
                   
                   const semester = Number(form.querySelector("#semesterSelect").value);
                   const newMark = form.querySelector('#newMark').value;
                   const markType = form.querySelector("#markType").value;

                   if(!newMark || !markType) 
                   {
                        displayMessage(displayMessageDivId, "Lỗi", "Xin vui lòng chọn cột điểm muốn nhập", "alert alert-danger", "md");
                        return;
                   }

                   const response = await updateMark(studentId, subjectId, semester, newMark, markType);

                   if(response.status !== 200)
                   {
                        displayMessage(displayMessageDivId, "Lỗi", response.message, "alert alert-danger", "md");
                        return;
                   }

                   displayMessage(displayMessageDivId, "Thành Công", "Đã Cập Nhật Điểm Thành Công", "alert alert-success", "md");
                   //* Remove the form
                   form.remove();
                });
                //* Append form to DOM
                document.body.appendChild(form);
            });
        });
    });
});