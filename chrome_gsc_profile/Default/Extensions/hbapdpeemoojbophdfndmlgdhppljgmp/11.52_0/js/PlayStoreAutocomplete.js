/**
 * Google Play search suggestions (batchexecute rpc teXCtc).
 */
var PlayStoreAutocomplete = (function () {
  const RPC_ID = 'teXCtc';

  const stripXssi = (text) => {
    if (!text || typeof text !== 'string') return '';
    let s = text.trimStart();
    if (s.startsWith(")]}'")) s = s.slice(4).trimStart();
    return s;
  };

  /** Parse a top-level JSON array starting at `start`, respecting strings. */
  const parseJsonArrayAt = (s, start) => {
    if (!s || s[start] !== '[') return null;
    let depth = 0;
    let inStr = false;
    let esc = false;
    for (let i = start; i < s.length; i++) {
      const ch = s[i];
      if (inStr) {
        if (esc) esc = false;
        else if (ch === '\\') esc = true;
        else if (ch === '"') inStr = false;
        continue;
      }
      if (ch === '"') {
        inStr = true;
        continue;
      }
      if (ch === '[') depth++;
      else if (ch === ']') {
        depth--;
        if (depth === 0) {
          try {
            return { value: JSON.parse(s.slice(start, i + 1)), end: i + 1 };
          } catch (e) {
            return null;
          }
        }
      }
    }
    return null;
  };

  const parseLengthPrefixedChunks = (text) => {
    const s = stripXssi(text);
    const out = [];
    let pos = 0;
    while (pos < s.length) {
      while (pos < s.length && (s[pos] === '\n' || s[pos] === '\r' || s[pos] === ' ')) pos++;
      if (pos >= s.length) break;
      const lineStart = pos;
      while (pos < s.length && s[pos] !== '\n' && s[pos] !== '\r') pos++;
      const lenLine = s.slice(lineStart, pos).trim();
      if (!lenLine) break;
      if (!/^\d+$/.test(lenLine)) {
        const res = parseJsonArrayAt(s, lineStart);
        if (res) {
          out.push(res.value);
          pos = lineStart + res.end;
        }
        break;
      }
      const len = parseInt(lenLine, 10);
      if (pos < s.length && s[pos] === '\r') pos++;
      if (pos < s.length && s[pos] === '\n') pos++;
      const end = pos + len;
      let parsed = null;
      let nextPos = end;
      try {
        parsed = JSON.parse(s.slice(pos, end));
      } catch (e) {
        const res = parseJsonArrayAt(s, pos);
        if (res) {
          parsed = res.value;
          nextPos = pos + res.end;
        }
      }
      if (parsed) out.push(parsed);
      pos = parsed ? nextPos : end;
    }
    return out;
  };

  const collectSuggestionRows = (inner, out) => {
    if (!Array.isArray(inner)) return;
    const list = inner[0];
    if (!Array.isArray(list)) return;
    for (let i = 0; i < list.length; i++) {
      const row = list[i];
      if (Array.isArray(row) && typeof row[0] === 'string' && row[0]) {
        out.push({ keyword: row[0] });
      }
    }
  };

  const getWrbTeXCtcInner = (row) => {
    if (!Array.isArray(row) || row.length < 3) return null;
    const markerIdx = row.findIndex((cell) => cell === 'wrb.fr');
    if (markerIdx === -1) return null;
    const rpcIdx = row.findIndex((cell, idx) => idx > markerIdx && cell === RPC_ID);
    if (rpcIdx === -1) return null;
    for (let j = rpcIdx + 1; j < row.length; j++) {
      const cell = row[j];
      if (typeof cell === 'string' && cell.length) {
        try {
          return JSON.parse(cell);
        } catch (e) {}
      }
      if (Array.isArray(cell)) return cell;
    }
    return null;
  };

  const extractKeywordsFromNode = (node, out) => {
    if (node == null) return;
    if (!Array.isArray(node)) return;
    const inner = getWrbTeXCtcInner(node);
    if (inner) {
      collectSuggestionRows(inner, out);
      return;
    }
    for (let i = 0; i < node.length; i++) extractKeywordsFromNode(node[i], out);
  };

  const buildRequest = (params) => {
    const query = (params.query || '').trim();
    const sourcePath = params.sourcePath || '/store/games';
    const hl = params.hl || 'en';
    const rpcInner = JSON.stringify([null, [query], [10], [2, 1], 4]);
    const fReq = JSON.stringify([[[RPC_ID, rpcInner, null, 'generic']]]);
    const body = 'f.req=' + encodeURIComponent(fReq) + '&at=' + encodeURIComponent(params.at || '');
    let url =
      'https://play.google.com/_/PlayStoreUi/data/batchexecute?' +
      'rpcids=' + RPC_ID +
      '&source-path=' + encodeURIComponent(sourcePath) +
      '&hl=' + encodeURIComponent(hl) +
      '&authuser=0&soc-app=121&soc-platform=1&soc-device=1&rt=c' +
      '&_reqid=' + String(Math.floor(Math.random() * 1e6));
    if (params.fSid) url += '&f.sid=' + encodeURIComponent(params.fSid);
    if (params.bl) url += '&bl=' + encodeURIComponent(params.bl);
    return {
      url: url,
      headers: {
        Accept: '*/*',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'X-Same-Domain': '1',
        Origin: 'https://play.google.com',
        Referer: 'https://play.google.com/'
      },
      body: body
    };
  };

  const parseResponse = (text) => {
    try {
      const out = [];
      const chunks = parseLengthPrefixedChunks(text);
      for (let c = 0; c < chunks.length; c++) {
        extractKeywordsFromNode(chunks[c], out);
      }
      if (!out.length) {
        return { error: true, data: 'No suggestions' };
      }
      return { error: false, data: out };
    } catch (e) {
      return { error: true, data: 'Parse error' };
    }
  };

  return {
    RPC_ID: RPC_ID,
    buildRequest: buildRequest,
    parseResponse: parseResponse
  };
})();
