// Portfolio Loader - Loads projects from portfolio-config.json

async function loadPortfolio() {
  try {
    // Determine which config file to load based on current page
    const isKorean = window.location.pathname.includes('index-ko.html');
    const configFile = isKorean ? './portfolio-config-ko.json' : './portfolio-config.json';

    const response = await fetch(configFile, { cache: 'no-cache' });
    const config = await response.json();

    loadProjects(config.projects);

  } catch (error) {
    console.error('Error loading portfolio config:', error);
  }
}

function loadProjects(projects) {
  const projectList = document.querySelector('.project-list');
  if (!projectList) return;

  projectList.innerHTML = '';

  projects.forEach(project => {
    const detailedImage = project.detailedImage || project.image;
    const focusItems = [
      project.problem,
      project.role,
      project.engineering,
      project.outcome,
      project.relevance
    ].filter(Boolean);

    const projectItem = document.createElement('li');
    projectItem.className = 'project-item active';
    projectItem.setAttribute('data-filter-item', '');
    projectItem.setAttribute('data-category', project.category.toLowerCase());
    projectItem.setAttribute('data-project-item', '');
    projectItem.setAttribute('data-project-description', project.detailedDescription || project.description);
    projectItem.setAttribute('data-project-technologies', project.technologies.join(', '));
    projectItem.setAttribute('data-project-detailed-image', detailedImage);
    projectItem.setAttribute('data-project-problem', project.problem || '');
    projectItem.setAttribute('data-project-role', project.role || '');
    projectItem.setAttribute('data-project-engineering', project.engineering || '');
    projectItem.setAttribute('data-project-outcome', project.outcome || '');
    projectItem.setAttribute('data-project-relevance', project.relevance || '');

    projectItem.innerHTML = `
      <a href="#" onclick="return false;">
        <figure class="project-img">
          <div class="project-item-icon-box">
            <ion-icon name="eye-outline"></ion-icon>
          </div>
          <img src="${project.image}" alt="${project.title}" loading="lazy">
        </figure>
        <h3 class="project-title" data-project-title>${project.title}</h3>
        <p class="project-category">${capitalizeCategory(project.category)}</p>
        <p class="project-summary">${project.description}</p>
        <div class="project-card-focus">
          ${focusItems.slice(0, 2).map(item => `<span>${item}</span>`).join('')}
        </div>
        <div class="project-card-tech">
          ${project.technologies.slice(0, 4).map(tech => `<span>${tech}</span>`).join('')}
        </div>
      </a>
    `;

    projectList.appendChild(projectItem);
  });

  // Reinitialize filter functionality
  reinitializeFilters();
  reinitializeProjectModals();
}

function capitalizeCategory(category) {
  // Handle specific categories
  const categoryMap = {
    'infrastructure': 'Infrastructure',
    'ai/ml': 'AI/ML',
    'automation': 'Automation',
    '인프라': '인프라',
    '자동화': '자동화'
  };

  return categoryMap[category.toLowerCase()] || category;
}

function reinitializeFilters() {
  const filterItems = document.querySelectorAll("[data-filter-item]");
  const filterBtns = document.querySelectorAll("[data-filter-btn]");
  const selectItems = document.querySelectorAll("[data-select-item]");
  const selectValue = document.querySelector("[data-selecct-value]");
  const select = document.querySelector("[data-select]");

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
  };

  // Add event to filter buttons
  let lastClickedBtn = filterBtns[0];
  for (let i = 0; i < filterBtns.length; i++) {
    // Remove old listeners by cloning
    const newBtn = filterBtns[i].cloneNode(true);
    filterBtns[i].parentNode.replaceChild(newBtn, filterBtns[i]);
  }

  const newFilterBtns = document.querySelectorAll("[data-filter-btn]");
  lastClickedBtn = newFilterBtns[0];

  for (let i = 0; i < newFilterBtns.length; i++) {
    newFilterBtns[i].addEventListener("click", function () {
      let selectedValue = this.innerText.toLowerCase();
      if (selectValue) selectValue.innerText = this.innerText;
      filterFunc(selectedValue);

      lastClickedBtn.classList.remove("active");
      this.classList.add("active");
      lastClickedBtn = this;
    });
  }

  // Add event to select items
  for (let i = 0; i < selectItems.length; i++) {
    const newSelectItem = selectItems[i].cloneNode(true);
    selectItems[i].parentNode.replaceChild(newSelectItem, selectItems[i]);
  }

  const newSelectItems = document.querySelectorAll("[data-select-item]");
  for (let i = 0; i < newSelectItems.length; i++) {
    newSelectItems[i].addEventListener("click", function () {
      let selectedValue = this.innerText.toLowerCase();
      if (selectValue) selectValue.innerText = this.innerText;
      if (select) select.classList.toggle("active");
      filterFunc(selectedValue);
    });
  }
}

function reinitializeProjectModals() {
  const isKorean = document.documentElement.lang === 'ko';
  const detailLabels = isKorean
    ? ['문제 상황', '내 역할', '설계/운영 포인트', '결과/배운 점', '직무 연결성']
    : ['Problem', 'Role', 'Engineering focus', 'Outcome / learning', 'Role fit'];
  const projectItems = document.querySelectorAll("[data-project-item]");
  const projectModal = document.querySelector("[data-project-modal]");
  const projectModalOverlay = document.querySelector("[data-project-modal-overlay]");
  const projectModalCloseBtn = document.querySelector("[data-project-modal-close]");
  const projectModalTitle = document.querySelector("[data-project-modal-title]");
  const projectModalImg = document.querySelector("[data-project-modal-img]");
  const projectModalDescription = document.querySelector("[data-project-modal-description]");
  const projectModalTechnologies = document.querySelector("[data-project-modal-technologies]");
  const projectModalDetails = document.querySelector("[data-project-modal-details]");

  const projectModalFunc = function () {
    if (projectModal && projectModalOverlay) {
      projectModal.classList.toggle("active");
      projectModalOverlay.classList.toggle("active");
    }
  };

  // Add click event to all project items
  if (projectItems.length > 0) {
    for (let i = 0; i < projectItems.length; i++) {
      projectItems[i].addEventListener("click", function (e) {
        e.preventDefault();

        const title = this.querySelector("[data-project-title]").textContent;
        const description = this.getAttribute("data-project-description");
        const technologies = this.getAttribute("data-project-technologies");
        const detailedImage = this.getAttribute("data-project-detailed-image");
        const details = [
          [detailLabels[0], this.getAttribute("data-project-problem")],
          [detailLabels[1], this.getAttribute("data-project-role")],
          [detailLabels[2], this.getAttribute("data-project-engineering")],
          [detailLabels[3], this.getAttribute("data-project-outcome")],
          [detailLabels[4], this.getAttribute("data-project-relevance")]
        ].filter(([, value]) => value);

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
        if (projectModalDetails) {
          projectModalDetails.innerHTML = details.map(([label, value]) => `
            <div class="project-detail-row">
              <h5>${label}</h5>
              <p>${value}</p>
            </div>
          `).join('');
        }

        projectModalFunc();
      });
    }
  }

  // Add click event to modal close button and overlay
  if (projectModalCloseBtn) {
    const newCloseBtn = projectModalCloseBtn.cloneNode(true);
    projectModalCloseBtn.parentNode.replaceChild(newCloseBtn, projectModalCloseBtn);
    newCloseBtn.addEventListener("click", projectModalFunc);
  }

  if (projectModalOverlay) {
    const newOverlay = projectModalOverlay.cloneNode(true);
    projectModalOverlay.parentNode.replaceChild(newOverlay, projectModalOverlay);
    newOverlay.addEventListener("click", projectModalFunc);
  }
}

// Load portfolio when page loads
document.addEventListener('DOMContentLoaded', loadPortfolio);
