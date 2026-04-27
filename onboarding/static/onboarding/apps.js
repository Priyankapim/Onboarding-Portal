function deleteRow(btn,prefix){
    const row = btn.closest('.form-row');
    const deleteInput = row.querySelector(`input[name$='-DELETE']`);
    if(deleteInput){ deleteInput.checked = true; }
    row.style.display = 'none';
}


function addRow(containerId, prefix, emptyHtml) {
    const container = document.getElementById(containerId);

    // ALWAYS directly target correct TOTAL_FORMS
    const totalForms = document.querySelector(
        `input[name='${prefix}-TOTAL_FORMS']`
    );

    let count = parseInt(totalForms.value);

    // replace Django __prefix__
    let html = emptyHtml.replaceAll("__prefix__", count);

    const div = document.createElement("div");
    div.classList.add("form-row");

    div.innerHTML = html + `
        <button type="button"
                class="btn-delete"
                onclick="deleteRow(this, '${prefix}')">
            Delete
        </button>
    `;

    container.appendChild(div);

    // increase form count
    totalForms.value = count + 1;
}



// Work toggle for Fresher
const workStatus = document.getElementById("id_work_status");
const workSection = document.getElementById("work-section");
function toggleWork(){ if(workStatus && workSection) workSection.style.display=(workStatus.value==="FRESHER")?"none":"block"; }
if(workStatus){ toggleWork(); workStatus.addEventListener("change",toggleWork); }

// Sidebar smooth scroll
const navLinks = document.querySelectorAll(".nav-link");
const sections = document.querySelectorAll(".section");
navLinks.forEach(link=>{
    link.addEventListener("click", function(e){
        e.preventDefault();
        const target = document.querySelector(this.getAttribute("href"));
        if(target) window.scrollTo({top:target.offsetTop-80, behavior:"smooth"});
    });
});

window.addEventListener("scroll", ()=>{
    let current="";
    sections.forEach(section=>{
        const sectionTop = section.offsetTop-120;
        if(pageYOffset>=sectionTop) current=section.getAttribute("id");
    });
    navLinks.forEach(link=>link.classList.remove("active"));
    navLinks.forEach(link=>{ if(link.getAttribute("href")==="#"+current) link.classList.add("active"); });
});

// Sidebar toggle
const toggleBtn = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
const main = document.querySelector(".main");

if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        sidebar.classList.toggle("open");
        main.classList.toggle("full");
    });
}


document.addEventListener("DOMContentLoaded", () => {

    const alerts = document.querySelectorAll('.alert');

    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(el => {
                el.style.opacity = '0';
                setTimeout(() => el.remove(), 300);
            });
        }, 5000);
    }

});


function setLastCompany(button, value) {
    // sab checkboxes false
    document.querySelectorAll(".yes-no-group input[type='checkbox']").forEach(cb => {
        cb.checked = false;
        cb.removeAttribute("checked");
    });

    // sab buttons reset
    document.querySelectorAll(".yes-no-group button").forEach(btn => {
        btn.classList.remove("active-yes", "active-no");
    });

    // current row
    const parent = button.closest(".yes-no-group");
    const checkbox = parent.querySelector("input[type='checkbox']");

    if (value) {
        checkbox.checked = true;
        checkbox.setAttribute("checked", "checked");
        button.classList.add("active-yes");
    } else {
        checkbox.checked = false;
        button.classList.add("active-no");
    }
}


function addWorkRow() {
    const container = document.getElementById("work-container");
    const totalForms = document.getElementById("id_workexperience_set-TOTAL_FORMS");
    const count = parseInt(totalForms.value);

    let html = document.getElementById("empty-work-form").innerHTML;
    html = html.replace(/__prefix__/g, count);

    container.insertAdjacentHTML("beforeend", html);

    totalForms.value = count + 1;
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".yes-no-group").forEach(group => {
        const checkbox = group.querySelector("input[type='checkbox']");
        const buttons = group.querySelectorAll("button");

        if (!checkbox || buttons.length < 2) return;

        const yesBtn = buttons[0];
        const noBtn = buttons[1];

        // reset classes
        yesBtn.classList.remove("active-yes");
        noBtn.classList.remove("active-no");

        // Django rendered checked attribute detect
        if (checkbox.hasAttribute("checked") || checkbox.checked) {
            yesBtn.classList.add("active-yes");
        } else {
            noBtn.classList.add("active-no");
        }
    });
});



