document.addEventListener('DOMContentLoaded', function() {
    // Add fade out effect to alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });

    // Initialize Bootstrap modals
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
    
    // Delete confirmation handling
    const deleteButtons = document.querySelectorAll('.btn-outline-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const deleteUrl = this.getAttribute('href');
            const deleteForm = document.getElementById('deleteForm');
            deleteForm.setAttribute('action', deleteUrl);
            deleteModal.show();
        });
    });

    // Add hover effect to table rows
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.transform = 'scale(1.01)';
            row.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', () => {
            row.style.transform = 'scale(1)';
            row.style.backgroundColor = '';
        });
    });

    // Add smooth scroll to top button
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '↑';
    scrollBtn.className = 'scroll-top-btn';
    document.body.appendChild(scrollBtn);

    window.onscroll = () => {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    };

    scrollBtn.onclick = () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    // Add modal focus handling
    const modalInputs = document.querySelectorAll('.modal input, .modal button');
    modalInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                const modal = this.closest('.modal');
                if (modal) {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                }
            }
        });
    });
});
