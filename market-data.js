// Рыночные индексы (обновляются вручную еженедельно).
// SCFI — sse.net.cn (пятница); Drewry WCI — drewry.co.uk (четверг); BDI — balticexchange.com (ежедневно).
window.MARKET = {
  updated: "13.11.2026",
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
      value: "$4 305",
      unit: "USD / 40ft",
      change: "−2% к пред. неделе",
      shortChange: "−2%",
      down: true,
      date: "12.11.2026"
    },
    {
      name: "BDI",
      full: "Baltic Exchange Dry Index",
      value: "3 020",
      unit: "пункты",
      change: "+2.06%",
      shortChange: "+2.06%",
      down: false,
      date: "12.11.2026"
    }
  ]
};
