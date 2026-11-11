// Автообновление года в футере
(function () {
  var els = document.querySelectorAll('#current-year');
  if (!els.length) return;
  var year = new Date().getFullYear();
  for (var i = 0; i < els.length; i++) els[i].textContent = year;
})();

// Поиск по сайту (клиентский, по локальному индексу)
(function () {
  var INDEX = [
    { t: "Главная", u: "index.html", k: "главная логистика международная вэд" },
    { t: "Инкотермс 2020", u: "incoterms.html", k: "инкотермс incoterms базис поставки exw fob cif dap ddp fca" },
    { t: "Морские перевозки", u: "sea-freight.html", k: "море морские перевозки фрахт коносамент конвенции" },
    { t: "Коносамент (B/L)", u: "documents-sea.html", k: "коносамент bill of lading bl коносамент морской документ" },
    { t: "Морские конвенции", u: "regulations-sea.html", k: "конвенции гаагские висби гамбургские роттердамские solas imdg ктм" },
    { t: "Фрахтование", u: "chartering.html", k: "фрахтование чартер проформа дженкон тайм-чартер рейсовый" },
    { t: "Техника фрахтовых операций", u: "chartering-technique.html", k: "фрахтовые операции рекап сталия демередж диспач" },
    { t: "Фрахтовые сокращения", u: "chartering-abbreviations.html", k: "сокращения аббревиатуры фрахт словарь" },
    { t: "Ж/д перевозки", u: "rail-freight.html", k: "железнодорожные перевозки жд смгс гу накладная" },
    { t: "Ж/д перевозочные документы", u: "documents-rail.html", k: "смгс гу накладная железнодорожная этран" },
    { t: "Ж/д соглашения и правила", u: "regulations-rail.html", k: "смгс цим cotif отиф осжд устав железнодорожного" },
    { t: "Коммерческий акт и Акт общей формы", u: "railway-acts.html", k: "коммерческий акт общей формы акт претензия недостача порча" },
    { t: "Негабаритные и тяжеловесные грузы", u: "railway-oversized.html", k: "негабаритные тяжеловесные дч-1835 индекс негабаритности габарит погрузки" },
    { t: "Авиаперевозки", u: "air-freight.html", k: "авиа авиаперевозки воздушные грузовые" },
    { t: "Авиадокументы (AWB)", u: "documents-air.html", k: "авианакладная awb air waybill авиа" },
    { t: "Авиа конвенции", u: "regulations-air.html", k: "варшавская монреальская чикагская iata icao авиа" },
    { t: "Автоперевозки", u: "road-freight.html", k: "авто автоперевозки дорожные грузовые" },
    { t: "Автодокументы (CMR, ТН, ЭТрН)", u: "documents-road.html", k: "cmr транспортная накладная тн электронная этран адр" },
    { t: "Авто конвенции", u: "regulations-road.html", k: "cmr tir мдп адр допуск правила перевозок авто" },
    { t: "Опасные грузы", u: "dangerous-goods.html", k: "опасные грузы классы опасности оон un классификация msds паспорт безопасности material safety data sheet ghs 16 разделов химическая продукция" },
    { t: "Опасные грузы: авто (ДОПОГ)", u: "dangerous-goods-road.html", k: "допог adr опасные грузы авто водитель свидетельство" },
    { t: "Опасные грузы: ж/д (ППОГ, ЦМ-407)", u: "dangerous-goods-rail.html", k: "ппог смгс опасные грузы жд аварийная карточка цм-407" },
    { t: "Опасные грузы: море (IMDG)", u: "dangerous-goods-sea.html", k: "imdg опасные грузы море декларация группа упаковки" },
    { t: "Опасные грузы: авиа (IATA)", u: "dangerous-goods-air.html", k: "iata dgr опасные грузы авиа литиевые батареи" },
    { t: "UCP-600", u: "ucp600.html", k: "ucp 600 аккредитив документарный банк" },
    { t: "Глоссарий", u: "glossary.html", k: "глоссарий термины словарь определения логистика" },
    { t: "Литература и источники", u: "literature.html", k: "литература источники документы приказы конвенции" },
    { t: "О себе", u: "about.html", k: "о себе автор специалист" },
    { t: "Связаться", u: "contact.html", k: "связаться контакты форма связь" },
    { t: "Правовая информация", u: "disclaimer.html", k: "правовая информация дисклеймер" }
  ];

  var header = document.querySelector('.header-inner');
  if (!header) return;

  var wrap = document.createElement('div');
  wrap.className = 'site-search';
  wrap.innerHTML = '<input type="search" id="site-search-input" placeholder="Поиск по сайту…" autocomplete="off" aria-label="Поиск по сайту">' +
                   '<div id="site-search-results" class="site-search-results" hidden></div>';
  header.appendChild(wrap);

  var input = document.getElementById('site-search-input');
  var results = document.getElementById('site-search-results');
  if (!input || !results) return;

  function norm(s) { return (s || '').toLowerCase(); }

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
      results.innerHTML = '<div class="site-search-empty">Ничего не найдено</div>';
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
    idxBox.innerHTML = '<table><thead><tr><th>Индекс</th><th>Значение</th><th>Изменение</th><th>На дату</th></tr></thead><tbody>' + rows + '</tbody></table>';
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
