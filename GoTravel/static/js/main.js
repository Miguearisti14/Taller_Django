import { initializeSlider } from "./slider.js";
import { setupNavbar } from "./navbar.js";


document.addEventListener("DOMContentLoaded", () => {

    if (document.querySelector('.slider')) {
        initializeSlider();
    }

    if (document.querySelector('.nav-toggle')) {
        setupNavbar();
    }

});
