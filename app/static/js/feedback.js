// feedback.js
export function showSuccess(message) {
  console.log('Sucesso:', message); // Temporário, substituir por um toast/elemento UI
  // Ex: showToast('success', message);
}

export function showError(message) {
  console.error('Erro:', message); // Temporário, substituir por um toast/elemento UI
  // Ex: showToast('error', message);
}

export function showInfo(message) {
  console.info('Info:', message); // Temporário, substituir por um toast/elemento UI
  // Ex: showToast('info', message);
}

// Função de exemplo para um toast (requer HTML e CSS para funcionar)
/*
function showToast(type, message) {
  const toastContainer = document.getElementById('toastContainer'); // Crie este elemento no seu HTML
  if (!toastContainer) {
    console.warn('Toast container not found. Falling back to console log.');
    if (type === 'error') console.error(message);
    else if (type === 'success') console.log(message);
    else console.info(message);
    return;
  }

  const toast = document.createElement('div');
  toast.className = `toast align-items-center text-white bg-${type} border-0`;
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'assertive');
  toast.setAttribute('aria-atomic', 'true');
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        ${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  toastContainer.appendChild(toast);
  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();
  toast.addEventListener('hidden.bs.toast', () => toast.remove());
}
*/
