document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login');
    const inputs = form.querySelectorAll('input');
    const submitButton = document.getElementById('form-submit');
    const errorMessage = document.getElementById('error-message');

    inputs.forEach(input => {
        input.addEventListener('input', validateInput);
    });

    form.addEventListener('input', function () {
        const isValid = [...inputs].every(input => input.classList.contains('valid'));
        submitButton.disabled = !isValid;
    });

    function validateInput(event) {
        const input = event.target;
        if (input.value.trim() === '') {
            input.classList.remove('valid');
            input.classList.add('invalid');
        } else {
            input.classList.remove('invalid');
            input.classList.add('valid');
        }
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                console.log(result);
                // No se necesita almacenar el token en localStorage
                errorMessage.style.display = 'none'; // Ocultar el mensaje de error
                // Redirigir a la página principal u otra página
                window.location.href = "/"; // Ejemplo de redirección a otra página
            } else {
                errorMessage.textContent = 'Usuario o contraseña incorrectos';
                errorMessage.style.display = 'block';
                console.log(data)
            }
        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = 'Ocurrió un error. Por favor, inténtelo más tarde.';
            errorMessage.style.display = 'block';
        }
    });

});
