(() => {
  if (window.__KE_GTRENDS_AJAX_HOOKED__) return;
  window.__KE_GTRENDS_AJAX_HOOKED__ = true;

  const ajaxDebugPrefix = '[KE gtrends ajax]';
  /**
   * Legacy batchexecute uses this exact string as the first cell of a wrapper row.
   * It is Google's internal wire marker
   */
  const WRB_LEGACY_SERIES_WRAPPER_TAG = 'trap';
  let logBatchexecuteMissCount = 0;
  let logMultilineMissCount = 0;
  let logXhrSkippedTypeCount = 0;
  let logTrendsResponseCount = 0;

  function stripXssPrefix(text) {
    if (!text || typeof text !== 'string') return '';
    let s = text.trimStart();
    if (s.startsWith(")]}'")) s = s.slice(4).trimStart();
    return s;
  }

  /** Index in `s` after consuming `byteLen` UTF-8 bytes starting at `start`, or -1 if incomplete / misaligned. */
  function indexAfterUtf8Bytes(s, start, byteLen) {
    let i = start;
    let used = 0;
    while (used < byteLen) {
      if (i >= s.length) return -1;
      const cp = s.codePointAt(i);
      let n;
      if (cp <= 0x7f) n = 1;
      else if (cp <= 0x7ff) n = 2;
      else if (cp <= 0xffff) n = 3;
      else n = 4;
      if (used + n > byteLen) return -1;
      used += n;
      i += cp > 0xffff ? 2 : 1;
    }
    return i;
  }

  /**
   * One batchexecute body chunk: JSON bytes, usually prefixed by a UTF-8 byte length.
   * The declared length can include trailing CRLF, disagree with copy/pasted samples, or
   * use code-unit counts on ASCII-only payloads — fall back to scanning for the next
   * line that is only digits (the following chunk's length line).
   */
  function consumeLpChunkJson(s, pos, declaredLen) {
    const endUtf8 = indexAfterUtf8Bytes(s, pos, declaredLen);
    if (endUtf8 >= 0) {
      try {
        return { value: JSON.parse(s.slice(pos, endUtf8)), next: endUtf8 };
      } catch (e1) {}
    }
    if (pos + declaredLen <= s.length) {
      try {
        return { value: JSON.parse(s.slice(pos, pos + declaredLen)), next: pos + declaredLen };
      } catch (e2) {}
    }
    const from = pos;
    let scan = pos;
    while (scan < s.length) {
      const nl = s.indexOf('\n', scan);
      if (nl === -1) {
        const tail = s.slice(from).trim();
        if (tail.length) {
          try {
            return { value: JSON.parse(tail), next: s.length };
          } catch (e4) {}
        }
        break;
      }
      const lineEnd = s.indexOf('\n', nl + 1);
      if (lineEnd === -1) {
        const maybeLen = s.slice(nl + 1).replace(/\r$/, '').trim();
        if (/^\d+$/.test(maybeLen)) {
          scan = nl + 1;
          continue;
        }
        const jsonStr = s.slice(from, nl);
        try {
          return { value: JSON.parse(jsonStr), next: s.length };
        } catch (e5) {
          scan = nl + 1;
          continue;
        }
      }
      let lenOnly = s.slice(nl + 1, lineEnd);
      if (lenOnly.charAt(lenOnly.length - 1) === '\r') lenOnly = lenOnly.slice(0, -1);
      lenOnly = lenOnly.trim();
      if (!/^\d+$/.test(lenOnly)) {
        scan = nl + 1;
        continue;
      }
      const jsonStr = s.slice(from, nl);
      try {
        const value = JSON.parse(jsonStr);
        return { value, next: nl + 1 };
      } catch (e3) {
        scan = nl + 1;
      }
    }
    return null;
  }

  function parseLengthPrefixedChunks(text) {
    const s = stripXssPrefix(text);
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
        try {
          out.push(JSON.parse(s.slice(lineStart)));
        } catch (e2) {}
        break;
      }
      const len = parseInt(lenLine, 10);
      if (pos < s.length && s[pos] === '\r') pos++;
      if (pos < s.length && s[pos] === '\n') pos++;
      const got = consumeLpChunkJson(s, pos, len);
      if (!got) break;
      out.push(got.value);
      pos = got.next;
    }
    return out;
  }

  function isWrbFrToken(v) {
    return v === 'wrb.fr' || (typeof v === 'string' && v.trim() === 'wrb.fr');
  }

  /**
   * Batchexecute rows are usually `['wrb.fr', id, jsonString, ...]` but newer payloads may use
   * extra columns, different order, or wrap structures in objects — scan after the marker for the
   * first cell that parses as JSON.
   */
  function parseMaybeDoubleEncodedJson(str) {
    let v = JSON.parse(str);
    while (typeof v === 'string') {
      try {
        v = JSON.parse(v);
      } catch (e) {
        break;
      }
    }
    return v;
  }

  /** Parsed structure inside a wrb.fr row (object/array), or null. */
  function getWrbRowInnerParsed(row) {
    if (!Array.isArray(row) || row.length < 2) return null;
    const markerIdx = row.findIndex(isWrbFrToken);
    if (markerIdx === -1) return null;
    for (let j = markerIdx + 1; j < row.length; j++) {
      const cell = row[j];
      if (cell != null && typeof cell === 'object') return cell;
      if (typeof cell === 'string' && cell.length) {
        try {
          return parseMaybeDoubleEncodedJson(cell);
        } catch (e) {}
      }
    }
    return null;
  }

  function walkFindWrbRows(node, acc) {
    if (node == null) return;
    const t = typeof node;
    if (t === 'string' || t === 'number' || t === 'boolean') return;
    if (Array.isArray(node)) {
      if (getWrbRowInnerParsed(node)) acc.push(node);
      for (let i = 0; i < node.length; i++) walkFindWrbRows(node[i], acc);
      return;
    }
    if (t === 'object') {
      for (const k in node) {
        if (Object.prototype.hasOwnProperty.call(node, k)) walkFindWrbRows(node[k], acc);
      }
    }
  }

  function isLegacyWrbSeriesWrapperRow(n) {
    if (!Array.isArray(n) || n.length <= 4 || !Array.isArray(n[4])) return false;
    const tag = n[0];
    return (
      tag === WRB_LEGACY_SERIES_WRAPPER_TAG ||
      (typeof tag === 'string' && tag.trim() === WRB_LEGACY_SERIES_WRAPPER_TAG)
    );
  }

  /** Older payloads wrap the point list in a row whose first cell is WRB_LEGACY_SERIES_WRAPPER_TAG. */
  function findWrappedSeriesPointArrays(inner) {
    const out = [];
    function walk(n) {
      if (n == null) return;
      if (Array.isArray(n)) {
        if (isLegacyWrbSeriesWrapperRow(n)) {
          out.push(n[4]);
          return;
        }
        for (let i = 0; i < n.length; i++) walk(n[i]);
        return;
      }
      if (typeof n === 'object') {
        for (const k in n) {
          if (Object.prototype.hasOwnProperty.call(n, k)) walk(n[k]);
        }
      }
    }
    walk(inner);
    return out;
  }

  function isTimelinePointRow(row) {
    return (
      Array.isArray(row) &&
      row.length >= 5 &&
      typeof row[0] === 'number' &&
      typeof row[1] === 'number' &&
      Array.isArray(row[2]) &&
      Array.isArray(row[2][0]) &&
      row[2][0].length === 1 &&
      Array.isArray(row[2][1]) &&
      row[2][1].length === 1 &&
      typeof row[2][0][0] === 'number' &&
      typeof row[2][1][0] === 'number'
    );
  }

  function timelinePointRowsToPoints(rows) {
    const pts = [];
    if (!Array.isArray(rows)) return pts;
    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      if (!isTimelinePointRow(row)) continue;
      pts.push({
        start: row[2][0][0],
        end: row[2][1][0],
        value: row[1],
        isPartial: !!row[3]
      });
    }
    return pts;
  }

  /**
   * Current batchexecute often nests series as `[[["<any keyword>",null,null,56,[row,row,...]]]]`
   * where each `row` matches isTimelinePointRow. Collect every homogeneous point row list.
   */
  function collectHomogeneousTimelineSeries(inner) {
    const out = [];
    function walk(n) {
      if (n == null) return;
      if (Array.isArray(n)) {
        if (n.length > 0 && n.every(function (item) { return isTimelinePointRow(item); })) {
          const pts = timelinePointRowsToPoints(n);
          if (pts.length) out.push(pts);
          return;
        }
        for (let i = 0; i < n.length; i++) walk(n[i]);
        return;
      }
      if (typeof n === 'object') {
        for (const k in n) {
          if (Object.prototype.hasOwnProperty.call(n, k)) walk(n[k]);
        }
      }
    }
    walk(inner);
    return out;
  }

  function inferResolutionFromPoints(points) {
    if (!points || points.length < 2) return 'WEEK';
    const steps = [];
    for (let i = 1; i < points.length; i++) steps.push(points[i].start - points[i - 1].start);
    steps.sort((a, b) => a - b);
    const med = steps[Math.floor(steps.length / 2)] || 86400;
    if (med >= 86400 * 25) return 'MONTH';
    return 'WEEK';
  }

  function formatTimeRange(start, end) {
    const a = new Date(start * 1000);
    const b = new Date(end * 1000);
    if (start === end) {
      return a.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' });
    }
    return (
      a.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' }) +
      ' – ' +
      b.toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
    );
  }

  function mergeSeriesToTimeline(allPointSeries) {
    if (!allPointSeries.length) return null;
    const count = allPointSeries.length;
    const timeMap = new Map();
    for (let si = 0; si < count; si++) {
      const pts = allPointSeries[si];
      for (let j = 0; j < pts.length; j++) {
        const p = pts[j];
        const k = p.start;
        if (!timeMap.has(k)) {
          timeMap.set(k, {
            end: p.end,
            value: new Array(count).fill(null),
            partial: false
          });
        }
        const slot = timeMap.get(k);
        slot.value[si] = p.value;
        slot.partial = slot.partial || p.isPartial;
        slot.end = p.end;
      }
    }
    const starts = Array.from(timeMap.keys()).sort((a, b) => a - b);
    const timelineData = starts.map(function (start) {
      const slot = timeMap.get(start);
      return {
        time: start,
        formattedTime: formatTimeRange(start, slot.end),
        value: slot.value.map(function (v) {
          return v == null ? 0 : v;
        }),
        isPartial: slot.partial,
        hasData: slot.value.map(function (v) {
          return v != null;
        })
      };
    });
    let resolution = 'WEEK';
    if (allPointSeries.length === 1 && allPointSeries[0].length >= 2) {
      resolution = inferResolutionFromPoints(allPointSeries[0]);
    } else if (starts.length >= 2) {
      const step = starts[1] - starts[0];
      resolution = step >= 86400 * 25 ? 'MONTH' : 'WEEK';
    }
    return { timelineData: timelineData, resolution: resolution };
  }

  function tryNormalizeBatchexecute(text) {
    if (!text || text.indexOf('wrb.fr') === -1) return null;
    const chunks = parseLengthPrefixedChunks(text);
    const wbRows = [];
    for (let c = 0; c < chunks.length; c++) {
      walkFindWrbRows(chunks[c], wbRows);
    }
    if (!wbRows.length) return null;
    const allSeriesPoints = [];
    for (let w = 0; w < wbRows.length; w++) {
      let inner;
      try {
        inner = getWrbRowInnerParsed(wbRows[w]);
        if (!inner) continue;
      } catch (e) {
        continue;
      }
      const homog = collectHomogeneousTimelineSeries(inner);
      if (homog.length) {
        for (let h = 0; h < homog.length; h++) {
          if (homog[h].length) allSeriesPoints.push(homog[h]);
        }
      } else {
        const wrapped = findWrappedSeriesPointArrays(inner);
        for (let t = 0; t < wrapped.length; t++) {
          const pts = timelinePointRowsToPoints(wrapped[t]);
          if (pts.length) allSeriesPoints.push(pts);
        }
      }
    }
    if (!allSeriesPoints.length) return null;
    const merged = mergeSeriesToTimeline(allSeriesPoints);
    if (!merged || !merged.timelineData.length) return null;
    return {
      json: { default: { timelineData: merged.timelineData } },
      req: { request: { resolution: merged.resolution } }
    };
  }

  function appendChartTemplate(url, jsonObj, reqFromBatchexecute, source) {
    const str = JSON.stringify(jsonObj);
    JSON.parse(str);
    const node = document.createElement('template');
    node.setAttribute('data-multiline', '');
    if (url) node.setAttribute('data-url', url);
    if (reqFromBatchexecute) node.setAttribute('data-req', JSON.stringify(reqFromBatchexecute));
    node.textContent = str;
    document.body.appendChild(node);
    if (window.__KE_GTRENDS_DEBUG__ || window.__KE_GTRENDS_AJAX_DEBUG__) {
      const timelinePoints =
        jsonObj &&
        jsonObj.default &&
        Array.isArray(jsonObj.default.timelineData)
          ? jsonObj.default.timelineData.length
          : 0;
      console.log(ajaxDebugPrefix, 'chart payload appended', {
        source: source || 'unknown',
        hasUrl: !!url,
        hasReq: !!reqFromBatchexecute,
        timelinePoints: timelinePoints
      });
    }
  }

  function stripMultilineBody(responseText) {
    let body = responseText.trimStart();
    if (!body.startsWith(")]}'")) return body;
    body = body.slice(4).trimStart();
    return body;
  }

  function parseMultilineJson(responseText) {
    let body = stripMultilineBody(responseText);
    try {
      return JSON.parse(body);
    } catch (e1) {}
    try {
      const legacy = responseText.trimStart();
      if (legacy.startsWith(")]}'")) {
        return JSON.parse(legacy.slice(5).trim());
      }
    } catch (e2) {}
    const chunks = parseLengthPrefixedChunks(responseText);
    for (let i = 0; i < chunks.length; i++) {
      const ch = chunks[i];
      if (ch && ch.default && Array.isArray(ch.default.timelineData)) return ch;
    }
    return null;
  }

  function maybeCaptureMultiline(url, responseText) {
    if (!responseText || url.indexOf('/multiline') === -1) return;
    try {
      const jsonObj = parseMultilineJson(responseText);
      if (!jsonObj || !jsonObj.default || !Array.isArray(jsonObj.default.timelineData)) {
        if (logMultilineMissCount < 3) {
          logMultilineMissCount++;
          console.warn(ajaxDebugPrefix, 'multiline: could not extract timeline', url.slice(0, 120));
        }
        return;
      }
      appendChartTemplate(url, jsonObj, null, 'multiline');
    } catch (e) {}
  }

  function isTrendsBatchexecuteUrl(url) {
    if (!url || url.indexOf('trends.google') === -1) return false;
    return url.indexOf('/_/TrendsUi/data/batchexecute') !== -1 || url.indexOf('TrendsUi/data/batchexecute') !== -1;
  }

  function maybeCaptureBatchexecute(url, responseText) {
    if (!responseText || !isTrendsBatchexecuteUrl(url)) return;
    const norm = tryNormalizeBatchexecute(responseText);
    if (!norm) {
      if (logBatchexecuteMissCount < 3) {
        logBatchexecuteMissCount++;
        console.warn(ajaxDebugPrefix, 'batchexecute: could not parse timeline', url.slice(0, 120));
      }
      return;
    }
    appendChartTemplate(null, norm.json, norm.req, 'batchexecute');
  }

  function onNetworkResponse(url, responseText) {
    if (
      window.__KE_GTRENDS_AJAX_DEBUG__ &&
      url &&
      url.indexOf('trends.google') !== -1 &&
      logTrendsResponseCount < 30
    ) {
      logTrendsResponseCount++;
      const looksBatchexecute = isTrendsBatchexecuteUrl(url);
      const looksMultiline = url.indexOf('/multiline') !== -1;
      if (looksBatchexecute || looksMultiline) {
        console.log(ajaxDebugPrefix, 'trends response observed', {
          looksBatchexecute,
          looksMultiline,
          url: url.slice(0, 200),
          bodyLen: responseText.length
        });
      }
    }
    maybeCaptureBatchexecute(url, responseText);
    maybeCaptureMultiline(url, responseText);
  }

  const xhr = XMLHttpRequest.prototype;
  const send = xhr.send;
  xhr.send = function () {
    const self = this;
    this.addEventListener('load', function () {
      const url = self.responseURL || '';
      if (self.responseType !== '' && self.responseType !== 'text') {
        if (
          window.__KE_GTRENDS_AJAX_DEBUG__ &&
          logXhrSkippedTypeCount < 12 &&
          url &&
          (isTrendsBatchexecuteUrl(url) || url.indexOf('/multiline') !== -1)
        ) {
          logXhrSkippedTypeCount++;
          console.log(ajaxDebugPrefix, 'XHR body skipped (responseType not text)', {
            responseType: self.responseType,
            url: url.slice(0, 160)
          });
        }
        return;
      }
      const text = self.responseText;
      if (!text) return;
      onNetworkResponse(url, text);
    });
    return send.apply(this, arguments);
  };

  const origFetch = window.fetch;
  window.fetch = function () {
    const input = arguments[0];
    const url = typeof input === 'string' ? input : (input && input.url) || '';
    const p = origFetch.apply(this, arguments);
    if (!url || (url.indexOf('/multiline') === -1 && !isTrendsBatchexecuteUrl(url))) {
      return p;
    }
    return p.then(function (response) {
      try {
        response
          .clone()
          .text()
          .then(function (text) {
            onNetworkResponse(url, text);
          })
          .catch(function () {});
      } catch (e) {}
      return response;
    });
  };
  if (window.__KE_GTRENDS_DEBUG__ || window.__KE_GTRENDS_AJAX_DEBUG__) {
    console.log(ajaxDebugPrefix, 'XHR/fetch hooks installed (page world)');
  }
})();
