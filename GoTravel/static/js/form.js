export function setupForm() {
    var handleForm = (event) => {
        event.preventDefault();

        const form = event.target;
        const userField = form[0].value;
        const emailField = form[1].value;
        const asuntField = form[2].value;
        const messageField = form[3].value;

        localStorage.setItem("nombre", userField);
        localStorage.setItem("correo", emailField);
        localStorage.setItem("asunto", asuntField);
        localStorage.setItem("mensaje", messageField);

        form.reset();
    };

    var form = document.getElementById("formulario");

    if (form) {
        form.addEventListener("submit", handleForm);
    } else {
        console.error("No se encontró el formulario.");
    }
}
