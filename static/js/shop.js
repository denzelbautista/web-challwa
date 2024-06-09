document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('productos-container');
    const pagination = document.querySelector('.pagination');
    const itemsPerPage = 12;
    let currentPage = 1;
    let productos = [];

    function fetchProductos() {
        fetch('/productos')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    productos = data.productos;
                    renderProductos();
                    setupPagination();
                } else {
                    alert('Error al cargar productos.');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function renderProductos() {
        const container = document.getElementById('productos-container');
        container.innerHTML = '';
        const start = (currentPage - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const paginatedProductos = productos.slice(start, end);
    
        paginatedProductos.forEach(producto => {
            const productoDiv = document.createElement('div');
            productoDiv.className = 'product-card';
    
            productoDiv.innerHTML = `
                <div class="item">
                    <div class="thumb">
                        <img class="product-image" src="${producto.imagen_producto}" alt="${producto.nombre}">
                    </div>
                    <div class="down-content">
                        <span class="product-category">${producto.categoria}</span>
                        <h4 class="product-name">${producto.nombre}</h4>
                        <span class="product-price">S/. ${producto.precio}</span>
                        <button class="buy-button" data-id="${producto.id}">Comprar</button>
                    </div>
                </div>
            `;
            container.appendChild(productoDiv);
        });
    
        document.querySelectorAll('.buy-button').forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                window.location.href = `/detallesproducto?id=${productId}`;
            });
        });
    }
    

    function setupPagination() {
        pagination.innerHTML = '';
        const pageCount = Math.ceil(productos.length / itemsPerPage);

        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.textContent = i;
            a.href = '#';
            if (i === currentPage) a.classList.add('is_active');
            a.addEventListener('click', function(e) {
                e.preventDefault();
                currentPage = i;
                renderProductos();
                setupPagination();
            });
            li.appendChild(a);
            pagination.appendChild(li);
        }
    }

    fetchProductos();
});
