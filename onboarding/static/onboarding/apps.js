function deleteRow(btn,prefix){
    const row = btn.closest('.form-row');
    const deleteInput = row.querySelector(`input[name$='-DELETE']`);
    if(deleteInput){ deleteInput.checked = true; }
    row.style.display = 'none';
}

function addRow(containerId,prefix,emptyHtml){
    const container = document.getElementById(containerId);
    const totalForms = document.querySelector(`input[name='${prefix}-TOTAL_FORMS']`);
    let count = parseInt(totalForms.value);
    const html = emptyHtml.replace(/__prefix__/g,count);
    const div = document.createElement('div');
    div.classList.add('form-row');
    div.innerHTML = html + `<button type="button" class="btn-delete" onclick="deleteRow(this,'${prefix}')">Delete</button>`;
    container.appendChild(div);
    totalForms.value = count+1;
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

toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    main.classList.toggle("full");
});



