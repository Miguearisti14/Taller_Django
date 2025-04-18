import { initializeSlider } from "./slider.js";
import { setupNavbar } from "./navbar.js";
import { closeBtn } from "./closeBtn.js";


document.addEventListener("DOMContentLoaded", () => {

    if (document.querySelector('.slider')) {
        initializeSlider();
    }

    if (document.querySelector('.nav-toggle')) {
        setupNavbar();
    }

    if (document.querySelectorAll('.close-btn')) {
        closeBtn();
    }

});
