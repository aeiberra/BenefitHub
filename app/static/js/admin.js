document.addEventListener('DOMContentLoaded', () => {
    const deleteForms = document.querySelectorAll('.delete-form');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this benefit?')) {
                form.submit();
            }
        });
    });

    // Fetch and display stats
    fetch('/admin/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('total-redemptions').textContent = data.total_redemptions;
            const topBenefitsList = document.getElementById('top-benefits');
            data.top_benefits.forEach(benefit => {
                const li = document.createElement('li');
                li.textContent = benefit.name;
                topBenefitsList.appendChild(li);
            });
        })
        .catch(error => console.error('Error fetching stats:', error));
});
