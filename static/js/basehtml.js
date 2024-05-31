document.addEventListener('DOMContentLoaded', function () {
    // Obtener el elemento del menú de navegación
    const navMenu = document.querySelector('.main-nav ul.nav');

    // Función para actualizar el menú de navegación según el estado de autenticación
    function updateNavigationMenu(isAuthenticated) {
        // Limpiar el menú existente
        navMenu.innerHTML = '';

        // Crear nuevos enlaces basados en el estado de autenticación
        if (isAuthenticated) {
            navMenu.innerHTML += `
                <li><a href="/views/index" class="active">Inicio</a></li>
                <li><a href="/views/shop">Tienda</a></li>
                <li><a href="/views/sell">Vende ahora</a></li>
                <li><a href="/views/contact">Contacto</a></li>
                <li><a href="/views/profile">Mi Perfil</a></li>
                <li><a href="#" id="logout-link">Cerrar sesión</a></li>
            `;
        } else {
            navMenu.innerHTML += `
                <li><a href="/views/index" class="active">Inicio</a></li>
                <li><a href="/views/shop">Tienda</a></li>
                <li><a href="/views/sell">Vende ahora</a></li>
                <li><a href="/views/contact">Contacto</a></li>
                <li><a href="/views/register">Regístrate</a></li>
                <li><a href="/views/login">Inicia sesión</a></li>
            `;
        }

        // Añadir el evento click al enlace de cerrar sesión
        const logoutLink = document.querySelector('#logout-link');
        if (logoutLink) {
            logoutLink.addEventListener('click', async function (event) {
                event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace
                const token = localStorage.getItem('token');
                if (!token) {
                    console.error('No se encontró token');
                    return;
                }

                try {
                    // Enviar una solicitud al endpoint de logout
                    const response = await fetch('/logout', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-ACCESS-TOKEN': token
                        },
                    });

                    // Verificar si la solicitud fue exitosa
                    if (response.ok) {
                        // Eliminar el token del localStorage
                        localStorage.removeItem('token');

                        // Redireccionar al usuario de vuelta al inicio
                        window.location.href = '/';
                    } else {
                        // Mostrar un mensaje de error si la solicitud falla
                        alert('Error al cerrar sesión. Por favor, inténtelo de nuevo.');
                    }
                } catch (error) {
                    // Manejar cualquier error de red u otro error
                    console.error('Error:', error);
                    alert('Ocurrió un error al cerrar sesión. Por favor, inténtelo de nuevo más tarde.');
                }
            });
        }
    }

    // Comprobar si el usuario está autenticado (por ejemplo, si hay un token en localStorage)
    const isAuthenticated = localStorage.getItem('token') !== null;
    updateNavigationMenu(isAuthenticated);
});
