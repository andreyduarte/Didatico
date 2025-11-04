// api.js
const API_BASE_URL = ''; // Pode ser ajustado se a API estiver em um subdomínio diferente

export async function fetchSlides(lessonId, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/lesson/${lessonId}/slides`);
  if (!response.ok) {
    throw new Error('Erro ao carregar slides.');
  }
  return response.json();
}

export async function fetchSlideBlocks(slideId) {
  const response = await fetch(`${API_BASE_URL}/api/slide/${slideId}/blocks`);
  if (!response.ok) {
    throw new Error('Erro ao carregar blocos do slide.');
  }
  return response.json();
}

export async function fetchSlidePreview(slideId) {
  const response = await fetch(`${API_BASE_URL}/api/slide/${slideId}/preview`);
  if (!response.ok) {
    throw new Error('Erro ao carregar preview do slide.');
  }
  return response.text();
}

export async function updateSlide(slideId, data, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/slide/${slideId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(data)
  });
  if (!response.ok) {
    throw new Error('Erro ao atualizar slide.');
  }
  return response.json();
}

export async function createSlide(lessonId, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/lesson/${lessonId}/slide`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    }
  });
  if (!response.ok) {
    throw new Error('Erro ao criar slide.');
  }
  return response.json();
}

export async function deleteSlide(slideId, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/slide/${slideId}`, {
    method: 'DELETE',
    headers: { 'X-CSRFToken': csrfToken }
  });
  if (!response.ok) {
    throw new Error('Erro ao deletar slide.');
  }
  return response.json();
}

export async function updateBlock(blockId, payload, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/block/${blockId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ payload })
  });
  if (!response.ok) {
    throw new Error('Erro ao atualizar bloco.');
  }
  return response.json();
}

export async function createBlock(slideId, type, payload, csrfToken) {
  const response = await fetch(`${API_BASE_URL}/api/slide/${slideId}/block`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify({ type, payload })
  });
  if (!response.ok) {
    throw new Error('Erro ao criar bloco.');
  }
  return response.json();
}

export async function uploadImage(slideId, file, csrfToken) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/slide/${slideId}/upload`, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken },
    body: formData
  });
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Erro ao fazer upload da imagem.');
  }
  return response.json();
}
