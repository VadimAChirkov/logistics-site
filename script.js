// Счётчик посещений
(function () {
  var el = document.getElementById('visit-counter');
  if (!el) return;
  fetch('/api/visit')
    .then(function (r) { return r.json(); })
    .then(function (d) { el.textContent = 'Посещений: ' + d.count; })
    .catch(function () { el.textContent = ''; });
})();

// Форма связи
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('contact-status');
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('cf-name').value.trim();
    var msg = document.getElementById('cf-message').value.trim();
    if (!msg) {
      status.textContent = 'Напишите сообщение.';
      status.style.color = '#b00020';
      return;
    }
    status.textContent = 'Отправка…';
    status.style.color = '#5c6672';
    fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name, message: msg })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok) {
          status.textContent = 'Спасибо! Сообщение отправлено.';
          status.style.color = '#1a7a3a';
          form.reset();
        } else {
          status.textContent = 'Не отправлено: ' + (d.error || 'ошибка');
          status.style.color = '#b00020';
        }
      })
      .catch(function () {
        status.textContent = 'Ошибка отправки. Попробуйте ещё раз.';
        status.style.color = '#b00020';
      });
  });
})();
