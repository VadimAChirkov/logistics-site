// Рыночные индексы (обновляются вручную еженедельно).
// SCFI — sse.net.cn (пятница); Drewry WCI — drewry.co.uk (четверг); BDI — balticexchange.com (ежедневно).
window.MARKET = {
  updated: "27.11.2026",
  indices: [
    {
      name: "SCFI",
      full: "Shanghai Containerized Freight Index",
      value: "3569.54",
      unit: "пункты",
      change: "+65.76 (+1.88%)",
      shortChange: "+1.88%",
      down: false,
      date: "27.11.2026"
    },
    {
      name: "Drewry WCI",
      full: "World Container Index",
      value: "$4 032",
      unit: "USD / 40ft",
      change: "−3% к пред. неделе",
      shortChange: "−3%",
      down: true,
      date: "26.11.2026"
    },
    {
      name: "BDI",
      full: "Baltic Exchange Dry Index",
      value: "3 137",
      unit: "пункты",
      change: "−0.48%",
      shortChange: "−0.48%",
      down: true,
      date: "27.11.2026"
    }
  ]
};
