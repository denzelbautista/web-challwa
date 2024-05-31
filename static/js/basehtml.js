document.addEventListener('DOMContentLoaded', function () {

    // basehtml.js

    // Función para cerrar sesión
    async function logout() {
        try {
            const response = await fetch('/logout', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (response.ok) {
                const result = await response.json();
                console.log(result.message); // Muestra el mensaje de éxito en la consola
                window.location.href = "/"; // Redirecciona a la página principal
            } else {
                console.error('Error al cerrar sesión:', response.statusText);
                // Maneja el error según sea necesario
            }
        } catch (error) {
            console.error('Error en la solicitud:', error);
            // Maneja el error según sea necesario
        }
    }

    // Ejecuta la función de cierre de sesión al cargar la página
    window.addEventListener('load', function () {
        const logoutButton = document.getElementById('logout-button'); // Reemplaza 'logout-button' con el ID de tu botón de cierre de sesión
        if (logoutButton) {
            logoutButton.addEventListener('click', function (event) {
                event.preventDefault(); // Evita que el formulario se envíe automáticamente
                logout(); // Llama a la función de cierre de sesión al hacer clic en el botón
            });
        }
    });

});