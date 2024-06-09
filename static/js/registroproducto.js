document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('productoForm');
    const alertBox = document.getElementById('alert');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        
        fetch('/productos', {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')  // Asumiendo que el token se guarda en localStorage
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alertBox.style.display = 'block';
                alertBox.classList.remove('alert-danger');
                alertBox.classList.add('alert-success');
                alertBox.innerText = data.message;
                form.reset();

                 // Ocultar el alertBox después de 5 segundos (5000 milisegundos)
                setTimeout(() => {
                    alertBox.style.display = 'none';
                }, 1000);   
            } else {
                alertBox.style.display = 'block';
                alertBox.classList.remove('alert-success');
                alertBox.classList.add('alert-danger');
                alertBox.innerText = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alertBox.style.display = 'block';
            alertBox.classList.remove('alert-success');
            alertBox.classList.add('alert-danger');
            alertBox.innerText = 'Error creando producto';
        });
    });
});