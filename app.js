const KEY = 'habits';
let habits = JSON.parse(localStorage.getItem(KEY) || '[]');

function save() { localStorage.setItem(KEY, JSON.stringify(habits)); }

function render() {
  const ul = document.getElementById('list');
  ul.innerHTML = '';
  habits.forEach((h, i) => {
    const li = document.createElement('li');
    if (h.done) li.classList.add('done');
    li.innerHTML = `<input type="checkbox" ${h.done?'checked':''} data-i="${i}" /><span>${h.name}</span><button class="del" data-d="${i}">x</button>`;
    ul.appendChild(li);
  });
}

document.getElementById('addBtn').onclick = () => {
  const v = document.getElementById('habitInput').value.trim();
  if (!v) return;
  habits.push({ name: v, done: false });
  document.getElementById('habitInput').value = '';
  save(); render();
};

document.getElementById('list').onclick = e => {
  if (e.target.dataset.i !== undefined) {
    habits[e.target.dataset.i].done = e.target.checked;
    save(); render();
  }
  if (e.target.dataset.d !== undefined) {
    habits.splice(e.target.dataset.d, 1);
    save(); render();
  }
};

render();
