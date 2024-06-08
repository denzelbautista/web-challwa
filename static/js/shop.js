document.addEventListener('DOMContentLoaded', function() {
    fetch('/productos')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const productos = data.productos;
                const container = document.getElementById('productos-container');
                container.innerHTML = '';

                productos.forEach(producto => {
                    const productoDiv = document.createElement('div');
                    productoDiv.className = `col-lg-3 col-md-6 align-self-center mb-30 trending-items ${producto.categoria.toLowerCase()}`;

                    productoDiv.innerHTML = `
                        <div class="item">
                            <div class="thumb">
                                <a href="product-details.html?id=${producto.id}"><img src="${producto.imagen_producto}" alt=""></a>
                                <span class="price"><em>$${producto.precio}</em>$${producto.precio}</span>
                            </div>
                            <div class="down-content">
                                <span class="category">${producto.categoria}</span>
                                <h4>${producto.nombre}</h4>
                                <a href="product-details.html?id=${producto.id}"><i class="fa fa-shopping-bag"></i></a>
                            </div>
                        </div>
                    `;
                    container.appendChild(productoDiv);
                });

                // Add filter functionality
                const filters = document.querySelectorAll('.trending-filter a');
                filters.forEach(filter => {
                    filter.addEventListener('click', function(e) {
                        e.preventDefault();
                        const filterValue = this.getAttribute('data-filter');

                        filters.forEach(f => f.classList.remove('is_active'));
                        this.classList.add('is_active');

                        const items = document.querySelectorAll('.trending-items');
                        items.forEach(item => {
                            if (filterValue === '*' || item.classList.contains(filterValue.substring(1))) {
                                item.style.display = 'block';
                            } else {
                                item.style.display = 'none';
                            }
                        });
                    });
                });
            } else {
                alert('Error al cargar productos.');
            }
        })
        .catch(error => console.error('Error:', error));
});
