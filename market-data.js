// Рыночные индексы (обновляются вручную еженедельно).
// SCFI — sse.net.cn (пятница); Drewry WCI — drewry.co.uk (четверг); BDI — balticexchange.com (ежедневно).
window.MARKET = {
  updated: "20.11.2026",
  indices: [
    {
      name: "SCFI",
      full: "Shanghai Containerized Freight Index",
      value: "3503.78",
      unit: "пункты",
      change: "−68.55 (−1.92%)",
      shortChange: "−1.92%",
      down: true,
      date: "20.11.2026"
    },
    {
      name: "Drewry WCI",
      full: "World Container Index",
      value: "$4 176",
      unit: "USD / 40ft",
      change: "−3% к пред. неделе",
      shortChange: "−3%",
      down: true,
      date: "19.11.2026"
    },
    {
      name: "BDI",
      full: "Baltic Exchange Dry Index",
      value: "2 901",
      unit: "пункты",
      change: "−0.45%",
      shortChange: "−0.45%",
      down: true,
      date: "19.11.2026"
    }
  ]
};
