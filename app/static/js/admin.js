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
            updateDashboardStats(data);
            updateAnalyticsCharts(data);
        })
        .catch(error => console.error('Error fetching stats:', error));
});

function updateDashboardStats(data) {
    // Update total redemptions
    const totalRedemptions = data.daily_redemptions.reduce((sum, day) => sum + day.count, 0);
    const totalRedemptionsElement = document.getElementById('total-redemptions');
    if (totalRedemptionsElement) {
        totalRedemptionsElement.textContent = totalRedemptions;
    }

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
}

function updateAnalyticsCharts(data) {
    createDailyRedemptionsChart(data.daily_redemptions);
    createTopBenefitsChart(data.top_benefits);
    createCategoryRedemptionsChart(data.category_redemptions);
}

function createDailyRedemptionsChart(data) {
    const ctx = document.getElementById('dailyRedemptionsChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(item => item.date),
                datasets: [{
                    label: 'Daily Redemptions',
                    data: data.map(item => item.count),
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

function createTopBenefitsChart(data) {
    const ctx = document.getElementById('topBenefitsChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.name),
                datasets: [{
                    label: 'Redemptions',
                    data: data.map(item => item.count),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

function createCategoryRedemptionsChart(data) {
    const ctx = document.getElementById('categoryRedemptionsChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.map(item => item.name),
                datasets: [{
                    data: data.map(item => item.count),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.6)',
                        'rgba(54, 162, 235, 0.6)',
                        'rgba(255, 206, 86, 0.6)',
                        'rgba(75, 192, 192, 0.6)',
                        'rgba(153, 102, 255, 0.6)',
                        'rgba(255, 159, 64, 0.6)'
                    ]
                }]
            },
            options: {
                responsive: true
            }
        });
    }
}
