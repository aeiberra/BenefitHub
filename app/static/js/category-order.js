document.addEventListener('DOMContentLoaded', function() {
    var el = document.getElementById('sortable-categories');
    var sortable = Sortable.create(el, {
        handle: '.handle',
        animation: 150,
        onEnd: function (evt) {
            var itemEl = evt.item;
            var newIndex = evt.newIndex;
            var categoryId = itemEl.getAttribute('data-id');
            
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
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Category order updated successfully');
                } else {
                    console.error('Failed to update category order');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
            });
        }
    });
});
