var Tool = (function(){

  var source = 'claude';

  var rootSel = '.header__search';
  var observer;
  var suggestionsTimer;
  var suggestionsList = {};
  var cachedSuggestions = {};
  var darkMode = false;
  var buttonRetryTimer = null;


  var init = async function(){
    await formReady();
    setTimeout(checkPendingRequests, 1000);
    addWidgetButton();
    startButtonRetry();
    initBodyClassObserver();
    initWindowMessaging();
    initMutationObserver(document.body);
    var settings = Starter.getSettings();
    if (settings.showChatGPTactions) {
      addPersuasions();
    }
    initURLChangeListener(function(){
      addWidgetButton();
    })
  };


  const formReady = function(){
    return new Promise(resolve => {
      let attempt = 10;
      let timer = setInterval(() => {
        if (attempt-- <= 0) {
          clearInterval(timer);
          resolve();
        }
        let div = document.querySelector('fieldset div[contenteditable="true"]');
        if (div) {
          resolve(div);
          clearInterval(timer);
        }
      }, 500);
    });
  };


  const headerReady = function(){
    return new Promise(resolve => {
      let attempt = 100;
      let timer = setInterval(() => {
        if (attempt-- <= 0) {
          clearInterval(timer);
          resolve();
        }
        let div = document.querySelector('[data-testid="menu-sidebar"]');
        if (div) {
          resolve(div);
          clearInterval(timer);
        }
      }, 600);
    });
  };


  var checkPendingRequests = function(){
    let limit = 39000;
    chrome.runtime.sendMessage({
      cmd: 'yt.transcript.summarize.get'
    }, function(data){
      if (!data) return;
      let points = data.text.length > 2000 ? 10 : 5;
      let prompt = `Summarize the transcript of a YouTube video in ${points} bullet points. The video is by ${data.channelName} and is titled ${data.title}. The entire transcript is given below.\n` + data.text;
      prompt = prompt.substr(0, limit);
      chooseTemplate({
        prompt: prompt
      });
    });
    chrome.runtime.sendMessage({
      cmd: 'prompt_pending.get'
    }, function(prompt){
      if (!prompt) return;
      prompt = prompt.substr(0, limit);
      chooseTemplate({
        prompt: prompt
      });
    });
  };


  var initBodyClassObserver = function(){
    const doc = document.documentElement;
    const onClassChange = (mutationsList) => {
      for (const mutation of mutationsList) {
        if (mutation.type === 'attributes' && mutation.attributeName === 'data-mode') {
          OpenaiWidgetController.post('darkmode', isDarkMode());
        }
      }
    };
    const observer = new MutationObserver(onClassChange);
    observer.observe(doc, { attributes: true, attributeFilter: ['data-mode'] });
  };


  var initMutationObserver = function( target ){
    if (observer) observer.disconnect();
    observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(mutation) {
        if (mutation.type === 'childList') {
          if (!mutation.addedNodes.length) return;
          for (var i = 0, len = mutation.addedNodes.length; i < len; i++) {
            var node = mutation.addedNodes[i];
            // console.log(node);
            if (node.nodeType === Node.ELEMENT_NODE && (
              node.querySelector('[data-testid="chat-controls"]') ||
              node.querySelector('[data-testid="page-header"]') ||
              node.querySelector('[data-testid="main-content"]') ||
              node.querySelector('[data-testid="wiggle-controls-actions"]') ||
              node.querySelector('[data-testid="wiggle-controls-actions-share"]') ||
              node.matches && node.matches('header[data-testid="page-header"]')
            )) {
              addWidgetButton();
            }
          }
        }
      });
    });
    var config = { subtree: true, childList: true};
    observer.observe(target, config);
  };


  var initWindowMessaging = function(){
    // console.log('initWindowMessaging');
    window.addEventListener("message", function(event){
      var payload = event.data;
      if (typeof payload !== 'object') return;
      var cmd = payload.cmd;
      var data = payload.data;
      if (!cmd) return;
      if (cmd === 'xt.resize') {
        var height = data.height;
        var source = data.source;
        var selector = '#xt-openai-widget';
        if (source === 'claude_sidebar') selector = '#xt-claude-sidebar-iframe';
        if (!selector) return;
        if (height <= 0) return;
        $(selector + ' iframe').height(height + 10);
      }
      else if (cmd === 'xt-openai-choose-template') {
        chooseTemplate(data);
      }
      else if (cmd === 'xt-openai-get-settings') {
        OpenaiWidgetController.post('settings', {
          plan: Common.getPlan(),
          credits: Common.getCredits(),
          settings: Starter.getSettings()
        });
      }
    }, false);
  };


  var chooseTemplate = async function(data){
    const $form = $('fieldset');
    if ($form[0]) {
      let $textarea = $form.find('div[contenteditable="true"]');
      $textarea[0].innerHTML = '<p>' + data.prompt.replace(/\n/g, '</p><p>') + '</p>';
      $textarea[0].dispatchEvent(new Event('input', {bubbles: true}));
      setTimeout(function(){
        let $button = $form.find('button[aria-label="Send message"]');
        $button.removeAttr('disabled').click();
      }, 500);
    }
  };


  var getMainContent = function(){
    return $('[data-testid="main-content"], #main-content, main').first();
  };


  var getHeaderActionsContainer = function(){
    var header = document.querySelector('header[data-testid="page-header"]');
    if (!header) return $();
    var actions = header.querySelector('div.right-3.flex');
    if (actions) return $(actions);
    var rows = header.querySelectorAll(':scope > div.flex');
    for (var i = rows.length - 1; i >= 0; i--) {
      var right = rows[i].querySelector('div.right-3, div.flex.gap-2');
      if (right) return $(right);
    }
    return $();
  };


  var getChatsButton = function(){
    return $('[aria-label="Chats"]').first();
  };


  var startButtonRetry = function(){
    if (buttonRetryTimer) return;
    var attempts = 0;
    buttonRetryTimer = setInterval(function(){
      attempts++;
      addWidgetButton();
      if (($('.xt-claude-btn')[0] || $('.xt-claude-btn-sec')[0]) && attempts >= 3) {
        clearInterval(buttonRetryTimer);
        buttonRetryTimer = null;
      }
      if (attempts >= 40) {
        clearInterval(buttonRetryTimer);
        buttonRetryTimer = null;
      }
    }, 1000);
  };


  var logoSvg = function(darkmode){
    var svg = LOGO_SVG;
    if (!darkmode) svg = svg.replace(/#fff/g, '#000');
    return svg;
  };


  var sidebarMenuItemTemplate = function(darkmode){
    return `
    <div class="relative group xt-claude-btn" data-state="closed"><a target="_self" class="inline-flex
      items-center
      justify-center
      relative
      shrink-0
      can-focus
      select-none
      disabled:pointer-events-none
      disabled:opacity-50
      disabled:shadow-none
      disabled:drop-shadow-none text-text-300
              border-transparent
              transition
              font-styrene
              duration-300
              ease-[cubic-bezier(0.165,0.85,0.45,1)]
              hover:bg-bg-400
              aria-pressed:bg-bg-400
              aria-checked:bg-bg-400
              aria-expanded:bg-bg-300
              hover:text-text-100
              aria-pressed:text-text-100
              aria-checked:text-text-100
              aria-expanded:text-text-100 h-9 px-4 py-2 rounded-lg min-w-[5rem] active:scale-[0.985] whitespace-nowrap text-sm w-full hover:bg-bg-300 overflow-hidden !min-w-0 group active:bg-bg-400 active:scale-[0.99] px-4" aria-label="Templates" href="#"><div class="-translate-x-2 w-full flex flex-row items-center justify-start gap-3"><div class="size-4 flex items-center justify-center group-hover:!text-text-200 text-text-400">${logoSvg(darkmode)}</div><span class="truncate group-hover:[mask-image:linear-gradient(to_right,hsl(var(--always-black))_78%,transparent_95%)] text-sm whitespace-nowrap w-full [mask-size:100%_100%]"><div class="transition-all duration-200">Templates</div></span></div></a><div class="absolute right-0 top-1/2 -translate-y-1/2 hidden group-hover:block"></div></div>
            `;
  };


  var headerBtnTemplate = function(darkmode){
    return `
      <button type="button" data-cds="Button" data-size="sm" class="xt-claude-btn-sec cds-reset group/btn relative isolate inline-flex shrink-0 items-center justify-center gap-1.5 whitespace-nowrap select-none border-0 outline-none rounded h-control font-sans text-body font-medium text-primary px-md" aria-label="Templates">
        <span aria-hidden="true" class="absolute -z-[1] rounded-[inherit] transition-colors duration-fast group-focus-visible/btn:shadow-[inset_0_0_0_1px_var(--cds-page-bg)] bg-fill-secondary group-hover/btn:bg-fill-secondary-hover group-aria-expanded/btn:bg-fill-secondary-hover inset-0 group-aria-pressed/btn:bg-accent group-hover/btn:group-aria-pressed/btn:bg-accent cds-btn-squish shadow-field"></span>
        <span class="inline-flex items-center gap-1 ">
          <span class="size-4 flex items-center justify-center">${logoSvg(darkmode)}</span>
          <span>Templates</span>
        </span>
      </button>
    `;
  };


  var addSidebarButton = function(){
    if ($('.xt-claude-btn')[0]) return;
    var $menuButton = getChatsButton();
    if (!$menuButton.length) return;
    var menuButton = $menuButton[0];
    var parent = menuButton.parentNode && menuButton.parentNode.parentNode;
    if (!parent) return;
    parent.style.gridTemplateColumns = 'auto auto 1fr auto';
    var afterBtn = parent.querySelector('div.group');
    var $btn = afterBtn
      ? $(sidebarMenuItemTemplate(darkMode)).insertAfter(afterBtn)
      : $(sidebarMenuItemTemplate(darkMode)).insertAfter($menuButton);
    $btn.on('click', function(e) {
      e.preventDefault();
      toggleWidget();
    });
    addSidebarIframe($btn);
  };


  var getShareActionsContainer = function(){
    var $main = getMainContent();
    if ($main.length) {
      var $actions = $main.find('[data-testid="wiggle-controls-actions"]').first();
      if ($actions.length) return $actions;
    }
    return $('[data-testid="wiggle-controls-actions"]').first();
  };


  var findShareButton = function(){
    var $main = getMainContent();
    var roots = [];
    if ($main.length) roots.push($main[0]);
    roots.push(document);
    for (var r = 0; r < roots.length; r++) {
      var share = roots[r].querySelector('[data-testid="wiggle-controls-actions-share"]');
      if (share) return $(share);
    }
    if ($main.length) {
      var $share = $main.find('[aria-label="Share"], [aria-label*="Share chat"], [aria-label*="Share"]').first();
      if ($share.length) return $share;
    }
    return $('[data-testid="wiggle-controls-actions-share"], header[data-testid="page-header"] [aria-label="Share"]').first();
  };


  var placeHeaderButton = function($btn, $share){
    if ($share.length) {
      $btn.insertBefore($share);
      return;
    }
    var $actions = getShareActionsContainer();
    if (!$actions.length) $actions = getHeaderActionsContainer();
    if ($actions.length) $btn.prependTo($actions);
  };


  var addHeaderButton = function(){
    var $share = findShareButton();
    var $actions = getShareActionsContainer();
    if (!$share.length && !$actions.length && !getHeaderActionsContainer().length) return;

    var $btn = $('.xt-claude-btn-sec').first();
    if (!$btn.length) {
      $btn = $(headerBtnTemplate(darkMode));
      placeHeaderButton($btn, $share);
      $btn.click(function(e) {
        e.preventDefault();
        toggleWidget();
      });
      return;
    }

    if ($share.length) {
      var needsMove = $btn[0] !== $share[0].previousElementSibling;
      if (!needsMove && $share[0].parentNode) {
        needsMove = !$share[0].parentNode.contains($btn[0]);
      }
      if (needsMove) placeHeaderButton($btn, $share);
    }
  };


  var addWidgetButton = function() {
    darkMode = isDarkMode();
    addSidebarButton();
    addHeaderButton();
  };


  var addSidebarIframe = function($btn){
    if ($('#xt-claude-sidebar-iframe')[0]) return;
    var html = Common.renderIframeHTML({
      query: '',
      settingEnabled: true,
      darkMode: darkMode,
      iframeSrcParam: 'claude_sidebar'
    });
    var $root = $('<div>', {id: 'xt-claude-sidebar-iframe'}).html(html);
    var $flexParent = $btn && $btn[0] ? $btn.closest('.flex') : null;
    if ($flexParent && $flexParent[0]) {
      $root.insertAfter($flexParent);
      return;
    }
    if ($btn && $btn[0]) {
      $root.insertAfter($btn);
    }
  };


  var addPersuasions = function(){
    chrome.runtime.sendMessage({
      cmd: 'api.openAIfetchPersuasions',
      data: ''
    }, function(response){
      let isEmpty = Object.keys(response).length === 0;
      if (isEmpty) {
        $('.xt-buttons-container').remove();
        return;
      }
      if (typeof response !== 'object') return;
      let $div = $('<div>');
      for (const key in response) {
        const value = response[key];
        $div.append(`<a data-prompt="${value}">${key}</a>`);
      }
      $('.xt-icon').append($div).find('a').click(function(){
        const prompt = this.dataset.prompt;
        chooseTemplate({prompt: prompt});
      });
    });
  };


  var isDarkMode = function() {
    return document.documentElement.dataset.mode === 'dark';
  };


  var toggleWidget = function(){
    OpenaiWidgetController.toggle({
      darkMode: darkMode,
      source: source
    });
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


  var getSource = function(){
    return source;
  };


  let LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 262.77 262.77"><g id="Layer_2" data-name="Layer 2"><g id="Layer_1-2" data-name="Layer 1"><g><circle cx="131.38" cy="131.38" r="126.38" style="fill: none;stroke-miterlimit: 10;stroke-width: 10px; stroke: #fff;"/><path d="M109.38,106.42c7.54-9,14-17.2,20.94-25,7.63-8.58,15.73-16.73,23.48-25.2,4.32-4.72,9.2-5.71,14.78-2.85,5.07,2.59,10,5.43,14.34,7.81-12.71,12-24.57,23.42-36.64,34.59-4.92,4.56-5.87,9.38-3.45,15.63,11.36,29.37,23.23,58.47,41.41,84.49.95,1.35,2,2.62,3.47,4.5C180.2,206.74,172,210.94,162.14,211c-1.48,0-3.48-2-4.39-3.54-5-8.63-10.36-17.12-14.36-26.2-6.75-15.37-12.57-31.15-18.78-46.77-1-2.6-2-5.22-3.51-9.14-5.47,8.17-12.51,14.31-12.51,23.93,0,16.81.38,33.63.91,50.44.11,3.63-.92,5.56-4.32,6.67-6.73,2.18-13.44,3.46-20.58,2.12-2.79-.52-3.69-1.83-3.77-4.22-.12-3.32-.23-6.65-.16-10q.93-41.44,1.94-82.89c.08-3.33.33-6.65.56-10,.84-11.8-.41-23.09-6-33.86-3.1-5.92-2.59-6.68,3.77-8.25a151.63,151.63,0,0,1,22.45-4c6.93-.64,7.1-.1,7,6.71-.23,12.48-.62,25-.93,37.44C109.34,101.33,109.38,103.16,109.38,106.42Z" style=""/></g></g></g></svg>`;


  return {
    init: init,
    getSource: getSource
  };

})();

