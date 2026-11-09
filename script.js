// Автообновление года в футере
(function () {
  var els = document.querySelectorAll('#current-year');
  if (!els.length) return;
  var year = new Date().getFullYear();
  for (var i = 0; i < els.length; i++) els[i].textContent = year;
})();

// Форма связи (Formspree)
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('contact-status');
  var ENDPOINT = 'https://formspree.io/f/xkjjlpzw';
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('cf-name').value.trim();
    var email = document.getElementById('cf-email').value.trim();
    var msg = document.getElementById('cf-message').value.trim();
    var gotcha = document.getElementById('cf-company').value;
    if (gotcha) {
      // бот заполнил скрытое поле — молча игнорируем
      status.textContent = 'Спасибо! Сообщение отправлено.';
      status.style.color = '#1a7a3a';
      form.reset();
      return;
    }
    if (!msg) {
      status.textContent = 'Напишите сообщение.';
      status.style.color = '#b00020';
      return;
    }
    if (!email || email.indexOf('@') < 0) {
      status.textContent = 'Укажите корректный email.';
      status.style.color = '#b00020';
      return;
    }
    status.textContent = 'Отправка…';
    status.style.color = '#5c6672';
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ name: name, email: email, message: msg, _gotcha: gotcha })
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
