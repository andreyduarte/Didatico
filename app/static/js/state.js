// state.js
let slides = [];
let currentSlideId = null;
let blocks = [];
let lessonTheme = '';
let lessonId = null;
let csrfToken = '';

const subscribers = [];

export function initializeState(config) {
  lessonId = config.lessonId;
  lessonTheme = config.lessonTheme;
  csrfToken = config.csrfToken;
}

export function getLessonId() {
  return lessonId;
}

export function getLessonTheme() {
  return lessonTheme;
}

export function getCsrfToken() {
  return csrfToken;
}

export function getSlides() {
  return [...slides]; // Retorna uma cópia para evitar modificações diretas
}

export function setSlides(newSlides) {
  slides = newSlides;
  notifySubscribers('slidesUpdated');
}

export function getCurrentSlideId() {
  return currentSlideId;
}

export function setCurrentSlideId(id) {
  currentSlideId = id;
  notifySubscribers('currentSlideChanged');
}

export function getCurrentSlide() {
  return slides.find(s => s.id === currentSlideId);
}

export function getBlocks() {
  return [...blocks]; // Retorna uma cópia
}

export function setBlocks(newBlocks) {
  blocks = newBlocks;
  notifySubscribers('blocksUpdated');
}

export function getBlockById(blockId) {
  return blocks.find(b => b.id == blockId);
}

export function addSlide(newSlide, afterSlideId = null) {
  if (afterSlideId) {
    const currentIndex = slides.findIndex(s => s.id === afterSlideId);
    slides.splice(currentIndex + 1, 0, newSlide);
  } else {
    slides.push(newSlide);
  }
  notifySubscribers('slidesUpdated');
}

export function removeSlide(slideId) {
  slides = slides.filter(s => s.id !== slideId);
  notifySubscribers('slidesUpdated');
}

export function updateSlideData(slideId, data) {
  const slideIndex = slides.findIndex(s => s.id === slideId);
  if (slideIndex > -1) {
    slides[slideIndex] = { ...slides[slideIndex], ...data };
    notifySubscribers('slidesUpdated');
    if (slideId === currentSlideId) {
      notifySubscribers('currentSlideChanged'); // Notifica se o slide atual foi modificado
    }
  }
}

export function updateBlockData(blockId, payload) {
  const blockIndex = blocks.findIndex(b => b.id == blockId);
  if (blockIndex > -1) {
    blocks[blockIndex] = { ...blocks[blockIndex], payload };
    notifySubscribers('blocksUpdated');
  }
}

export function addBlock(newBlock) {
  blocks.push(newBlock);
  notifySubscribers('blocksUpdated');
}

export function removeBlock(blockId) {
  blocks = blocks.filter(b => b.id !== blockId);
  notifySubscribers('blocksUpdated');
}

// Observer pattern
export function subscribe(callback) {
  subscribers.push(callback);
}

function notifySubscribers(event) {
  subscribers.forEach(callback => callback(event));
}
