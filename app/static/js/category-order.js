document.addEventListener('DOMContentLoaded', function() {
    var el = document.getElementById('sortable-categories');
    var sortable = Sortable.create(el, {
        handle: '.handle',
        animation: 150,
        onEnd: function (evt) {
            var itemEl = evt.item;
            var newIndex = evt.newIndex;
            var categoryId = parseInt(itemEl.getAttribute('data-id'));
            
            console.log('Updating category order:', { categoryId, newIndex });
            
            // Send the new order to the server
            fetch('/admin/update_category_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category_id: categoryId,
                    new_order: newIndex
                }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    console.log('Category order updated successfully');
                } else {
                    console.error('Failed to update category order:', data.error);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    });
});
