function submitForm(event) {
    event.preventDefault();
    const form = document.getElementById('link_form');
    const formData = new FormData(form);

    fetch('/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const linkContainer = document.getElementById('new_link');
            if (linkContainer) {
                linkContainer.href = `${window.location.origin}/${data.custom_id}`;
                linkContainer.textContent = `${window.location.origin}/${data.custom_id}`;
                linkContainer.parentElement.style.display = 'block';
            }
            form.reset();
        } else {
            console.error('Form submission failed:', data.errors || data.message);
            
            const errorDiv = document.createElement('div');
            errorDiv.style.color = 'red';
            errorDiv.style.textAlign = 'center';
            errorDiv.textContent = data.message || 'Form submission failed';
            
            form.parentNode.insertBefore(errorDiv, form);
            
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Error during form submission:', error);
        
        const errorDiv = document.createElement('div');
        errorDiv.style.color = 'red';
        errorDiv.style.textAlign = 'center';
        errorDiv.textContent = 'Network error occurred';
        
        form.parentNode.insertBefore(errorDiv, form);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    });
}