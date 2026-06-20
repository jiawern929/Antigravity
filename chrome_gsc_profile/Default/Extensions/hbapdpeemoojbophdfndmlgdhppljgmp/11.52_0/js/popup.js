(function(){

  var settings = {};


  var init = function(){
    chrome.storage.local.get(null, function( data ){
      if (data.settings) {
        // checkMaintenance();
        initUI(data.settings);
      }
    });
  };


  var checkMaintenance = function(){
    chrome.runtime.sendMessage({
      cmd: 'api.isOnline'
    }, function(response){
      if (!response.data) {
        $('.maintenance-msg')
          .removeClass('hidden')
          .text(response.message);
      }
    });
  };


  var initUI = function(appSettings){
    settings = appSettings;
    chrome.runtime.sendMessage({cmd: 'api.getConfig'}, function(json){
      if (json.error) return;
      console.log(json);
      if (json.data && !json.data.showUrlMetrics) return;
      $('.feature-organic-domain, .feature-organic-url').removeClass('hidden');
    });

    if (!settings.apiKey) {
      $('#apiKeyWarning').show();
    }
    populateCountries(settings);
    $('#toggle-extension')[0].dataset.state = settings.enabled ? 'on' : 'off';
    document.body.dataset.state = settings.enabled ? 'on' : 'off';

    $('.toggle-button').click(function(){
      this.dataset.state = this.dataset.state === 'on' ? 'off' : 'on';
    });

    $('#toggle-extension').click(function(){
      chrome.runtime.sendMessage({
        cmd: 'app.setState',
        data: {
          state: this.dataset.state === 'on'
        }
      });
      document.body.dataset.state = this.dataset.state;
    });

    $('select').change(function(e){
      var id = this.id;
      if (id !== 'country') return;
      else settings[id] = $.trim(this.value);
      chrome.storage.local.set({settings: settings});
      chrome.runtime.sendMessage({cmd: 'settings.update'});
    });

    $('[data-page]').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      var page = this.dataset.page;
      chrome.tabs.create({
        url: '/html/page.html?page=' + page
      });
    });

    $('.analyze').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      var href = this.href;
      chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var url = tabs[0].url;
        if (!url.match(/^http/)) {
          alert('Please open a website to analyze before using this feature.');
          return;
        }
        var id = btoa(url);
        chrome.runtime.sendMessage({
          cmd: 'urlToAnalyze',
          data: {
            id: id,
            url: url
          }
        });
        setTimeout(function(){
          chrome.tabs.create({
            url: '/html/page.html?page=analyze&id=' + encodeURIComponent(id)
          });
        }, 50);
      });
    });

    $('.analyze-dom').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var tab = tabs[0];
        var url = tabs[0].url;
        var fn = function(){
          chrome.runtime.sendMessage({
            cmd: 'page.dom',
            data: {
              url: document.location.href,
              dom: document.documentElement.outerHTML
            }
          }, function(){});
        };
        chrome.scripting.executeScript({
          target: {tabId: tab.id},
          func: fn,
          args: []
        });
        var id = btoa(url);
        chrome.runtime.sendMessage({
          cmd: 'urlToAnalyze',
          data: {
            id: id,
            url: url
          }
        });
        setTimeout(function(){
          chrome.tabs.create({
            url: '/html/page.html?page=analyze&id=' + encodeURIComponent(id)
          });
        }, 50);
      });
    });

    $('.feature-direct-bulk-keywords').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      chrome.tabs.create({
        url: buildToolsUrl('search-volume-checker', {
          country: settings.country || '',
          dataSource: settings.dataSource || 'cli'
        })
      });
    });

    $('.feature-bulk-traffic-direct').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      chrome.tabs.create({
        url: 'https://keywordseverywhere.com/tools/website-traffic-checker/?apiKey=' + encodeURIComponent(settings.apiKey || '')
      });
    });

    $('.feature-organic-domain, .feature-organic-url').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      var isDomain = $(this).hasClass('feature-organic-domain');
      chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var pageUrl = tabs[0].url;
        if (!pageUrl.match(/^http/)) {
          alert('Please open a website to analyze before using this feature.');
          return;
        }
        var params = {country: settings.country || ''};
        if (isDomain) {
          params.domain = new URL(pageUrl).hostname;
        } else {
          params.url = pageUrl;
        }
        chrome.tabs.create({
          url: buildToolsUrl('organic-ranking-checker', params)
        });
      });
    });

    $('.feature-gap-direct').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      chrome.tabs.create({
        url: buildToolsUrl('keyword-gap-analysis', {
          country: settings.country || ''
        })
      });
    });

    $('.feature-toppages-direct').click(function(e){
      e.preventDefault();
      if (document.body.dataset.state === 'off') {
        showDisabledWarning();
        return;
      }
      chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var pageUrl = tabs[0].url;
        if (!pageUrl.match(/^http/)) {
          alert('Please open a website to analyze before using this feature.');
          return;
        }
        chrome.tabs.create({
          url: buildToolsUrl('top-pages-finder', {
            domain: new URL(pageUrl).hostname
          })
        });
      });
    });

    $('.feature-keywordkeg').click(function(e){
      e.preventDefault();
      var $this = $(this);
      var href = this.href + settings.apiKey;
      chrome.tabs.create({
        url: href
      });
    });

    injectIframe(settings);
  };


  var buildToolsUrl = function(toolPath, extraParams){
    var url = 'https://keywordseverywhere.com/tools/' + toolPath + '/?apiKey=' + encodeURIComponent(settings.apiKey || '');
    url += '&t=' + Date.now();
    if (extraParams) {
      for (var key in extraParams) {
        if (extraParams[key] === undefined || extraParams[key] === null) continue;
        url += '&' + key + '=' + encodeURIComponent(extraParams[key]);
      }
    }
    return url;
  };


  var showDisabledWarning = function(){
    $('#disabledWarning').removeClass('hidden');
    setTimeout(function(){
      $('#disabledWarning').addClass('hidden');
    }, 2000);
  };


  var injectIframe = function(params){
    var version = chrome.runtime.getManifest().version;
    var src = 'https://keywordseverywhere.com/ke/kepopup.php?apiKey=' + params.apiKey + '&version=' + version + '&t=' + Date.now() ;
    $('<iframe/>').attr('src', src).appendTo($('#iframe-root'));
  };


  var run = function(action){
    if (action === 'popup') return;
    else if (action === 'settings') {
      chrome.tabs.create({url: '/html/options.html'});
    }
    else if (action === 'manual') {
      chrome.tabs.create({
        url: buildToolsUrl('search-volume-checker', {
          country: settings.country || '',
          dataSource: settings.dataSource || 'cli'
        })
      });
    }
    else if (action === 'favorite') {
      chrome.tabs.create({url: 'https://keywordseverywhere.com/ke/3/favorites.php'});
    }
  };


  var populateCountries = function(settings){
    chrome.runtime.sendMessage({cmd: 'api.getCountries'}, function(json){
      if (!json || !Object.keys(json).length) {
        return;
      }
      for (var key in json) {
        var $option = $('<option/>')
          .attr('value', key)
          .text(json[key]);
        if (settings.country === key) $option.attr('selected', 'true');
        $option.appendTo($('#country'));
      }
    });
  };


  return {
    init: init
  };

})().init();
