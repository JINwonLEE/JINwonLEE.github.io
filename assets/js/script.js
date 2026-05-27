'use strict';



// element toggle function
const elementToggleFunc = function (elem) { elem.classList.toggle("active"); }



// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () { elementToggleFunc(sidebar); });



// testimonials variables (optional - only if testimonials section exists)
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");

// modal variable
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");

// modal toggle function
const testimonialsModalFunc = function () {
  if (modalContainer && overlay) {
    modalContainer.classList.toggle("active");
    overlay.classList.toggle("active");
  }
}

// add click event to all modal items (only if they exist)
if (testimonialsItem.length > 0 && modalImg && modalTitle && modalText) {
  for (let i = 0; i < testimonialsItem.length; i++) {

    testimonialsItem[i].addEventListener("click", function () {

      modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
      modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
      modalTitle.innerHTML = this.querySelector("[data-testimonials-title]").innerHTML;
      modalText.innerHTML = this.querySelector("[data-testimonials-text]").innerHTML;

      testimonialsModalFunc();

    });

  }

  // add click event to modal close button
  if (modalCloseBtn) modalCloseBtn.addEventListener("click", testimonialsModalFunc);
  if (overlay) overlay.addEventListener("click", testimonialsModalFunc);
}



// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-selecct-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

if (select) {
  select.addEventListener("click", function () { elementToggleFunc(this); });
}

// add event in all select items
for (let i = 0; i < selectItems.length; i++) {
  selectItems[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    elementToggleFunc(select);
    filterFunc(selectedValue);

  });
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {

  for (let i = 0; i < filterItems.length; i++) {

    if (selectedValue === "all" || selectedValue === "전체") {
      filterItems[i].classList.add("active");
    } else if (selectedValue === filterItems[i].dataset.category) {
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].classList.remove("active");
    }

  }

}

// add event in all filter button items for large screen
let lastClickedBtn = filterBtn[0];

for (let i = 0; i < filterBtn.length; i++) {

  filterBtn[i].addEventListener("click", function () {

    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    filterFunc(selectedValue);

    lastClickedBtn.classList.remove("active");
    this.classList.add("active");
    lastClickedBtn = this;

  });

}



// contact form variables
const form = document.querySelector("[data-form]");
const formInputs = document.querySelectorAll("[data-form-input]");
const formBtn = document.querySelector("[data-form-btn]");

// add event to all form input field
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {

    // check form validation
    if (form.checkValidity()) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }

  });
}



// page navigation variables
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// add event to all nav link
for (let i = 0; i < navigationLinks.length; i++) {
  navigationLinks[i].addEventListener("click", function () {

    for (let i = 0; i < pages.length; i++) {
      if (this.innerHTML.toLowerCase() === pages[i].dataset.page) {
        pages[i].classList.add("active");
        navigationLinks[i].classList.add("active");
        window.scrollTo(0, 0);
      } else {
        pages[i].classList.remove("active");
        navigationLinks[i].classList.remove("active");
      }
    }

  });
}



// project modal functionality
const projectItems = document.querySelectorAll("[data-project-item]");
const projectModal = document.querySelector("[data-project-modal]");
const projectModalOverlay = document.querySelector("[data-project-modal-overlay]");
const projectModalCloseBtn = document.querySelector("[data-project-modal-close]");
const projectModalTitle = document.querySelector("[data-project-modal-title]");
const projectModalImg = document.querySelector("[data-project-modal-img]");
const projectModalDescription = document.querySelector("[data-project-modal-description]");
const projectModalTechnologies = document.querySelector("[data-project-modal-technologies]");

// modal toggle function
const projectModalFunc = function () {
  if (projectModal && projectModalOverlay) {
    projectModal.classList.toggle("active");
    projectModalOverlay.classList.toggle("active");
  }
}

// add click event to all project items
if (projectItems.length > 0) {
  for (let i = 0; i < projectItems.length; i++) {
    projectItems[i].addEventListener("click", function (e) {
      e.preventDefault();

      const title = this.querySelector("[data-project-title]").textContent;
      const description = this.getAttribute("data-project-description");
      const technologies = this.getAttribute("data-project-technologies");
      const detailedImage = this.getAttribute("data-project-detailed-image");

      if (projectModalTitle) projectModalTitle.textContent = title;
      if (projectModalDescription) projectModalDescription.textContent = description;
      if (projectModalImg) {
        projectModalImg.src = detailedImage || this.querySelector("img").src;
        projectModalImg.alt = title;
      }
      if (projectModalTechnologies) {
        projectModalTechnologies.innerHTML = technologies.split(',').map(tech =>
          `<span class="tech-tag">${tech.trim()}</span>`
        ).join('');
      }

      projectModalFunc();
    });
  }
}

// add click event to modal close button and overlay
if (projectModalCloseBtn) projectModalCloseBtn.addEventListener("click", projectModalFunc);
if (projectModalOverlay) projectModalOverlay.addEventListener("click", projectModalFunc);