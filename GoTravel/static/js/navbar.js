export function setupNavbar() {
    // Barra de navegación

    // Seleccionamos el botón y la lista de navegación
    const navToggle = document.querySelector('.nav-toggle');
    const navUl = document.querySelector('nav ul');

    // Al hacer clic en el botón, alternamos la clase "active" en el menú
    navToggle.addEventListener('click', () => {
        navUl.classList.toggle('active');
    });
}
