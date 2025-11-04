// ui.js
import { getSlides, getCurrentSlideId, getCurrentSlide, getBlocks, getBlockById, getLessonTheme } from './state.js';
import { selectSlide, deleteSlide, updateBlock, updateSlideData, createBlock, uploadImage } from './main.js';
import * as feedback from './feedback.js';
import * as api from './api.js';

const elements = {};

export function initializeUI(layouts) {
  elements.slidePreview = document.getElementById('slidePreview');
  elements.layoutSelect = document.getElementById('layoutSelect');
  elements.colorPicker = document.getElementById('colorPicker');
  elements.saveBtn = document.getElementById('saveBtn');
  elements.thumbnailsList = document.getElementById('thumbnailsList');
  elements.addSlideBtn = document.getElementById('addSlideBtn');
  elements.imageModal = document.getElementById('imageModal');
  elements.imageUrlInput = document.getElementById('imageUrlInput');
  elements.imageFileInput = document.getElementById('imageFileInput');
  elements.saveImageBtn = document.getElementById('saveImageBtn');

  elements.layoutSelect.innerHTML = layouts.map(layout => 
    `<option value="${layout.value}">${layout.label}</option>`
  ).join('');

  attachEventListeners();
}

function attachEventListeners() {
  elements.layoutSelect.addEventListener('change', (e) => {
    updateSlideData(getCurrentSlideId(), { layout: e.target.value });
  });

  elements.colorPicker.addEventListener('change', (e) => {
    updateSlideData(getCurrentSlideId(), { background: e.target.value });
  });

  elements.saveBtn.addEventListener('click', () => {
    showSaveFeedback();
  });

  elements.addSlideBtn.addEventListener('click', () => {
    createSlide();
  });

  elements.saveImageBtn?.addEventListener('click', async () => {
    const url = elements.imageUrlInput.value.trim();
    const currentImageBlockId = elements.imageModal.dataset.blockId;
    
    if (!url) return;
    
    try {
      if (currentImageBlockId) {
        await updateBlock(currentImageBlockId, { url });
      } else {
        await createBlock('image', { url });
      }
      bootstrap.Modal.getInstance(elements.imageModal).hide();
      selectSlide(getCurrentSlideId());
    } catch (error) {
      feedback.showError(error.message);
    }
  });

  elements.imageFileInput?.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    try {
      const data = await uploadImage(getCurrentSlideId(), file);
      elements.imageUrlInput.value = data.url;
    } catch (err) {
      feedback.showError(err.message);
    }
  });

  document.addEventListener('keydown', handleKeyboardNavigation);
}

export function renderThumbnails() {
  const slides = getSlides();
  const currentSlideId = getCurrentSlideId();
  
  const thumbnailsHTML = slides.map((s) => {
    const previewHTML = generateThumbnailPreview(s, s.blocks || []);
    
    return `
      <div class="slide-thumbnail ${s.id === currentSlideId ? 'active' : ''}" 
           data-id="${s.id}">
        <div class="slide-thumbnail-number">${s.order}</div>
        <div class="slide-thumbnail-actions">
          <button class="btn btn-icon btn-danger" data-slide-id="${s.id}" title="Deletar">×</button>
        </div>
        <div class="thumbnail-preview">
          ${previewHTML}
        </div>
      </div>
    `;
  }).join('');
  
  elements.thumbnailsList.innerHTML = thumbnailsHTML;

  elements.thumbnailsList.querySelectorAll('.slide-thumbnail').forEach(thumb => {
    thumb.addEventListener('click', () => selectSlide(parseInt(thumb.dataset.id)));
  });
  elements.thumbnailsList.querySelectorAll('.slide-thumbnail-actions .btn-danger').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteSlide(parseInt(btn.dataset.slideId));
    });
  });
}

function generateThumbnailPreview(slide, slideBlocks) {
  const textBlocks = slideBlocks.filter(b => b.type === 'text');
  const imageBlocks = slideBlocks.filter(b => b.type === 'image');
  
  if (slide.layout === 'titulo') {
    const title = textBlocks[0]?.payload?.text || 'Título';
    const subtitle = textBlocks[1]?.payload?.text || '';
    return `<div class="thumb-text">${title.substring(0, 30)}${subtitle ? '<br>' + subtitle.substring(0, 20) : ''}</div>`;
  } else if (slide.layout === 'conteudo') {
    const text = textBlocks[0]?.payload?.text || 'Conteúdo';
    return `<div class="thumb-text">${text.substring(0, 40)}...</div>`;
  } else if (slide.layout === 'sumario') {
    const title = textBlocks[0]?.payload?.text || 'Sumário';
    return `<div class="thumb-text">${title.substring(0, 30)}...</div>`;
  } else if (slide.layout === 'subtitulo') {
    const title = textBlocks[0]?.payload?.text || 'Subtítulo';
    return `<div class="thumb-text">${title.substring(0, 30)}...</div>`;
  }
  
  return `<div class="thumb-empty">${slide.layout}</div>`;
}

export async function renderPreview(html) {
  const slide = getCurrentSlide();
  if (!slide) {
    elements.slidePreview.innerHTML = '<div class="preview-placeholder">Selecione um slide para editar</div>';
    return;
  }

  elements.slidePreview.innerHTML = html;
  attachEditableListeners();
}

export function updateToolbar() {
  const slide = getCurrentSlide();
  if (slide) {
    elements.layoutSelect.value = slide.layout;
    elements.layoutSelect.disabled = false;
    elements.colorPicker.value = slide.background || '#6366f1';
    elements.colorPicker.disabled = false;
    elements.saveBtn.disabled = false;
  } else {
    elements.layoutSelect.disabled = true;
    elements.colorPicker.disabled = true;
    elements.saveBtn.disabled = true;
    elements.slidePreview.innerHTML = '<div class="preview-placeholder">Nenhum slide</div>';
  }
}

let currentImageBlockId = null;

function attachEditableListeners() {
  document.querySelectorAll('.editable-text').forEach(el => {
    el.addEventListener('blur', async function() {
      const blockId = this.dataset.blockId;
      const text = this.innerText.trim();
      
      if (blockId) {
        await updateBlock(blockId, { text });
      } else {
        const index = parseInt(this.dataset.blockIndex);
        await createBlock('text', { text }, index);
      }
      this.classList.remove('editing');
    });
    
    el.addEventListener('focus', function() {
      this.classList.add('editing');
    });
    
    el.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        this.blur();
      }
    });
  });
  
  document.querySelectorAll('.editable-image, .editable-placeholder').forEach(el => {
    el.addEventListener('click', function(e) {
      e.stopPropagation();
      currentImageBlockId = this.dataset.blockId;
      elements.imageModal.dataset.blockId = currentImageBlockId;
      
      const currentBlock = getBlockById(currentImageBlockId);
      elements.imageUrlInput.value = currentBlock?.payload?.url || '';
      
      const modal = new bootstrap.Modal(elements.imageModal);
      modal.show();
    });
  });
}

export function showSaveFeedback() {
  const btn = elements.saveBtn;
  btn.textContent = 'Salvo!';
  btn.classList.remove('btn-success');
  btn.classList.add('btn-secondary');
  setTimeout(() => {
    btn.textContent = 'Salvar';
    btn.classList.remove('btn-secondary');
    btn.classList.add('btn-success');
  }, 1500);
}

export function showErrorFeedback(message) {
  alert(message);
}

function handleKeyboardNavigation(e) {
  if (e.target.tagName === 'INPUT' || 
      e.target.tagName === 'TEXTAREA' || 
      e.target.tagName === 'SELECT' ||
      e.target.isContentEditable) {
    return;
  }

  const slides = getSlides();
  const currentSlideId = getCurrentSlideId();
  if (!currentSlideId || slides.length === 0) return;

  const currentIndex = slides.findIndex(s => s.id === currentSlideId);
  
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
    e.preventDefault();
    if (currentIndex < slides.length - 1) {
      selectSlide(slides[currentIndex + 1].id);
    }
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    e.preventDefault();
    if (currentIndex > 0) {
      selectSlide(slides[currentIndex - 1].id);
    }
  } else if (e.key === 'Home') {
    e.preventDefault();
    selectSlide(slides[0].id);
  } else if (e.key === 'End') {
    e.preventDefault();
    selectSlide(slides[slides.length - 1].id);
  }
}

export function loadThemeCss(theme) {
  const existingLink = document.querySelector('link[data-theme-css]');
  if (existingLink) {
    existingLink.href = `/static/css/${theme}.css`;
  } else {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `/static/css/${theme}.css`;
    link.dataset.themeCss = 'true';
    document.head.appendChild(link);
  }
}
