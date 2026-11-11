// Рыночные индексы (обновляются вручную еженедельно).
// SCFI — sse.net.cn (пятница); Drewry WCI — drewry.co.uk (четверг); BDI — balticexchange.com (ежедневно).
window.MARKET = {
  updated: "11.11.2026",
  indices: [
    {
      name: "SCFI",
      full: "Shanghai Containerized Freight Index",
      value: "3633.45",
      unit: "пункты",
      change: "−53.90 (−1.46%)",
      shortChange: "−1.46%",
      down: true,
      date: "06.11.2026"
    },
    {
      name: "Drewry WCI",
      full: "World Container Index",
      value: "$4 389",
      unit: "USD / 40ft",
      change: "−1% к пред. неделе",
      shortChange: "−1%",
      down: true,
      date: "05.11.2026"
    },
    {
      name: "BDI",
      full: "Baltic Exchange Dry Index",
      value: "2 862",
      unit: "пункты",
      change: "+0.28%",
      shortChange: "+0.28%",
      down: false,
      date: "10.11.2026"
    }
  ]
};
