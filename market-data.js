// Данные для виджетов главной страницы: рыночные индексы и новости.
// Обновляется ВРУЧНУЮ еженедельно (по пятницам):
//   - SCFI — официальный источник Shanghai Shipping Exchange (sse.net.cn), публикуется по пятницам.
//   - Drewry WCI — drewry.co.uk, публикуется по четвергам.
//   - BDI — Baltic Exchange / TradingEconomics, публикуется ежедневно.
// Новости также обновляются вручную (тот же еженедельный прогон).
window.MARKET = {
  updated: "11.11.2026",
  indices: [
    {
      name: "SCFI",
      full: "Shanghai Containerized Freight Index",
      value: "3633.45",
      unit: "пункты",
      change: "−53.90 (−1.46%)",
      down: true,
      date: "06.11.2026"
    },
    {
      name: "Drewry WCI",
      full: "World Container Index",
      value: "$4 389",
      unit: "USD / 40ft",
      change: "−1% к пред. неделе",
      down: true,
      date: "05.11.2026"
    },
    {
      name: "BDI",
      full: "Baltic Exchange Dry Index",
      value: "2 862",
      unit: "пункты",
      change: "+0.28%",
      down: false,
      date: "10.11.2026"
    }
  ],
  news: [
    {
      title: "Эксперт: России необходимо строить ещё одну железную дорогу в Китай",
      src: "Trans.ru",
      date: "10.11.2026",
      url: "https://trans.ru/news/ekspert-rossii-neobhodimo-stroit-esche-odnu-zheleznuyu-dorogu-v-kitai"
    },
    {
      title: "В Казахстане хотят сделать обязательными электронные международные накладные",
      src: "Trans.ru",
      date: "10.11.2026",
      url: "https://trans.ru/news/v-kazahstane-hotyat-sdelat-obyazatelnimi-esche-i-elektronnie-mezhdunarodnie-nakladnie"
    },
    {
      title: "Атаки на танкеры у Ормузского пролива продолжаются",
      src: "Splash 247",
      date: "11.11.2026",
      url: "https://splash247.com/hormuz-tanker-attacks-mount/"
    },
    {
      title: "Панамский канал вновь увеличивает пропускную способность",
      src: "Splash 247",
      date: "11.11.2026",
      url: "https://splash247.com/panama-canal-turns-the-taps-back-on/"
    }
  ]
};
