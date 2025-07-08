// renderer.js - handles UI interactions for Hamster Water Pet

const hamster = document.getElementById('hamster');
const controls = document.getElementById('controls');
const waterCountLabel = document.getElementById('waterCount');
const drinkBtn = document.getElementById('drinkBtn');
const bottleSlider = document.getElementById('bottleSlider');
const bottleImg = document.getElementById('bottle');

// Persisted daily total (simple localStorage for now)
let count = parseInt(localStorage.getItem('waterIntake') || '0', 10);
updateLabel();

// --- Click hamster to reveal controls ---
hamster.addEventListener('click', () => {
  controls.style.display = controls.style.display === 'none' ? 'block' : 'none';
});

// --- Drink button ---
drinkBtn.addEventListener('click', () => {
  count += 1;
  saveAndUpdate();
});

// --- Slider to add up to 10 cups ---
bottleSlider.addEventListener('change', (e) => {
  const val = parseInt(e.target.value, 10);
  if (val > 0) {
    count += val;
    e.target.value = 0; // reset slider
    saveAndUpdate();
  }
});

// --- Drag-and-drop bottle image onto hamster ---
bottleImg.addEventListener('dragstart', (e) => {
  e.dataTransfer.setData('text/plain', 'water');
});

hamster.addEventListener('dragover', (e) => {
  e.preventDefault();
});

hamster.addEventListener('drop', (e) => {
  e.preventDefault();
  const data = e.dataTransfer.getData('text/plain');
  if (data === 'water') {
    count += 1;
    saveAndUpdate();
  }
});

function saveAndUpdate() {
  localStorage.setItem('waterIntake', String(count));
  updateLabel();
}

function updateLabel() {
  waterCountLabel.textContent = `Water intake: ${count} cup${count !== 1 ? 's' : ''}`;
}

// Reset at midnight (simple check every minute)
setInterval(() => {
  const now = new Date();
  if (now.getHours() === 0 && now.getMinutes() === 0) {
    count = 0;
    saveAndUpdate();
  }
}, 60000);
