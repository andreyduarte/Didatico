// main.js
import * as api from './api.js';
import * as state from './state.js';
import * as ui from './ui.js';
import * as feedback from './feedback.js';

// Variáveis injetadas do HTML
const { lessonId, lessonTheme, csrfToken } = window.EDITOR_CONFIG;

// Função de inicialização
document.addEventListener('DOMContentLoaded', async () => {
  state.initializeState({ lessonId, lessonTheme, csrfToken });

  // Carregar layouts para a UI
  const res = await fetch(`/api/lesson/${lessonId}/theme-layouts`);
  const layouts = await res.json();
  ui.initializeUI(layouts);

  state.subscribe(handleStateChange);
  await loadSlides();
});

// Manipulador de mudanças de estado
function handleStateChange(event) {
  switch (event) {
    case 'slidesUpdated':
      ui.renderThumbnails();
      ui.updateToolbar();
      break;
    case 'currentSlideChanged':
      loadCurrentSlideContent();
      ui.updateToolbar();
      break;
  }
}

// Funções de orquestração
export async function loadSlides() {
  try {
    const slides = await api.fetchSlides(state.getLessonId(), state.getCsrfToken());
    state.setSlides(slides);
    if (slides.length > 0) {
      state.setCurrentSlideId(slides[0].id);
    } else {
      state.setCurrentSlideId(null);
    }
  } catch (error) {
    feedback.showError(error.message);
  }
}

export async function selectSlide(slideId) {
  state.setCurrentSlideId(slideId);
}

async function loadCurrentSlideContent() {
  const currentSlide = state.getCurrentSlide();
  if (!currentSlide) {
    ui.renderPreview(''); // Limpa o preview se não houver slide
    state.setBlocks([]);
    return;
  }

  try {
    const html = await api.fetchSlidePreview(currentSlide.id);
    ui.renderPreview(html);
    const blocks = await api.fetchSlideBlocks(currentSlide.id);
    state.setBlocks(blocks);
  } catch (error) {
    feedback.showError(error.message);
  }
}

export async function createSlide() {
  try {
    const newSlide = await api.createSlide(state.getLessonId(), state.getCsrfToken());
    state.addSlide(newSlide, state.getCurrentSlideId());
    state.setCurrentSlideId(newSlide.id);
  } catch (error) {
    feedback.showError(error.message);
  }
}

export async function deleteSlide(slideId) {
  if (!confirm('Remover este slide?')) return;
  
  try {
    await api.deleteSlide(slideId, state.getCsrfToken());
    state.removeSlide(slideId);
    
    if (state.getCurrentSlideId() === slideId) {
      const slides = state.getSlides();
      if (slides.length > 0) {
        state.setCurrentSlideId(slides[0].id);
      } else {
        state.setCurrentSlideId(null);
      }
    }
  } catch (error) {
    feedback.showError(error.message);
  }
}

export async function updateSlideData(slideId, data) {
  try {
    await api.updateSlide(slideId, data, state.getCsrfToken());
    state.updateSlideData(slideId, data);
  } catch (error) {
    feedback.showError(error.message);
  }
}

export async function updateBlock(blockId, payload) {
  try {
    await api.updateBlock(blockId, payload, state.getCsrfToken());
    state.updateBlockData(blockId, payload);
  } catch (error) {
    ui.showErrorFeedback(error.message);
  }
}

export async function createBlock(type, payload, index = 0) {
  try {
    const newBlock = await api.createBlock(state.getCurrentSlideId(), type, payload, state.getCsrfToken());
    state.addBlock(newBlock);
  } catch (error) {
    ui.showErrorFeedback(error.message);
  }
}

export async function uploadImage(slideId, file) {
  try {
    return await api.uploadImage(slideId, file, state.getCsrfToken());
  } catch (error) {
    feedback.showError(error.message);
    throw error; // Re-throw para que a UI possa lidar com isso
  }
}
