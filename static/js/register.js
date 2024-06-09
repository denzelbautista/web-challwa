document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register');
    const inputs = form.querySelectorAll('input');
    const submitButton = document.getElementById('form-submit');
    const roleSelect = document.getElementById('role');
    const phoneContainer = document.getElementById('phone-container');
    const phoneInput = document.getElementById('telefono');

    roleSelect.addEventListener('change', function () {
        if (roleSelect.value === 'vendedor') {
            phoneContainer.style.display = 'block';
            phoneInput.required = true;
        } else {
            phoneContainer.style.display = 'none';
            phoneInput.required = false;
            phoneInput.value = ''; // Clear the phone input value if hidden
        }
    });

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
            const response = await fetch('/usuarios', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                window.location.href = '/';
                console.log(result);
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
});
