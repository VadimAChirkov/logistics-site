// Локализация интерфейса (RU/EN)
window.L10N = (function () {
  var en = (document.documentElement.lang === 'en');
  return en ? {
    searchPlaceholder: 'Search…', searchAria: 'Search',
    voiceTitle: 'Voice search', empty: 'Nothing found',
    idxHeaders: ['Index', 'Value', 'Change', 'As of'],
    voiceLang: 'en-US',
    formThanks: 'Thank you! Your message has been sent.',
    formEmpty: 'Please write a message.',
    formBadEmail: 'Please enter a valid email.',
    formSending: 'Sending…',
    formNotSent: 'Not sent: ',
    formError: 'Sending failed. Please try again.'
  } : {
    searchPlaceholder: 'Поиск по сайту…', searchAria: 'Поиск по сайту',
    voiceTitle: 'Голосовой поиск', empty: 'Ничего не найдено',
    idxHeaders: ['Индекс', 'Значение', 'Изменение', 'На дату'],
    voiceLang: 'ru-RU',
    formThanks: 'Спасибо! Сообщение отправлено.',
    formEmpty: 'Напишите сообщение.',
    formBadEmail: 'Укажите корректный email.',
    formSending: 'Отправка…',
    formNotSent: 'Не отправлено: ',
    formError: 'Ошибка отправки. Попробуйте ещё раз.'
  };
})();

// Автообновление года в футере
(function () {
  var els = document.querySelectorAll('#current-year');
  if (!els.length) return;
  var year = new Date().getFullYear();
  for (var i = 0; i < els.length; i++) els[i].textContent = year;
})();

// Поиск по сайту (полнотекстовый, по индексу search-index.js)
(function () {
  var INDEX = (window.SEARCH_INDEX || []).map(function (e) {
    return { t: e.t, u: e.u, k: e.text };
  });

  var header = document.querySelector('.header-inner');
  if (!header) return;
  var S = window.L10N || {};

  var wrap = document.createElement('div');
  wrap.className = 'site-search';
  wrap.innerHTML = '<div class="site-search-box">' +
                   '<input type="search" id="site-search-input" placeholder="' + S.searchPlaceholder + '" autocomplete="off" aria-label="' + S.searchAria + '">' +
                   '<button type="button" id="site-search-mic" class="site-search-mic" title="' + S.voiceTitle + '" aria-label="' + S.voiceTitle + '">🎤</button>' +
                   '</div>' +
                   '<div id="site-search-results" class="site-search-results" hidden></div>';
  header.appendChild(wrap);

  var input = document.getElementById('site-search-input');
  var results = document.getElementById('site-search-results');
  var mic = document.getElementById('site-search-mic');
  if (!input || !results) return;

  function norm(s) { return (s || '').toLowerCase(); }

  function snippet(text, q) {
    var idx = text.toLowerCase().indexOf(q.toLowerCase());
    if (idx < 0) return text.slice(0, 140) + '…';
    var start = Math.max(0, idx - 40);
    var end = Math.min(text.length, idx + q.length + 100);
    return (start > 0 ? '…' : '') + text.slice(start, end) + (end < text.length ? '…' : '');
  }

  function render(q) {
    q = norm(q).trim();
    if (!q) { results.hidden = true; results.innerHTML = ''; return; }
    var terms = q.split(/\s+/);
    var hits = [];
    for (var i = 0; i < INDEX.length; i++) {
      var hay = norm(INDEX[i].t + ' ' + INDEX[i].k);
      var ok = true;
      for (var j = 0; j < terms.length; j++) {
        if (hay.indexOf(terms[j]) < 0) { ok = false; break; }
      }
      if (ok) hits.push(INDEX[i]);
    }
    if (!hits.length) {
      results.innerHTML = '<div class="site-search-empty">' + S.empty + '</div>';
    } else {
      var html = '';
      for (var h = 0; h < Math.min(hits.length, 8); h++) {
        html += '<a href="' + hits[h].u + '">' + hits[h].t + '</a>';
      }
      results.innerHTML = html;
    }
    results.hidden = false;
  }

  input.addEventListener('input', function () { render(input.value); });
  input.addEventListener('focus', function () { if (input.value) render(input.value); });
  document.addEventListener('click', function (e) {
    if (!wrap.contains(e.target)) results.hidden = true;
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { results.hidden = true; input.value = ''; }
  });

  // Голосовой поиск (Web Speech API; если браузер не поддерживает — кнопку скрываем)
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (mic && SR) {
    var rec = new SR();
    rec.lang = S.voiceLang || 'ru-RU';
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    rec.onresult = function (e) {
      var text = e.results[0][0].transcript;
      if (text) { input.value = text; render(text); }
    };
    rec.onerror = function () { mic.classList.remove('listening'); };
    rec.onend = function () { mic.classList.remove('listening'); };
    mic.addEventListener('click', function () {
      if (mic.classList.contains('listening')) {
        try { rec.stop(); } catch (err) {}
        mic.classList.remove('listening');
      } else {
        try { rec.start(); } catch (err) {}
        mic.classList.add('listening');
      }
    });
  } else if (mic) {
    mic.style.display = 'none';
  }
})();

// Виджеты главной страницы: рыночные индексы и новости (данные из market-data.js)
(function () {
  if (!window.MARKET) return;
  var M = window.MARKET;

  // Компактная строка индексов под шапкой (вверху справа)
  var strip = document.getElementById('indices-strip');
  if (strip && M.indices && M.indices.length) {
    var parts = [];
    for (var s = 0; s < M.indices.length; s++) {
      var x = M.indices[s];
      var xc = x.down ? 'scfi-delta-down' : 'scfi-delta-up';
      parts.push('<span class="idx-item"><strong>' + x.name + '</strong> ' + x.value +
        ' <span class="' + xc + '">' + x.shortChange + '</span></span>');
    }
    strip.innerHTML = parts.join('<span class="idx-sep">·</span>');
  }

  // Рыночные индексы (таблица)
  var idxBox = document.getElementById('indices-widget');
  if (idxBox && M.indices && M.indices.length) {
    var S = window.L10N || {};
    var hd = S.idxHeaders || ['Индекс', 'Значение', 'Изменение', 'На дату'];
    var rows = '';
    for (var i = 0; i < M.indices.length; i++) {
      var d = M.indices[i];
      var cls = d.down ? 'scfi-delta-down' : 'scfi-delta-up';
      rows += '<tr>' +
        '<td><strong>' + d.name + '</strong><br><span class="scfi-meta">' + d.full + '</span></td>' +
        '<td><strong>' + d.value + '</strong> <span class="scfi-meta">' + d.unit + '</span></td>' +
        '<td class="' + cls + '">' + d.change + '</td>' +
        '<td class="scfi-meta">' + d.date + '</td>' +
        '</tr>';
    }
    idxBox.innerHTML = '<table><thead><tr><th>' + hd[0] + '</th><th>' + hd[1] + '</th><th>' + hd[2] + '</th><th>' + hd[3] + '</th></tr></thead><tbody>' + rows + '</tbody></table>';
  }
  var updEl = document.getElementById('market-updated');
  if (updEl) updEl.textContent = M.updated;

  // Новости
  var newsBox = document.getElementById('news-widget');
  var newsData = window.NEWS;
  if (newsBox && newsData && newsData.items && newsData.items.length) {
    var html = '<ul class="news-list">';
    for (var j = 0; j < newsData.items.length; j++) {
      var n = newsData.items[j];
      html += '<li><a href="' + n.url + '" target="_blank" rel="noopener noreferrer">' + n.title + '</a>' +
              '<span class="news-src">' + n.src + ' · ' + n.date + '</span></li>';
    }
    html += '</ul>';
    newsBox.innerHTML = html;
    var newsUpd = document.getElementById('news-updated');
    if (newsUpd && newsData.updated) newsUpd.textContent = newsData.updated;
  }
})();

// Форма связи (Formspree)
(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var status = document.getElementById('contact-status');
  var T = window.L10N;
  var ENDPOINT = 'https://formspree.io/f/xkjjlpzw';
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('cf-name').value.trim();
    var email = document.getElementById('cf-email').value.trim();
    var msg = document.getElementById('cf-message').value.trim();
    var gotcha = document.getElementById('cf-company').value;
    if (gotcha) {
      // бот заполнил скрытое поле — молча игнорируем
      status.textContent = T.formThanks;
      status.style.color = '#1a7a3a';
      form.reset();
      return;
    }
    if (!msg) {
      status.textContent = T.formEmpty;
      status.style.color = '#b00020';
      return;
    }
    if (!email || email.indexOf('@') < 0) {
      status.textContent = T.formBadEmail;
      status.style.color = '#b00020';
      return;
    }
    status.textContent = T.formSending;
    status.style.color = '#5c6672';
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({ name: name, email: email, message: msg, _gotcha: gotcha })
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok) {
          status.textContent = T.formThanks;
          status.style.color = '#1a7a3a';
          form.reset();
        } else {
          status.textContent = T.formNotSent + (d.error || 'error');
          status.style.color = '#b00020';
        }
      })
      .catch(function () {
        status.textContent = T.formError;
        status.style.color = '#b00020';
      });
  });
})();
