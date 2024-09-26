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
    fetch('/admin/api/analytics')
        .then(response => response.json())
        .then(data => {
            // Update total redemptions
            const totalRedemptions = data.daily_redemptions.reduce((sum, day) => sum + day.count, 0);
            document.getElementById('total-redemptions').textContent = totalRedemptions;

            // Update top benefits
            const topBenefitsList = document.getElementById('top-benefits');
            if (topBenefitsList) {
                topBenefitsList.innerHTML = ''; // Clear existing list
                data.top_benefits.forEach(benefit => {
                    const li = document.createElement('li');
                    li.textContent = `${benefit.name}: ${benefit.count} redemptions`;
                    topBenefitsList.appendChild(li);
                });
            }
        })
        .catch(error => console.error('Error fetching stats:', error));
});
