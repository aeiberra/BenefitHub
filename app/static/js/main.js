document.addEventListener('DOMContentLoaded', () => {
    initializeComponents();
    setupNavigationHandlers();
});

function initializeComponents() {
    initializeRedeemForms();
    initializeDeleteForms();
    initializeSortableCategories();
    initializeAnalyticsCharts();
}

function initializeRedeemForms() {
    const redeemForms = document.querySelectorAll('.redeem-form');
    
    redeemForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            
            try {
                const response = await fetch('/redeem', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const qrCode = data.qr_code;
                    
                    // Create a modal to display the QR code
                    const modal = document.createElement('div');
                    modal.innerHTML = `
                        <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="qr-modal">
                            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                                <h3 class="text-lg font-medium leading-6 text-gray-900 mb-2">Tu Código QR:</h3>
                                <img src="data:image/png;base64,${qrCode}" alt="QR Code" class="mx-auto">
                                <button class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onclick="this.closest('#qr-modal').remove()">Cerrar</button>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(modal);
                } else {
                    throw new Error('Failed to redeem benefit');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while redeeming the benefit. Please try again.');
            }
        });
    });
}

function initializeDeleteForms() {
    const deleteForms = document.querySelectorAll('.delete-form');
    
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this item?')) {
                form.submit();
            }
        });
    });
}

function initializeSortableCategories() {
    var el = document.getElementById('sortable-categories');
    if(el) {
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
    }
}

function initializeAnalyticsCharts() {
    const analyticsContainer = document.getElementById('analytics-container');
    if (analyticsContainer) {
        fetch('/admin/api/analytics')
            .then(response => response.json())
            .then(data => {
                createDailyRedemptionsChart(data.daily_redemptions);
                createTopBenefitsChart(data.top_benefits);
                createCategoryRedemptionsChart(data.category_redemptions);
            })
            .catch(error => console.error('Error fetching analytics data:', error));
    }
}

function setupNavigationHandlers() {
    // Add event listener for all links
    document.addEventListener('click', (event) => {
        const link = event.target.closest('a');
        if (link && link.href && !link.target && !event.ctrlKey && !event.metaKey) {
            event.preventDefault();
            navigateToPage(link.href);
        }
    });

    // Handle browser back/forward
    window.addEventListener('popstate', () => {
        navigateToPage(window.location.href);
    });
}

function navigateToPage(url) {
    showLoading();
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            document.title = doc.title;
            const mainContent = doc.querySelector('main');
            if (mainContent) {
                document.querySelector('main').innerHTML = mainContent.innerHTML;
            }
            history.pushState(null, '', url);
            hideLoading();
            initializeComponents();
            initializeAnalyticsCharts();
        })
        .catch(error => {
            console.error('Error:', error);
            hideLoading();
        });
}

function showLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.classList.remove('hidden');
    } else {
        console.warn('Loading element not found');
    }
}

function hideLoading() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.classList.add('hidden');
    } else {
        console.warn('Loading element not found');
    }
}

// Chart creation functions
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
