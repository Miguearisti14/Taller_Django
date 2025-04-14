export function closeBtn() {
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.parentElement.style.opacity = '0';
            setTimeout(() => {
                btn.parentElement.remove();
            }, 300); // Coincide con la duración de la animación de salida si la añades
        });
    });
}