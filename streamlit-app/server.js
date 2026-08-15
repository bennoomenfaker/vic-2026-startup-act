const express = require('express');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = process.env.PORT || 8082;

app.use(express.static(path.join(__dirname, 'public')));

const DATA = path.join(__dirname, '..', 'public', 'data');

app.get('/api/dashboard', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'dashboard_data.json'))));
});

app.get('/api/sessions', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'sessions.json'))));
});

app.get('/api/startups', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'database_startups.json'))));
});

app.get('/api/reports', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'annual_reports_parsed.json'))));
});

app.get('/api/analysis', (req, res) => {
  try {
    res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'analyse_quantitative_results.json'))));
  } catch { res.json({ error: 'not available' }); }
});

app.get('/api/corrections', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'corrections.json'))));
});

app.get('/api/parcours', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'parcours.json'))));
});

app.get('/api/startupblink', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'startupblink_tunisia.json'))));
});

app.get('/api/corrections-md', (req, res) => {
  const filepath = path.join(__dirname, '..', 'corrections.md');
  if (fs.existsSync(filepath)) {
    res.json({ filename: 'corrections.md', content: fs.readFileSync(filepath, 'utf8') });
  } else {
    res.status(404).json({ error: 'not found' });
  }
});

app.get('/api/livrables', (req, res) => {
  const dir = path.join(__dirname, '..', 'livrables');
  const files = fs.readdirSync(dir).filter(f => /\.(md|pdf|xlsx|docx)$/.test(f)).sort();
  res.json(files.map(f => ({ file: f, ext: path.extname(f) })));
});

app.get('/api/livrables/:filename', (req, res) => {
  const filepath = path.join(__dirname, '..', 'livrables', path.basename(req.params.filename));
  if (!fs.existsSync(filepath)) return res.status(404).json({ error: 'not found' });
  if (filepath.endsWith('.pdf')) return res.sendFile(filepath);
  if (filepath.endsWith('.xlsx') || filepath.endsWith('.docx')) return res.sendFile(filepath);
  res.json({ filename: path.basename(filepath), content: fs.readFileSync(filepath, 'utf8') });
});

app.get('/api/session-pdfs', (req, res) => {
  const dir = path.join(DATA, 'session-pdfs');
  res.json(fs.readdirSync(dir).filter(f => f.endsWith('.pdf')).sort());
});

app.get('/api/pdf-extracted', (req, res) => {
  res.json(JSON.parse(fs.readFileSync(path.join(DATA, 'session_pdfs_extracted.json'))));
});

app.get('/api/session-json', (req, res) => {
  const dir = path.join(DATA, 'session-pdfs-json');
  res.json(fs.readdirSync(dir).filter(f => f.endsWith('.json')).sort());
});

app.get('/api/session-json/:filename', (req, res) => {
  const filepath = path.join(DATA, 'session-pdfs-json', req.params.filename);
  if (fs.existsSync(filepath)) return res.json(JSON.parse(fs.readFileSync(filepath)));
  res.status(404).json({ error: 'JSON not found' });
});

app.get('/api/pdf-annual/:filename', (req, res) => {
  const filepath = path.join(DATA, req.params.filename);
  if (fs.existsSync(filepath)) return res.sendFile(filepath);
  const alt = path.join(__dirname, '..', 'public', req.params.filename);
  if (fs.existsSync(alt)) return res.sendFile(alt);
  res.status(404).json({ error: 'PDF not found' });
});

app.get('/api/pdf/:filename', (req, res) => {
  const filepath = path.join(DATA, 'session-pdfs', req.params.filename);
  if (fs.existsSync(filepath)) return res.sendFile(filepath);
  res.status(404).json({ error: 'PDF not found' });
});

app.listen(PORT, () => {
  console.log(`App running at http://localhost:${PORT}`);
});
