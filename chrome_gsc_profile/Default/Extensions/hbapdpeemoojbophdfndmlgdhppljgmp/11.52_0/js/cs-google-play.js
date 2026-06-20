var Tool = (function(){

  var source = 'gplsto';

  var inputSel = 'input[aria-autocomplete="list"][aria-label="Search Google Play"]';
  var inputTimer = null;
  var processPageTimer = null;
  var queryInfoPollTimer = null;
  var queryInfoPollMs = 500;
  var lastQueryRender = null;
  var suggestionsPollTimer = null;
  var suggestionsPollMs = 400;
  var suggestionsList = {};
  var cachedSuggestions = {};
  var lastSuggestionCacheKey = '';
  var pendingSuggestionKey = '';
  var isApplyingMetrics = false;


  var init = function(){
    $('body').addClass('xt-gplsto');
    setTimeout(function(){
      scheduleProcessPage(600);
      initURLChangeListener(scheduleProcessPage);
      initSearchInputListener();
      initSuggestions();
      initQueryInfoPoll();
    }, 500);
    var waitTimer = setInterval(function(){
      if ($(inputSel).length) {
        clearInterval(waitTimer);
        scheduleProcessPage(600);
      }
    }, 500);
  };


  var initURLChangeListener = function(cbProcessPage){
    var url = document.location.href;
    setInterval(function(){
      if (url !== document.location.href) {
        url = document.location.href;
        cbProcessPage();
      }
    }, 1000);
  };


  var initSearchInputListener = function(){
    $(document).on('input', inputSel, function(){
      if (inputTimer) clearTimeout(inputTimer);
      inputTimer = setTimeout(function(){
        scheduleProcessPage(700);
      }, 0);
      lastSuggestionCacheKey = '';
    });
  };


  var scheduleProcessPage = function(delay){
    if (processPageTimer) clearTimeout(processPageTimer);
    processPageTimer = setTimeout(function(){
      processPageTimer = null;
      processPage();
    }, typeof delay === 'number' ? delay : 400);
  };


  var cacheQueryRender = function(query, html, highlight){
    lastQueryRender = {
      query: Common.cleanKeyword(query),
      html: html,
      highlight: highlight || null
    };
  };


  var applyQueryInfoHtml = function(html, highlight){
    var $node = ensureInfoNode();
    if (!$node.length) return $();
    $node.show().html(html);
    if (highlight) {
      $node.addClass('xt-highlight').css(highlight);
    } else {
      $node.removeClass('xt-highlight').css({ background: '', color: '' });
    }
    return $node;
  };


  var isQueryInfoPlaced = function(){
    var $node = $('#xt-info');
    if (!$node.length || !$node[0].isConnected) return false;
    var $combo = getSearchCombobox();
    if (!$combo.length || !$combo[0].isConnected) return false;
    return $combo.next().is($node);
  };


  var queryInfoNeedsRender = function(){
    var query = Common.cleanKeyword(getQuery());
    if (!query) return false;
    if (!isQueryInfoPlaced()) return true;
    var $node = $('#xt-info');
    if (!$node.is(':visible')) return true;
    if (!$.trim($node.html())) return true;
    if (lastQueryRender && lastQueryRender.query === query && lastQueryRender.html !== $node.html()) {
      return true;
    }
    return false;
  };


  var restoreQueryInfo = function(){
    var query = Common.cleanKeyword(getQuery());
    if (!query) {
      hideQueryInfo();
      return;
    }
    if (lastQueryRender && lastQueryRender.query === query) {
      applyQueryInfoHtml(lastQueryRender.html, lastQueryRender.highlight);
      return;
    }
    scheduleProcessPage(0);
  };


  var scheduleQueryInfoRestore = function(){
    [350, 800, 1500].forEach(function(ms){
      setTimeout(function(){
        if (queryInfoNeedsRender()) restoreQueryInfo();
      }, ms);
    });
  };


  var pollQueryInfo = function(){
    if (!document.location.pathname.match(/^\/store\//)) return;
    var query = Common.cleanKeyword(getQuery());
    if (!query) {
      if ($('#xt-info').length) hideQueryInfo();
      return;
    }
    if (queryInfoNeedsRender()) restoreQueryInfo();
  };


  var initQueryInfoPoll = function(){
    if (queryInfoPollTimer) return;
    queryInfoPollTimer = setInterval(pollQueryInfo, queryInfoPollMs);
  };


  var getSearchInput = function(){
    return $(inputSel).first();
  };


  var getSuggestionKeyword = function(node){
    var $node = $(node);
    var text = $node.attr('data-display-text');
    if (!text) text = $.trim($node.find('a[href*="/store/search"]').first().text());
    if (!text) text = $.trim($node.text());
    return Common.cleanKeyword(text);
  };


  var getSuggestionTextHost = function($node){
    var $link = $node.find('a[href*="/store/search"]').first();
    if (!$link.length) return $node;
    var display = $.trim($node.attr('data-display-text') || '');
    if (display) {
      var $host = null;
      $link.find('div').each(function(){
        if ($.trim($(this).text()) === display) $host = $(this);
      });
      if ($host && $host.length) return $host;
    }
    var $bold = $link.find('div').has('b').last();
    if ($bold.length) return $bold;
    return $link.find('div').filter(function(){
      return $.trim($(this).text()).length > 0 && !$(this).find('i.google-material-icons').length;
    }).last();
  };


  var collectSuggestionsFromRoot = function($root){
    var list = {};
    var $scope = $root.is('[role="listbox"]') ? $root : $root.find('[role="listbox"]');
    if (!$scope.length) $scope = $root;
    $scope.find('[role="option"]').each(function(){
      var keyword = getSuggestionKeyword(this);
      if (keyword) list[keyword] = this;
    });
    return list;
  };


  var getLiveSuggestionsMap = function(){
    var $list = getSuggestionsListbox();
    if ($list.length) return collectSuggestionsFromRoot($list);
    return suggestionsList;
  };


  var allOptionsHaveMetrics = function(){
    var $list = getSuggestionsListbox();
    if (!$list.length) return false;
    var $options = $list.find('[role="option"]');
    if (!$options.length) return false;
    var complete = true;
    $options.each(function(){
      if (!$(this).find('.xt-suggestions-search').length) complete = false;
    });
    return complete;
  };


  var getSuggestionsListbox = function(){
    var $combo = getSearchCombobox();
    if (!$combo.length) return $();
    var listId = $combo.attr('aria-controls') || $combo.attr('aria-owns');
    if (listId) {
      var escId = (typeof CSS !== 'undefined' && CSS.escape) ? CSS.escape(listId) : listId;
      var $byId = document.getElementById(listId) ? $('#' + escId) : $();
      if ($byId.length && $byId.attr('role') === 'listbox') return $byId;
    }
    var $inCombo = $combo.find('[role="listbox"]').first();
    if ($inCombo.length) return $inCombo;
    return getSearchWiz().find('[role="listbox"]').first();
  };


  var isDropdownOpen = function(){
    var $combo = getSearchCombobox();
    return $combo.length && $combo.attr('aria-expanded') === 'true';
  };


  var getOptionsMissingMetrics = function($list){
    var missing = [];
    $list.find('[role="option"]').each(function(){
      if (!$(this).find('.xt-suggestions-search').length) missing.push(this);
    });
    return missing;
  };


  var pollSuggestions = function(){
    if (isApplyingMetrics) return;
    var settings = Starter.getSettings();
    if (!settings.showMetricsForSuggestions) return;
    if (!isDropdownOpen()) return;
    var $list = getSuggestionsListbox();
    if (!$list.length || !$list[0].isConnected) return;
    var list = collectSuggestionsFromRoot($list);
    if (!Object.keys(list).length) return;
    suggestionsList = list;
    if (!getOptionsMissingMetrics($list).length) return;
    processSuggestionsList(list);
  };


  var initSuggestions = function(){
    var settings = Starter.getSettings();
    if (!settings.showMetricsForSuggestions) return;
    if (suggestionsPollTimer) return;
    suggestionsPollTimer = setInterval(pollSuggestions, suggestionsPollMs);
    pollSuggestions();
  };


  var processSuggestionsList = function(list){
    if (!list) list = suggestionsList;
    for (var key in list) {
      if (!$(list[key]).is(':visible')) delete list[key];
    }
    var cacheKey = Object.keys(list).sort().join('|');
    if (!cacheKey) return;
    if (cacheKey === lastSuggestionCacheKey && allOptionsHaveMetrics()) {
      return;
    }
    if (cachedSuggestions[cacheKey]) {
      processSuggestionsListResponse(cachedSuggestions[cacheKey]);
      lastSuggestionCacheKey = cacheKey;
      return;
    }
    if (pendingSuggestionKey === cacheKey) return;
    pendingSuggestionKey = cacheKey;
    Common.processKeywords({
      keywords: Object.keys(list),
      tableNode: {},
      src: source
    }, function(json){
      pendingSuggestionKey = '';
      processSuggestionsListResponse(json);
      cachedSuggestions[cacheKey] = json;
      lastSuggestionCacheKey = cacheKey;
    });
  };


  var findKeywordNode = function(keywords, keyword){
    if (keywords[keyword]) return keywords[keyword];
    var lower = keyword.toLowerCase();
    for (var k in keywords) {
      if (k.toLowerCase() === lower) return keywords[k];
    }
    return null;
  };


  var processSuggestionsListResponse = function(json){
    if (!json || !json.data) return;
    isApplyingMetrics = true;
    var keywords = getLiveSuggestionsMap();
    var data = json.data;
    for (var key in data) {
      if (!Object.prototype.hasOwnProperty.call(data, key)) continue;
      var item = data[key];
      if (!item || !item.keyword) continue;
      var node = findKeywordNode(keywords, item.keyword);
      if (!node || !node.isConnected) continue;
      var $node = $(node);
      if ($node.find('.xt-suggestions-search').length) continue;
      var $span = $('<span/>').addClass('xt-suggestions-search');
      if (item.vol != '-' && item.vol != '0') {
        var html = Common.getResultStr(item);
        var color = Common.highlight(item);
        if (color) {
          $span.addClass('xt-highlight');
          $span.css({ background: color });
        }
        $span.html(html);
      }
      var $host = getSuggestionTextHost($node);
      $host.addClass('xt-gplsto-suggestion-text').append($span);
      $node.addClass('xt-gplsto-suggestion');
    }
    var $parent = getSuggestionsListbox();
    if ($parent.length) {
      var filename = 'googleplay-' + getQuery().replace(/\s+/g, '_') + '.csv';
      Common.addCopyExportButtons($parent[0], data, filename);
      $('#xt-suggestions-export').prependTo($parent);
    }
    isApplyingMetrics = false;
  };


  var getSearchWiz = function(){
    var $input = getSearchInput();
    if (!$input.length) return $();
    return $input.closest('c-wiz').first();
  };


  var getSearchCombobox = function(){
    var $input = getSearchInput();
    if (!$input.length) return $();
    var $box = $input.closest('[role="combobox"]');
    return $box.length ? $box.first() : $();
  };


  var syncInfoAlignment = function($node, $combo){
    if (!$node.length || !$combo.length) return;
    var cs = window.getComputedStyle($combo[0]);
    $node.css({
      marginLeft: cs.marginLeft,
      marginRight: cs.marginRight,
      marginInlineStart: cs.marginInlineStart,
      marginInlineEnd: cs.marginInlineEnd
    });
  };


  var getQuery = function(){
    var qs = new URLSearchParams(document.location.search);
    var fromUrl = qs.get('q');
    if (fromUrl) return $.trim(decodeURIComponent(fromUrl.replace(/\+/g, ' ')));
    return $.trim($(inputSel).first().val());
  };


  var scrapePlaySessionFromPage = function(){
    var html = document.documentElement.innerHTML;
    var at = '';
    var bl = '';
    var fSid = '';
    var mAt = html.match(/"SNlM0e"\s*:\s*"([^"]+)"/);
    if (mAt) at = mAt[1];
    var mBl = html.match(/"cfb2h"\s*:\s*"([^"]+)"/);
    if (mBl) bl = mBl[1];
    if (!bl) {
      var mBoq = html.match(/boq_playuiserver[^"'\\s&]+/);
      if (mBoq) bl = mBoq[0];
    }
    var mSid = html.match(/"FdrFJe"\s*:\s*(-?\d+)/);
    if (mSid) fSid = mSid[1];
    return { at: at, bl: bl, fSid: fSid };
  };


  var getPlayContext = function(){
    var path = document.location.pathname || '/store/games';
    var qs = new URLSearchParams(document.location.search);
    var catalog = qs.get('c') || 'apps';
    if (path.indexOf('/store/games') === 0) catalog = 'games';
    var hl = (document.documentElement.lang || 'en').split('-')[0];
    var session = scrapePlaySessionFromPage();
    return {
      sourcePath: path,
      hl: hl,
      catalog: catalog,
      at: session.at,
      bl: session.bl,
      fSid: session.fSid
    };
  };


  var ensureInfoNode = function(){
    var $wiz = getSearchWiz();
    if (!$wiz.length) return $();
    var $combo = getSearchCombobox();
    var $node = $('#xt-info');
    if (!$node.length) {
      $node = $('<div/>', {
        class: 'xt-gplsto-query'
      }).attr('id', 'xt-info');
    }
    if ($combo.length) {
      $combo.after($node);
      syncInfoAlignment($node, $combo);
    }
    else if (!$node.parent().is($wiz)) {
      $node.appendTo($wiz);
    }
    return $node;
  };


  var hideQueryInfo = function(){
    var $node = $('#xt-info');
    if (!$node.length) return;
    $node.empty().removeClass('xt-highlight').css({ background: '', color: '' }).hide();
    lastQueryRender = null;
  };


  var showLTKOnly = function(query){
    var settings = Starter.getSettings();
    if (!settings.showAutocompleteButton) {
      hideQueryInfo();
      return;
    }
    query = Common.cleanKeyword(query || getQuery());
    if (!query) {
      hideQueryInfo();
      return;
    }
    var $node = ensureInfoNode();
    if (!$node.length) return;
    var ctx = getPlayContext();
    var html = Common.appendLTKBtn('', {
      query: query,
      title: 'Find Google Play keywords for',
      service: 'googleplay',
      sourcePath: ctx.sourcePath,
      hl: ctx.hl,
      catalog: ctx.catalog,
      at: ctx.at,
      bl: ctx.bl,
      fSid: ctx.fSid
    });
    applyQueryInfoHtml(html, null);
    cacheQueryRender(query, html, null);
    scheduleQueryInfoRestore();
  };


  var processPage = function(){
    if (!document.location.pathname.match(/^\/store\//)) return;
    var query = Common.cleanKeyword(getQuery());
    if (!query) {
      hideQueryInfo();
      return;
    }
    if (lastQueryRender && lastQueryRender.query === query && lastQueryRender.html) {
      applyQueryInfoHtml(lastQueryRender.html, lastQueryRender.highlight);
      scheduleQueryInfoRestore();
    }
    chrome.runtime.sendMessage({
      cmd: 'api.getKeywordData',
      data: {
        keywords: [query],
        src: source
      }
    }, function(json){
      processQueryResponse(json);
      scheduleQueryInfoRestore();
    });
  };


  var processQueryResponse = function(json){
    var data;
    var settings = Starter.getSettings();
    if (json && json.error) {
      console.log('Error', json);
      return;
    }
    if (json && json.data) data = json.data[0];
    var $node = ensureInfoNode();
    if (!$node.length) return;
    var ctx = getPlayContext();
    if (!data) {
      if (json && (json.error_code === 'NOCREDITS' || json.error_code === 'NO_API_KEY')) {
        if (settings.showAutocompleteButton) {
          var html = Common.appendLTKBtn('', {
            query: getQuery(),
            title: 'Find Google Play keywords for',
            service: 'googleplay',
            sourcePath: ctx.sourcePath,
            hl: ctx.hl,
            catalog: ctx.catalog,
            at: ctx.at,
            bl: ctx.bl,
            fSid: ctx.fSid
          });
          applyQueryInfoHtml(html, null);
          cacheQueryRender(getQuery(), html, null);
        }
      }
      else if (json) {
        Common.processEmptyData(json, $node);
        cacheQueryRender(getQuery(), $node.html(), null);
      }
      else showLTKOnly(getQuery());
      return;
    }
    if (data.vol != '-') {
      Common.addKeywords(data.keyword);
      var html = Common.getResultStrType2(data);
      html = Common.appendStar(html, data);
      html = Common.appendKeg(html, json, data);
      if (settings.showAutocompleteButton) {
        html = Common.appendLTKBtn(html, {
          query: getQuery(),
          title: 'Find Google Play keywords for',
          service: 'googleplay',
          sourcePath: ctx.sourcePath,
          hl: ctx.hl,
          catalog: ctx.catalog,
          at: ctx.at,
          bl: ctx.bl,
          fSid: ctx.fSid
        });
      }
      var highlight = null;
      var color = Common.highlight(data);
      if (color) {
        highlight = {
          background: color,
          color: getContrastYIQ(color.replace('#', ''))
        };
      }
      applyQueryInfoHtml(html, highlight);
      cacheQueryRender(getQuery(), html, highlight);
    }
    else {
      showLTKOnly(getQuery());
    }
  };


  var getContrastYIQ = function(hexcolor){
    var r = parseInt(hexcolor.substr(0, 2), 16);
    var g = parseInt(hexcolor.substr(2, 2), 16);
    var b = parseInt(hexcolor.substr(4, 2), 16);
    var yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000;
    return (yiq >= 128) ? 'black' : 'white';
  };


  var getSource = function(){
    return source;
  };


  return {
    init: init,
    getSource: getSource
  };

})();
