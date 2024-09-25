document.addEventListener('DOMContentLoaded', () => {
    // Animate elements on page load
    gsap.from('.fade-in', { opacity: 0, duration: 1, ease: 'power2.out' });
    gsap.from('.slide-in-left', { x: -50, opacity: 0, duration: 1, ease: 'power2.out', stagger: 0.1 });
    gsap.from('.slide-in-bottom', { y: 50, opacity: 0, duration: 1, ease: 'power2.out', stagger: 0.1 });

    // Smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Parallax effect for header images
    const headerImages = document.querySelectorAll('.header-image');
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        headerImages.forEach(image => {
            const speed = image.dataset.speed || 0.5;
            gsap.to(image, { y: scrolled * speed, ease: 'none' });
        });
    });

    // Form validation and floating labels
    const formInputs = document.querySelectorAll('.form-input');
    formInputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('focused');
        });
        input.addEventListener('blur', () => {
            if (input.value === '') {
                input.parentElement.classList.remove('focused');
            }
        });
    });

    // Redeem form handling with loading state and animations
    const redeemForms = document.querySelectorAll('.redeem-form');
    redeemForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(form);
            const submitButton = form.querySelector('button[type="submit"]');
            
            try {
                submitButton.disabled = true;
                gsap.to(submitButton, { opacity: 0.5, duration: 0.3 });
                submitButton.innerHTML = '<svg class="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>Canjeando...';
                
                const response = await fetch('/redeem', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const qrCode = data.qr_code;
                    
                    const modal = document.createElement('div');
                    modal.innerHTML = `
                        <div class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full" id="qr-modal">
                            <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
                                <div class="mt-3 text-center">
                                    <h3 class="text-lg font-medium leading-6 text-gray-900 mb-2">Tu Código QR</h3>
                                    <div class="mt-2 px-7 py-3">
                                        <img src="data:image/png;base64,${qrCode}" alt="QR Code" class="mx-auto">
                                    </div>
                                    <div class="items-center px-4 py-3">
                                        <button id="close-modal" class="px-4 py-2 bg-blue-500 text-white text-base font-medium rounded-md w-full shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-300">
                                            Cerrar
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    document.body.appendChild(modal);
                    gsap.from('#qr-modal > div', { scale: 0.8, opacity: 0, duration: 0.5, ease: 'back.out(1.7)' });
                    
                    document.getElementById('close-modal').addEventListener('click', () => {
                        gsap.to('#qr-modal', { opacity: 0, duration: 0.3, onComplete: () => {
                            document.getElementById('qr-modal').remove();
                        }});
                    });
                } else {
                    throw new Error('Failed to redeem benefit');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Ocurrió un error al canjear el beneficio. Por favor, inténtalo de nuevo.');
            } finally {
                submitButton.disabled = false;
                gsap.to(submitButton, { opacity: 1, duration: 0.3 });
                submitButton.innerHTML = 'Canjear Beneficio';
            }
        });
    });

    // Infinite scroll for benefit listings
    const benefitContainer = document.querySelector('.benefit-container');
    if (benefitContainer) {
        let page = 1;
        const loadMoreBenefits = async () => {
            const response = await fetch(`/api/benefits?page=${page}`);
            const data = await response.json();
            if (data.benefits.length > 0) {
                data.benefits.forEach(benefit => {
                    const benefitCard = createBenefitCard(benefit);
                    benefitContainer.appendChild(benefitCard);
                    gsap.from(benefitCard, { opacity: 0, y: 50, duration: 0.5, ease: 'power2.out' });
                });
                page++;
            }
        };

        const createBenefitCard = (benefit) => {
            const card = document.createElement('div');
            card.className = 'benefit-card';
            card.innerHTML = `
                <img src="${benefit.image_url}" alt="${benefit.name}" class="w-full h-48 object-cover hover-brightness">
                <div class="p-4">
                    <h3 class="font-semibold text-lg mb-2 text-gray-800">${benefit.name}</h3>
                    <p class="text-gray-600 mb-4">${benefit.description}</p>
                    <a href="/benefit/${benefit.id}" class="btn-primary inline-block hover-scale">Ver Detalles</a>
                </div>
            `;
            return card;
        };

        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                loadMoreBenefits();
            }
        }, { rootMargin: '100px' });

        const sentinel = document.createElement('div');
        benefitContainer.appendChild(sentinel);
        observer.observe(sentinel);
    }

    // Show loading icon before navigating to a new page
    document.addEventListener('click', (e) => {
        const target = e.target.closest('a');
        if (target && target.href && !target.href.startsWith('#') && !target.href.includes('javascript:')) {
            e.preventDefault();
            document.getElementById('loading-icon').style.display = 'flex';
            setTimeout(() => {
                window.location.href = target.href;
            }, 100);
        }
    });

    // Show loading icon on form submissions
    document.addEventListener('submit', (e) => {
        document.getElementById('loading-icon').style.display = 'flex';
    });

    // Hide loading icon when page is fully loaded
    window.addEventListener('load', () => {
        document.getElementById('loading-icon').style.display = 'none';
    });

    console.log('DOMContentLoaded event fired');
    console.log('Initial loading icon display:', document.getElementById('loading-icon').style.display);
});