document.addEventListener("DOMContentLoaded", function () {
    const editProfileBtn = document.getElementById("edit-profile-btn");
    const readOnlyFields = document.querySelectorAll("input[readonly], textarea[readonly]");
    const editableFields = document.querySelectorAll(".editable-fields input, .editable-fields textarea");

    // Función para cambiar la propiedad 'readonly' de los campos editables
    function toggleEditable() {
        editableFields.forEach(field => {
            field.readOnly = !field.readOnly;
        });
    }

    // Función para cambiar el texto del botón de Editar/Guardar
    function toggleButtonText() {
        const isEditing = editProfileBtn.textContent === "Guardar Cambios";
        editProfileBtn.textContent = isEditing ? "Editar Perfil" : "Guardar Cambios";
    }

    // Función para cargar los datos del usuario desde el servidor
    async function loadUserData() {
        try {
            const response = await fetch("/usuarios", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });
            const data = await response.json();
            if (response.ok) {
                const usuario = data.usuario;
                // Actualizar los campos con los datos del usuario
                document.getElementById("nombre").value = usuario.nombre;
                document.getElementById("apellido").value = usuario.apellido;
                document.getElementById("email").value = usuario.email;
                document.getElementById("nombre-empresa").value = usuario.nombre_empresa || "";
                document.getElementById("telefono").value = usuario.telefono || "";
                document.getElementById("descripcion").value = usuario.descripcion || "";
                document.getElementById("direccion-envio").value = usuario.direccion_envio || "";
            } else {
                console.error("Error al cargar los datos del usuario:", data.error);
            }
        } catch (error) {
            console.error("Error de red:", error);
        }
    }

    // Función para enviar los datos actualizados del perfil al servidor
    async function updateUserData() {
        const formData = {
            nombre_empresa: document.getElementById("nombre-empresa").value,
            telefono: document.getElementById("telefono").value,
            descripcion: document.getElementById("descripcion").value,
            direccion_envio: document.getElementById("direccion-envio").value
        };
        try {
            const response = await fetch("/usuarios", {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (response.ok) {
                console.log("Perfil actualizado exitosamente:", data.message);
                // Volver los campos editables a modo de solo lectura
                toggleEditable();
                // Cambiar el texto del botón de nuevo a "Editar Perfil"
                toggleButtonText();
                // Recargar los datos del usuario
                loadUserData();
            } else {
                console.error("Error al actualizar el perfil:", data.error);
            }
        } catch (error) {
            console.error("Error de red:", error);
        }
    }

    // Manejar el evento click del botón Editar/Guardar
    editProfileBtn.addEventListener("click", function () {
        if (editProfileBtn.textContent === "Editar Perfil") {
            // Cambiar los campos editables a modo de edición
            toggleEditable();
            // Cambiar el texto del botón a "Guardar Cambios"
            toggleButtonText();
        } else {
            // Enviar los datos actualizados del perfil al servidor
            updateUserData();
        }
    });

    // Cargar los datos del usuario al cargar la página
    loadUserData();
});
