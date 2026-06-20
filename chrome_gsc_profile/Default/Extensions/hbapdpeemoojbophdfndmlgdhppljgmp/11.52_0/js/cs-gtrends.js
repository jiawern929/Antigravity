var Tool = (function(){

  var source = 'gtrend';

  var urlRE = new RegExp(/(trends\/explore|trends\/story|explore)/i);
  var observerTarget = 'body';
  var observer = null;

  var volBtnTimer = null;

  /** True when chart parent is new UI (no `.fe-line-chart`); synced in getChartParentNode. */
  var isGoogleTrendsNewDesign = false;

  /** Google Trends explore: legacy Angular pills vs newer UI. */
  var SEARCH_PILL_SELECTOR_NEW = 'div[data-type="Search term"]';
  var SEARCH_PILL_SELECTOR_LEGACY = '.search-term-wrapper ng-include';
  var getSearchPillRoots = function(){
    var $new = $(SEARCH_PILL_SELECTOR_NEW);
    if ($new.length) return $new;
    return $(SEARCH_PILL_SELECTOR_LEGACY);
  };

  var processReportTimer = null;
  var reportKeywordsList = [];

  var loadRelatedQueriesPermission = false;


  var init = function(){
    initPage();
    initURLChangeListener(function(){
      initPage();
    });
  };


  var initPage = function(){
    syncNewDesignGlobalFlag(false);
    $('.xt-gtrend-query').remove();
    // wait for table initialization
    checkTarget();
    var timer = setInterval(function(){
      var found = checkTarget();
      if (found) {
        clearInterval(timer);
      }
    }, 500);
    var pillsTimer = setInterval(function(){
      var found = $(SEARCH_PILL_SELECTOR_NEW)[0] || $(SEARCH_PILL_SELECTOR_LEGACY)[0];
      if (found) {
        clearInterval(pillsTimer);
        processKeywordPills();
      }
    }, 500);
  };


  var initURLChangeListener = function( cbProcessPage ){
    var url = document.location.href;
    var timer = setInterval(function(){
      if ( url !== document.location.href ) {
        url = document.location.href;
        cbProcessPage( url );
      }
    }, 1000);
  };


  var getPagePrefs = function(){
    var geo = getURLParameter('geo') || '';
    var date = getURLParameter('date') || '';
    var q = getURLParameter('q');
    var property = getURLParameter('gprop') || '';
    var category = getURLParameter('cat') || 0;
    var res = {};
    let mapping = {
      'All Time': ['all'],
      'All Time Yt': ['all_2008'],
      '5yrs': ['today 5-y'],
      // Legacy UI can emit empty `date` for past 12 months.
      '12mo': ['today 1-y', ''],
      '3mo': ['today 3-m'],
      '30d': ['today 1-m'],
      '7d': ['now 7-d'],
      '1d': ['now 1-d'],
      '4h': ['now 4-H'],
      '1h': ['now 1-H']
    };
    for (var key in mapping) {
      if (mapping[key].indexOf(date) !== -1) res.date = key.replace(' Yt', '');
    }
    if (date && !res.date) res.date = 'custom';
    'US GB CA AU IN NZ ZA'.split(' ').map(function(country){
      if (geo === country) {
        res.geo = country;
        if (country === 'GB') res.geo = 'UK';
      }
    });
    if (geo === '' || geo === 'Worldwide') res.geo = 'worldwide';
    res.property = property;
    res.category = category;
    return res;
  };


  var getURLParameter = function(sParam, useHash, url) {
    var location = window.location;
    if (url) location = new URL(url);
    var qs = location.search.substring(1);
    if (useHash) qs = location.hash.substring(1);
    qs = qs.split('+').join(' ');
    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;
    while (tokens = re.exec(qs)) {
      params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }
    return params[sParam];
  };


  var addLoadRelatedBtn = function(reportKeywordsList){
    var $secBtn = $('.xt-gtrends-related-btn');
    if ($secBtn[0]) $secBtn.remove();
    var $widgets = $('[id^=RELATED_QUERIES]');
    $widgets.map(function(i, widget){
      var $root = $(widget.parentNode);
      var $prependTo = $root.find('.pagination');
      if (!$prependTo[0]) $prependTo = $root.find('.pagination-container');
      $secBtn = $('<button>', {class: 'xt-gtrends-related-btn'}).prependTo($prependTo);
      $secBtn.text("Load Metrics (uses 25 credits)");
      $secBtn.click(function(e){
        e.preventDefault();
        e.stopPropagation();
        loadRelatedQueriesPermission = true;
        $('.xt-gtrends-related-btn').remove();
        processKeywords(reportKeywordsList, null);
      });

    });
  };


  var addSearchVolButtons = function(){
    var s = getPageSettings();
    var showButton = true;
    if (s.date !== 'Past 5 years' && s.date.indexOf(' - present') === -1) showButton = false;
    if (s.prop !== 'YouTube Search' && s.prop !== 'Web Search') showButton = false;
    var text = 'Get Trend Data in Bulk';
    if (s.prop === 'YouTube Search') {
      text = text.replace('2004', '2008');
    }
    var timerange = 'All Time';
    if (s.date === 'Past 5 years') {
      text = 'Get Trend Data in Bulk';
      timerange = '5yrs';
    }

    var $btn = $('#xt-gtrends-get-vol-main-btn');
    if ($btn[0]) $btn.remove();
    $btn = $('<button>', {
      id: 'xt-gtrends-get-vol-main-btn',
      class: 'compare-picker'
    }).appendTo('.compare-pickers ');
    $btn.text(text);
    $btn.toggleClass('xt-hidden', !showButton);
    $btn.click(function(e){
      e.preventDefault();
      var prop = s.prop === 'YouTube Search' ? 'youtube' : 'google';
      var termsStr = s.terms.join(',');
      var url = chrome.runtime.getURL(`html/page.html?page=trends&country=${s.country}&prop=${prop}&timerange=${timerange}&terms=${termsStr}`);
      chrome.runtime.sendMessage({
        cmd: 'new_tab',
        data: url
      });
    });

    // var $secBtn = $('.xt-gtrends-get-vol-sec-btn');
    // if ($secBtn[0]) $secBtn.remove();
    // var $widgets = $('[id^=RELATED_QUERIES]');
    // $widgets.map(function(i, widget){
    //   var $root = $(widget.parentNode);
    //   var $prependTo = $root.find('.pagination');
    //   if (!$prependTo[0]) $prependTo = $root.find('.pagination-container');
    //   $secBtn = $('<button>', {class: 'xt-gtrends-get-vol-sec-btn'}).prependTo($prependTo);
    //   $secBtn.text(text);
    //   $secBtn.toggleClass('xt-hidden', !showButton);
    //   $secBtn.click(function(e){
    //     e.preventDefault();
    //     var prop = s.prop === 'YouTube Search' ? 'youtube' : 'google';
    //     var termsStr = $root.find('[ng-bind="bidiText"]').map(function(j, node){
    //       return $(node).contents().get(0).nodeValue;
    //     }).toArray().join(',');
    //     var url = chrome.runtime.getURL(`html/page.html?page=trends&country=${s.country}&prop=${prop}&timerange=${timerange}&terms=${termsStr}`);
    //     chrome.runtime.sendMessage({
    //       cmd: 'new_tab',
    //       data: url
    //     });
    //   });
    // });

  };


  var getPageSettings = function(){
    var country = $.trim($('.compare-pickers [ng-model="ctrl.model.geo"]').text());
    var date = $.trim($('.compare-pickers custom-date-picker ._md-select-value').text());
    var prop = $.trim($('.compare-pickers [ng-model="ctrl.model.property"] ._md-select-value').text());
    var $termInputs = $(SEARCH_PILL_SELECTOR_NEW + ' input');
    if (!$termInputs.length) $termInputs = $('explore-search-term input');
    var terms = $termInputs.map(function(i, input){
      return input.value;
    }).toArray();
    return {country: country, date: date, prop: prop, terms: terms};
  };


  var checkTarget = function(){
    var $target = $( observerTarget );
    if (!$target.length) {
      return;
    }
    initMutationObserver( $target[0] );
    processChildList($('#RELATED_QUERIES').parent().find('.widget-template'), {});
    return true;
  };


  var initMutationObserver = function( target ){
    if (observer) observer.disconnect();
    observer = new MutationObserver(function(mutations) {
      if ( !document.location.href.match(urlRE) ) return;
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
          processChildList(mutation.addedNodes, mutation);
        }
      });
    });

    var config = {subtree: true, childList: true, characterData: true };
    observer.observe(target, config);
  };


  var processChildList = function(children, mutation){
    for (var i = 0, len = children.length; i < len; i++) {
      var node = children[i];
      var $node = $(node);
      if (node.id === 'report') {
        processReport( node );
      }
      else if ( $node.hasClass('widget-template') &&
                node.children &&
                $(node.children[0]).hasClass('fe-related-queries') ) {
        processReport( node );
      }
      else if (mutation.target && mutation.target.getAttribute('ng-bind') === 'bidiText' && mutation.addedNodes[0] && mutation.addedNodes[0].nodeType === Node.TEXT_NODE) {
        var $target = $(mutation.target);
        processReport($target.closest('.item'));
      }
    }
  };


  var chartParentClassName = 'xt-gtrends-chart-parent';

  var getNewDesignChartParentNode = function(){
    var heading = Array.from(document.querySelectorAll('h2, h3, [role="heading"]')).find(function(node){
      if (!node || !node.textContent) return false;
      var text = node.textContent.trim().toLowerCase();
      return text === 'interest over time' || text.indexOf('interest over time') === 0;
    });
    if (heading) {
      var jsControllerNode = heading.closest('div[jscontroller]');
      if (jsControllerNode && jsControllerNode.parentElement && jsControllerNode.parentElement.parentElement) {
        return jsControllerNode.parentElement.parentElement;
      }
    }
    var byJsname = document.querySelector('[jsname="kAWM8c"]');
    if (byJsname) {
      return byJsname;
    }
    return null;
  };


  var syncNewDesignGlobalFlag = function(value){
    isGoogleTrendsNewDesign = value;
    if (typeof window !== 'undefined') {
      window.__KE_GTRENDS_NEW_DESIGN__ = value;
    }
  };

  var getChartParentNode = function(){
    var legacyNode = $('.fe-line-chart')[0];
    if (legacyNode) {
      syncNewDesignGlobalFlag(false);
      return legacyNode;
    }
    var newDesignNode = getNewDesignChartParentNode();
    syncNewDesignGlobalFlag(!!newDesignNode);
    return newDesignNode;
  };


  var getChartParentSelector = function(){
    var parentNode = getChartParentNode();
    if (!parentNode) {
      return null;
    }
    $('.' + chartParentClassName).removeClass(chartParentClassName);
    parentNode.classList.add(chartParentClassName);
    return '.' + chartParentClassName;
  };


  const waitGoogleChartReady = function(opts){
    opts = opts || {};
    var timeoutMs = opts.timeoutMs != null ? opts.timeoutMs : 30000;
    return new Promise(function(resolve){
      var start = Date.now();
      var interval = setInterval(function(){
        var chartParent = getChartParentNode();
        if (chartParent) {
          clearInterval(interval);
          resolve(true);
          return;
        }
        if (Date.now() - start >= timeoutMs) {
          clearInterval(interval);
          resolve(false);
        }
      }, 200);
    });
  };

  var clearTrendChartLoadingUI = function(){
    $('#xt-trend-chart-root').remove();
  };

  /** Same selectors as getChartValues — payload is injected asynchronously by cs-gtrends-ajax (page world). */
  var chartPayloadTemplatesSel =
    'template[data-multiline], template[data-req], template[data-url]';
  var chartPayloadScriptsSel =
    'script[data-req], script[data-url], script[type="application/json"][data-req], script[type="application/json"][data-url]';

  function countChartPayloadNodes() {
    return $(chartPayloadTemplatesSel).length + $(chartPayloadScriptsSel).length;
  }

  /** Keyword API often returns before batchexecute finishes; poll until templates appear or timeout. */
  const waitForInjectedChartPayload = function (opts) {
    opts = opts || {};
    var timeoutMs = opts.timeoutMs != null ? opts.timeoutMs : 15000;
    var pollMs = opts.pollMs != null ? opts.pollMs : 100;
    return new Promise(function (resolve) {
      var start = Date.now();
      function tick() {
        var n = countChartPayloadNodes();
        if (n > 0) {
          resolve(true);
          return;
        }
        if (Date.now() - start >= timeoutMs) {
          resolve(false);
          return;
        }
        setTimeout(tick, pollMs);
      }
      tick();
    });
  };

  var showSpinner = function(){
    var rootId = 'xt-trend-chart-root';
    var $root = $('#' + rootId);
    var $parent = $(getChartParentNode());
    if (!$parent[0]) {
      return;
    }
    if (!$root[0]) {
      $root = $('<div>', {
        id: rootId,
        class: 'xt-ke-card'
      });
      if (!isGoogleTrendsNewDesign) {
        $parent.css({
          'overflow': 'auto',
          'height': 'auto'
        });
      }
      $parent.prepend($root);
    }
    $root.html('<img src="' + chrome.runtime.getURL('img/spinner32.gif') + '" style="vertical-align:middle"> Loading Keywords Everywhere Trend Chart');
  };


  var getChartValues = function(){
    // Legacy UI used to inject `template[data-multiline]`. New UI often injects only
    // `data-req` / `data-url`, so we need to be more permissive here.
    var $templates = $(chartPayloadTemplatesSel);

    // Some builds inject JSON into script tags; we can *read* them, but must not remove them.
    var $scripts = $(chartPayloadScriptsSel);

    var $nodes = $templates.add($scripts);
    var res = null;

    if ($nodes.length) {
      try {
        res = {};
        var last = null;
        $nodes.each(function () {
          if (this.getAttribute && (this.getAttribute('data-url') || this.getAttribute('data-req'))) last = this;
        });
        if (!last) last = $nodes[$nodes.length - 1];

        var rawText = (last.textContent || '').trim();
        // Handle common XSSI prefix used by Google endpoints.
        rawText = rawText.replace(/^\)\]\}'\s*\n/, '');
        res.json = JSON.parse(rawText);

        var dr = last.getAttribute && last.getAttribute('data-req');
        if (dr) {
          dr = dr.trim().replace(/^\)\]\}'\s*\n/, '');
          res.req = JSON.parse(dr);
        } else {
          var url = last.dataset && last.dataset.url;
          if (url) {
            var req = getURLParameter('req', false, url);
            if (req) {
              req = JSON.parse(decodeURIComponent(req));
              res.req = {request: req};
            }
          }
        }

        if (!res.json) res = null;
      } catch (e) {
        res = null;
      }
    }

    // Only remove injected templates; never remove script tags.
    $templates.remove();

    if (!res || !res.json) res = null;
    return res;
  };


  var processKeywordPills = async function(){
    var settings = Starter.getSettings();
    if (!settings.showChartsForGoogleTrends) {
      return;
    }
    var chartParentReady = await waitGoogleChartReady();
    if (!chartParentReady) {
      return;
    }
    var s = getPagePrefs();
    if (s.date === '1d' || s.date === '1h' || s.date === '4h' || s.date === 'custom') {
      return;
    }
    var hasCredits = Common.getCredits() > 0;
    var geo = s.geo;
    if (!geo) {
      return;
    }
    if (geo === 'worldwide') geo = '';
    var $chartParent = $(getChartParentNode());
    if ($chartParent.find('.widget-error-title')[0]) {
      return;
    }
    var pageQueries = [];
    var urlQueries = [];
    var promises = [];
    var q = getURLParameter('q') || '';
    // if (q && q.indexOf('/m/') !== -1) return;
    var qs = q ? q.split(',') : [];
    var nodes = [];
    var abort = false;
    getSearchPillRoots().map(function(i, node){
        var $node = $(node);
        var value = $node.find('input[type=search]').val();
        if (!value) value = $node.find('input').val();
        if (value.match(/^".*"$/)) abort = true;
        value = value.replace(/"/g, '');
        var urlValue = qs[i];
        urlQueries.push(urlValue);
        pageQueries.push(value.toLowerCase());
        nodes.push($node);
    });
    if (abort) return;
    var uniqQueries = pageQueries.filter(function(val, index){
      return pageQueries.indexOf(val) === index;
    });
    if (!uniqQueries.length) {
      return;
    }
    showSpinner();
    chrome.runtime.sendMessage({
      cmd: 'api.getKeywordData',
      data: {
        keywords: uniqQueries,
        country: geo,
        src: source
      }
    }, function( json ){
      (async function () {
        try {
          if (!json || !json.data) {
            clearTrendChartLoadingUI();
            return;
          }
          var dataByKeyword = {};
          var keys = Object.keys(json.data);
          for (var i = 0; i < keys.length; i++) {
            var row = json.data[keys[i]];
            if (row && row.keyword) dataByKeyword[row.keyword.toLowerCase()] = row;
          }
          // fighting with keywords with double quotes issue
          // reconstruct the json
          var clonedJSON = structuredClone(json);
          clonedJSON.data = [];
          var extra = {};
          for (var i = 0, len = nodes.length; i < len; i++) {
            var node = nodes[i];
            var keyword = pageQueries[i];
            var row = dataByKeyword[keyword];
            if (!row) {
              clearTrendChartLoadingUI();
              return;
            }
            clonedJSON.data.push(row);
            extra[keyword] = {vol: geo + ' Volume: ' + row.vol + '/mo'};
            // processQueryResponse(dataByKeyword[keyword], node, geo);
          }
          await waitForInjectedChartPayload({ timeoutMs: 15000, pollMs: 100 });
          var values = getChartValues();
          if (!values || !values.json) {
            clearTrendChartLoadingUI();
            return;
          }
          initTrendsChart({
            showVolume: hasCredits,
            extra: extra,
            queries: pageQueries,
            metrics: clonedJSON.data,
            chartData: values,
            geo: geo,
            timeRange: s.date,
            property: s.property,
            category: s.category
          });
        } catch (e) {
          clearTrendChartLoadingUI();
        }
      })();
    });
  };


  var processKeywordPill = function($node){
    var s = getPagePrefs();
    var hasCredits = Common.getCredits() > 0;
    var geo = s.geo;
    if (!geo) return;
    if (geo === 'worldwide') geo = '';
    var value = $node.find('input[type=search]').val();
    var metricsPromise = new Promise((resolve) => {
      chrome.runtime.sendMessage({
        cmd: 'api.getKeywordData',
        data: {
          keywords: [value],
          src: source
        }
      }, function( json ){
        if (!json || !json.data) return;
        processQueryResponse( json.data[0], $node, geo );
        resolve(json);
      });
    });
  };


  var processQueryResponse = function(data, $pill, geo){
    var $node = $pill.find('#xt-info');
    if (!$node.length) {
      $node = $('<div/>', {
          class: 'xt-gtrend-query'
        })
        .attr('id', 'xt-info');
      var $afterNode = $pill.find('input[type=search]');
      if (!$afterNode[0]) $afterNode = $pill.find('input');
      $node.insertAfter($afterNode);
    }
    if (!data) {
      Common.processEmptyData(json, $node);
      return;
    }
    else {
      if (data.vol != '-') {
        var html = geo + ' Volume: ' + data.vol + '/mo';
        $node.html(html);
      }
      else {
        $node.html('');
      }
    }
  };


  const initTrendsChart = (params) => {
    params.parentSelector = getChartParentSelector() || '.fe-line-chart';
    params.addFn = function($node){
      var $parent = $(params.parentSelector);
      if (!$parent[0]) {
        return;
      }
      if (!isGoogleTrendsNewDesign) {
        $parent.css({
          'overflow': 'auto',
          'height': 'auto'
        });
      }
      $parent.prepend($node);
    };
    params.parentClassName = 'xt-gtrends-trends-root';
    if (params.queries && params.queries.length === 1) {
      params.parentClassName = 'xt-gtrends-trends-single-root';
    }
    var query = params.query;
    if (!query) query = params.queries[0];
    params.rootId = 'xt-trend-chart-root';
    params.title = 'Trend Data';
    params.buttonCopy = 'Copy';
    params.buttonExport = 'Export';
    params.buttonScreenshot = 'Screenshot',
    params.source = source;
    params.darkMode = false;
    params.aspectRatio = 5;
    params.captcha = $('.g-recaptcha-response').val();
    params.hideIfNoData = true;
    params.maintainAspectRatio = true;
    TrendsChart.init(params);
  };


  var processReport = function( node ){
    // console.log(node);
    var $node = $(node);
    if ($node.closest('.geo-widget-wrapper, .multi-heat-map-widget')[0]) return;
    if ($node.closest('[widget-name="RELATED_TOPICS"]')[0]) return;
    var list = $node.find('.trends-bar-chart-name, .label-text span:first-child');
    for (var i = 0, len = list.length; i < len; i++) {
      if (list.find('.xt-gtrends-line')[0]) continue;
      var keyword = Common.cleanKeyword( list[i].textContent );
      reportKeywordsList.push({
        keyword: keyword,
        node: list[i]
      });
    }
    var hasCredits = Common.getCredits() > 0;
    if (hasCredits) {
      if (processReportTimer) clearTimeout(processReportTimer);
      processReportTimer = setTimeout(function(){
        processKeywords( reportKeywordsList, null );
      }, 200);
    }

    if (volBtnTimer) clearTimeout(volBtnTimer);
    volBtnTimer = setTimeout(function(){
      if (!loadRelatedQueriesPermission) {
        addLoadRelatedBtn(reportKeywordsList);
      }
      addSearchVolButtons();
    }, 100);
  };


  var processKeywords = function( keywordsList, table ){
    var keywords = {};
    for (var i = 0, len = keywordsList.length; i < len; i++) {
      keywords[ keywordsList[i].keyword ] = '';
      // if (!loadRelatedQueriesPermission) {
      //   var node = keywordsList[i].node;
      //   var $node = $(node);
      //   var $a = $('<a class="xt-gtrends-line">Load Metrics (uses 25 credits)</a>');
      //   if (!$node.find('.xt-gtrends-line')[0]) $node.append($a);
      //   $a.click(function(e){
      //     e.preventDefault();
      //     e.stopPropagation();
      //     loadRelatedQueriesPermission = true;
      //     $('.xt-gtrends-line').remove();
      //     processKeywords(keywordsList, table);
      //   });
      // }
    }
    if (!loadRelatedQueriesPermission) return;
    Common.processKeywords({
        keywords: Object.keys( keywords ),
        tableNode: table,
        src: source
      },
      function(json){
        processJSON( json, keywordsList );
        reportKeywordsList = [];
      }
    );
  };


  var processJSON = function( json, keywordsList ){
    var data = json.data;
    var dataByKeyword = {};
    for (var key in data) {
      var item = data[key];
      dataByKeyword[ item.keyword ] = item;
    }
    for (var i = 0, len = keywordsList.length; i < len; i++) {
      var keyword = keywordsList[i].keyword;
      var item = dataByKeyword[ keyword];
      if (item) {
        var title = Common.getResultStr(item);
        if (title) title = '[' + title + ']';
        var $res = $('<span/>').addClass('xt-gtrends-line').html(title);
        var color = Common.highlight(item);
        if (color) {
          $res.addClass('xt-highlight');
          $res.css('background', color);
        }
        // Common.appendStar($res, item);
        Common.addKeywords(keyword, item);
        Common.appendKeg($res, json, item);
        var $node = $( keywordsList[i].node );
        if ($node.find('.xt-gtrends-line')[0]) {
          $node.find('.xt-gtrends-line').remove();
        }
        $node.append( $res );
      }
    }
  };


  var getSource = function(){
    return source;
  };


  return {
    init: init,
    getSource: getSource,
    isGoogleTrendsNewDesign: function(){
      return isGoogleTrendsNewDesign;
    }
  };


})();
