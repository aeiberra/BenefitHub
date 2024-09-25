document.addEventListener('DOMContentLoaded', () => {
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
                                <h3 class="text-lg font-medium leading-6 text-gray-900 mb-2">Your QR Code</h3>
                                <img src="data:image/png;base64,${qrCode}" alt="QR Code" class="mx-auto">
                                <button class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" onclick="this.closest('#qr-modal').remove()">Close</button>
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
});
