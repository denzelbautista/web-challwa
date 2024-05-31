// Lógica para cargar los datos del usuario desde el servidor
window.addEventListener('DOMContentLoaded', async function () {
    const userId = 1; // ID del usuario actual (puedes obtenerlo de tu sistema de autenticación)
    const response = await fetch(`/usuarios/${userId}`);
    const userData = await response.json();

    // Actualizar los campos del perfil con los datos del usuario
    document.getElementById('user-image').value = userData.imagen_usuario;
    document.getElementById('nombre').value = userData.nombre;
    document.getElementById('apellido').value = userData.apellido;
    document.getElementById('nombre-empresa').value = userData.nombre_empresa;
    document.getElementById('telefono').value = userData.telefono;
    document.getElementById('descripcion').value = userData.descripcion;
    document.getElementById('direccion-envio').value = userData.direccion_envio;
});

// Lógica para habilitar la edición del perfil
document.getElementById('edit-profile-btn').addEventListener('click', function () {
    document.getElementById('nombre-empresa').removeAttribute('readonly');
    document.getElementById('telefono').removeAttribute('readonly');
    document.getElementById('descripcion').removeAttribute('readonly');
    document.getElementById('direccion-envio').removeAttribute('readonly');
});