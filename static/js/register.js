document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register');
    const inputs = form.querySelectorAll('input');
    const submitButton = document.getElementById('form-submit');

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

        if (input.id === 'password' && !verificarContrasena(input.value)) {
            input.classList.remove('valid');
            input.classList.add('invalid');
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
            const response = await fetch('/usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                alert('User registered successfully!');
                form.reset();
                inputs.forEach(input => input.classList.remove('valid'));
                submitButton.disabled = true;
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.');
        }
    });

    function verificarContrasena(password) {
        // Verifica la longitud
        if (password.length < 8) {
            return false;
        }

        // Verifica si hay al menos una mayúscula
        if (!/[A-Z]/.test(password)) {
            return false;
        }

        // Verifica si hay al menos un carácter especial
        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            return false;
        }

        // La contraseña cumple con todos los requisitos
        return true;
    }
});