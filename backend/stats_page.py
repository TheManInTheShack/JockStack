# ------------------------------------------------------------------------------
# JockStack — /stats reporting page
# Returns a self-contained HTML page. Chart.js fetches data from /api/stats/*.
# ------------------------------------------------------------------------------

def render_stats_page() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>JockStack — Stats</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: Georgia, 'Times New Roman', serif;
      background: #1a1a2e;
      color: #e0e0e0;
      min-height: 100vh;
      padding: 2rem;
    }

    h1 {
      font-size: 2rem;
      color: #c8a96e;
      margin-bottom: 0.25rem;
    }

    .subtitle {
      color: #888;
      font-style: italic;
      margin-bottom: 2rem;
      font-size: 0.95rem;
    }

    /* Summary cards */
    .cards {
      display: flex;
      flex-wrap: wrap;
      gap: 1rem;
      margin-bottom: 2.5rem;
    }

    .card {
      background: #16213e;
      border: 1px solid #2a2a5a;
      border-radius: 8px;
      padding: 1.25rem 1.75rem;
      min-width: 160px;
      flex: 1;
    }

    .card .value {
      font-size: 2rem;
      font-weight: bold;
      color: #c8a96e;
      line-height: 1;
    }

    .card .label {
      font-size: 0.8rem;
      color: #888;
      margin-top: 0.4rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    /* Charts */
    .charts {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 1.5rem;
    }

    .chart-box {
      background: #16213e;
      border: 1px solid #2a2a5a;
      border-radius: 8px;
      padding: 1.5rem;
    }

    .chart-box h2 {
      font-size: 1rem;
      color: #c8a96e;
      margin-bottom: 1rem;
      font-weight: normal;
      letter-spacing: 0.03em;
    }

    .chart-box canvas {
      max-height: 280px;
    }

    .empty {
      color: #555;
      font-style: italic;
      font-size: 0.9rem;
      padding: 2rem 0;
      text-align: center;
    }

    a.home {
      display: inline-block;
      margin-bottom: 1.5rem;
      color: #c8a96e;
      text-decoration: none;
      font-size: 0.9rem;
    }
    a.home:hover { text-decoration: underline; }
  </style>
</head>
<body>

  <a class="home" href="/">&larr; Back to JockStack</a>
  <h1>JockStack Stats</h1>
  <p class="subtitle">Longitudinal data across all generated stacks</p>

  <!-- Summary cards -->
  <div class="cards">
    <div class="card"><div class="value" id="total-runs">—</div><div class="label">Total Runs</div></div>
    <div class="card"><div class="value" id="total-jocks">—</div><div class="label">Jocks Generated</div></div>
    <div class="card"><div class="value" id="avg-size">—</div><div class="label">Avg Stack Size</div></div>
    <div class="card"><div class="value" id="common-size">—</div><div class="label">Most Common Size</div></div>
    <div class="card"><div class="value" id="much-variants">—</div><div class="label">Much-Variants</div></div>
  </div>

  <!-- Charts -->
  <div class="charts">
    <div class="chart-box">
      <h2>Runs Over Time</h2>
      <canvas id="chart-runs"></canvas>
      <p class="empty" id="empty-runs" style="display:none">No data yet — generate some stacks first.</p>
    </div>
    <div class="chart-box">
      <h2>Stack Size Distribution</h2>
      <canvas id="chart-dist"></canvas>
      <p class="empty" id="empty-dist" style="display:none">No data yet.</p>
    </div>
    <div class="chart-box">
      <h2>Avg Name Length by Stack Size</h2>
      <canvas id="chart-names"></canvas>
      <p class="empty" id="empty-names" style="display:none">No data yet.</p>
    </div>
    <div class="chart-box">
      <h2>Much-Variant Count per Run</h2>
      <canvas id="chart-much"></canvas>
      <p class="empty" id="empty-much" style="display:none">No data yet.</p>
    </div>
  </div>

<script>
const GOLD   = 'rgba(200,169,110,0.85)';
const GOLD_B = 'rgba(200,169,110,1)';
const LINE   = 'rgba(100,180,255,0.85)';
const LINE_B = 'rgba(100,180,255,1)';
const GRID   = 'rgba(255,255,255,0.06)';
const TICK   = '#888';

const baseOpts = {
  responsive: true,
  plugins: { legend: { display: false } },
  scales: {
    x: { ticks: { color: TICK }, grid: { color: GRID } },
    y: { ticks: { color: TICK }, grid: { color: GRID }, beginAtZero: true },
  }
};

function show(canvasId, emptyId) {
  document.getElementById(canvasId).style.display = 'block';
  document.getElementById(emptyId).style.display = 'none';
}
function hide(canvasId, emptyId) {
  document.getElementById(canvasId).style.display = 'none';
  document.getElementById(emptyId).style.display = 'block';
}

// --- Summary cards ---
fetch('/api/stats/summary')
  .then(r => r.json())
  .then(d => {
    document.getElementById('total-runs').textContent   = d.total_runs.toLocaleString();
    document.getElementById('total-jocks').textContent  = d.total_jocks_generated.toLocaleString();
    document.getElementById('avg-size').textContent     = d.avg_stack_size;
    document.getElementById('common-size').textContent  = d.most_common_stack_size ?? '—';
    document.getElementById('much-variants').textContent = d.total_much_variants.toLocaleString();
  });

// --- Runs over time (last 100, grouped by date) ---
fetch('/api/stats/runs?limit=100')
  .then(r => r.json())
  .then(rows => {
    if (!rows.length) { hide('chart-runs', 'empty-runs'); return; }
    show('chart-runs', 'empty-runs');

    // Group by date
    const counts = {};
    rows.forEach(r => {
      const date = r.timestamp.slice(0, 10);
      counts[date] = (counts[date] || 0) + 1;
    });
    const labels = Object.keys(counts).sort();
    const data   = labels.map(k => counts[k]);

    new Chart(document.getElementById('chart-runs'), {
      type: 'line',
      data: {
        labels,
        datasets: [{ data, borderColor: LINE_B, backgroundColor: 'rgba(100,180,255,0.1)',
                      fill: true, tension: 0.3, pointRadius: 3 }]
      },
      options: baseOpts,
    });
  });

// --- Stack size distribution ---
fetch('/api/stats/distribution')
  .then(r => r.json())
  .then(rows => {
    if (!rows.length) { hide('chart-dist', 'empty-dist'); return; }
    show('chart-dist', 'empty-dist');

    new Chart(document.getElementById('chart-dist'), {
      type: 'bar',
      data: {
        labels: rows.map(r => r.stack_size),
        datasets: [{ data: rows.map(r => r.run_count),
                     backgroundColor: GOLD, borderColor: GOLD_B, borderWidth: 1 }]
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          x: { ...baseOpts.scales.x, title: { display: true, text: 'Stack Size', color: TICK } },
          y: { ...baseOpts.scales.y, title: { display: true, text: 'Runs', color: TICK } },
        }
      },
    });
  });

// --- Avg name length by stack size ---
fetch('/api/stats/name_lengths')
  .then(r => r.json())
  .then(rows => {
    if (!rows.length) { hide('chart-names', 'empty-names'); return; }
    show('chart-names', 'empty-names');

    new Chart(document.getElementById('chart-names'), {
      type: 'line',
      data: {
        labels: rows.map(r => r.stack_size),
        datasets: [{ data: rows.map(r => r.avg_name_length),
                     borderColor: GOLD_B, backgroundColor: 'rgba(200,169,110,0.1)',
                     fill: true, tension: 0.3, pointRadius: 3 }]
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          x: { ...baseOpts.scales.x, title: { display: true, text: 'Stack Size', color: TICK } },
          y: { ...baseOpts.scales.y, title: { display: true, text: 'Avg Name Length (chars)', color: TICK } },
        }
      },
    });
  });

// --- Much-variant count per run (last 100) ---
fetch('/api/stats/runs?limit=100')
  .then(r => r.json())
  .then(rows => {
    if (!rows.length) { hide('chart-much', 'empty-much'); return; }
    show('chart-much', 'empty-much');

    // Bucket by much_variant_count
    const counts = {};
    rows.forEach(r => {
      const k = r.much_variant_count;
      counts[k] = (counts[k] || 0) + 1;
    });
    const labels = Object.keys(counts).map(Number).sort((a,b) => a-b);

    new Chart(document.getElementById('chart-much'), {
      type: 'bar',
      data: {
        labels,
        datasets: [{ data: labels.map(k => counts[k]),
                     backgroundColor: LINE, borderColor: LINE_B, borderWidth: 1 }]
      },
      options: {
        ...baseOpts,
        scales: {
          ...baseOpts.scales,
          x: { ...baseOpts.scales.x, title: { display: true, text: 'Much-Variants in Run', color: TICK } },
          y: { ...baseOpts.scales.y, title: { display: true, text: 'Runs', color: TICK } },
        }
      },
    });
  });
</script>
</body>
</html>
"""
