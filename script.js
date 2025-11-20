/**
 * Archivo: script.js
 * Propósito: Agregar efectos visuales y dinámicos a la interfaz.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Efecto de focus en los inputs
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            // Añadir una clase para un borde más llamativo al hacer focus
            input.style.boxShadow = '0 0 0 3px rgba(0, 123, 255, 0.3)';
        });

        input.addEventListener('blur', () => {
            // Quitar el box-shadow al perder el focus
            input.style.boxShadow = 'none';
        });
    });
    
    // 2. Control de la transparencia de los contenedores (Asegura el estilo visual)
    const contenedor = document.querySelector('.contenedor');
    if (contenedor) {
        console.log('Efectos JS cargados.');
    }
});