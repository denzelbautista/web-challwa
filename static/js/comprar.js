// comprar.js
/*
document.addEventListener('DOMContentLoaded', function () {
    const carrito = JSON.parse(localStorage.getItem('cart')) || [];
    const numeroTelefono = "922143197"; // Tu número de teléfono

    // Carrito productos
    const productosCarrito = document.getElementById('productos-carrito');
    let total = 10; // Delivery cost
    console.log(total)

    if (carrito.length === 0) {
        productosCarrito.innerHTML = '<p>El carrito está vacío.</p>';
        document.getElementById('comprar-button').disabled = true;
    } else {
        carrito.forEach(producto => {
            const li = document.createElement('li');
            li.textContent = `${producto.nombre} - S/. ${producto.precio} - Cantidad: ${producto.cantidad}`;
            productosCarrito.appendChild(li);
        
            // Verifica si los valores son números válidos
            if (!isNaN(parseFloat(producto.precio)) && !isNaN(parseInt(producto.cantidad))) {
                total += parseFloat(producto.precio) * parseInt(producto.cantidad);
            } else {
                console.error(`Valores inválidos para ${producto.nombre}: precio=${producto.precio}, cantidad=${producto.cantidad}`);
            }
        });
        document.getElementById('total-precio').textContent = total.toFixed(2);
    }

    // Validar el formulario del comprador
    const compradorForm = document.getElementById('comprador-form');
    compradorForm.addEventListener('input', function () {
        const isValid = [...compradorForm.elements].every(input => input.value.trim() !== '');
        document.getElementById('comprar-button').disabled = !isValid;
    });

    // Comprar button click
    document.getElementById('comprar-button').addEventListener('click', async function () {
        const compradorNombre = document.getElementById('comprador-nombre').value;
        const compradorApellido = document.getElementById('comprador-apellido').value;
        const compradorDireccion = document.getElementById('comprador-direccion').value;
        const compradorDni = document.getElementById('comprador-dni').value;

        // Update product stock
        for (let producto of carrito) {
            const response = await fetch(`/productos/${producto.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cantidad: producto.cantidad })
            });
            
            const result = await response.json();
            if (!result.success) {
                alert(`Error con el producto ${producto.nombre}: ${result.message}`);
                return;
            }
        }
        // Obtener los datos del vendedor mediante el id del producto
        





        // Register purchase
        const compraResponse = await fetch('/compras', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dni_usuario: compradorDni,
                productos: carrito.map(p => p.id),
                monto: total
            })
        });
        
        const compraResult = await compraResponse.json();
        if (!compraResult.success) {
            alert(`Error registrando la compra: ${compraResult.message}`);
            return;
        }
    
        // Prepare WhatsApp message
        const productosTexto = carrito.map(p => `${p.nombre} - Cantidad: ${p.cantidad} - Teléfono del vendedor: ${p.telefonoVendedor}`).join('%0A');
        const mensaje = `Resumen de compra:%0ANombre: ${compradorNombre}%0AApellido: ${compradorApellido}%0ADirección de envío: ${compradorDireccion}%0ADNI: ${compradorDni}%0AProductos:%0A${productosTexto}%0ASubtotal: S/. ${total.toFixed(2)}`;

        window.location.href = `https://wa.me/${numeroTelefono}?text=${mensaje}`;
    });
});
*/

document.addEventListener('DOMContentLoaded', async function () {
    const carrito = JSON.parse(localStorage.getItem('cart')) || [];
    const numeroTelefono = "922143197"; // Tu número de teléfono

    // Carrito productos
    const productosCarrito = document.getElementById('productos-carrito');
    let total = 10; // Delivery cost

    if (carrito.length === 0) {
        productosCarrito.innerHTML = '<p>El carrito está vacío.</p>';
        document.getElementById('comprar-button').disabled = true;
    } else {
        for (let producto of carrito) {
            try {
                // Fetch user information for each product
                const response = await fetch(`/usuario/${producto.id}/producto`);
                const result = await response.json();

                if (!result.success) {
                    throw new Error(result.message);
                }

                producto.telefonoVendedor = result.usuario.telefono;

                const li = document.createElement('li');
                li.textContent = `${producto.nombre} - S/. ${producto.precio} - Cantidad: ${producto.cantidad}`;
                productosCarrito.appendChild(li);

                // Verifica si los valores son números válidos
                if (!isNaN(parseFloat(producto.precio)) && !isNaN(parseInt(producto.cantidad))) {
                    total += parseFloat(producto.precio) * parseInt(producto.cantidad);
                } else {
                    console.error(`Valores inválidos para ${producto.nombre}: precio=${producto.precio}, cantidad=${producto.cantidad}`);
                }
            } catch (error) {
                alert(`Error obteniendo información del usuario para el producto ${producto.nombre}: ${error.message}`);
            }
        }
        document.getElementById('total-precio').textContent = total.toFixed(2);
    }

    // Validar el formulario del comprador
    const compradorForm = document.getElementById('comprador-form');
    compradorForm.addEventListener('input', function () {
        const isValid = [...compradorForm.elements].every(input => input.value.trim() !== '');
        document.getElementById('comprar-button').disabled = !isValid;
    });

    // Comprar button click
    document.getElementById('comprar-button').addEventListener('click', async function () {
        const compradorNombre = document.getElementById('comprador-nombre').value;
        const compradorApellido = document.getElementById('comprador-apellido').value;
        const compradorDireccion = document.getElementById('comprador-direccion').value;
        const compradorDni = document.getElementById('comprador-dni').value;

        // Update product stock
        for (let producto of carrito) {
            const response = await fetch(`/productos/${producto.id}`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ cantidad: producto.cantidad })
            });
            
            const result = await response.json();
            if (!result.success) {
                alert(`Error con el producto ${producto.nombre}: ${result.message}`);
                return;
            }
        }

        // Prepare WhatsApp message
        const productosTexto = carrito.map(p => `${p.nombre} - Cantidad: ${p.cantidad} - Teléfono del vendedor: ${p.telefonoVendedor}`).join('%0A');
        const mensaje = `Resumen de compra:%0ANombre: ${compradorNombre}%0AApellido: ${compradorApellido}%0ADirección de envío: ${compradorDireccion}%0ADNI: ${compradorDni}%0AProductos:%0A${productosTexto}%0ASubtotal: S/. ${total.toFixed(2)}`;

        window.location.href = `https://wa.me/${numeroTelefono}?text=${mensaje}`;
    });
});
