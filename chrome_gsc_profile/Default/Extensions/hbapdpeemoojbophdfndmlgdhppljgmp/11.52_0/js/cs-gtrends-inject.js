(() => {
  const injectPrefix = "[KE gtrends inject]";
  if (window.__KE_GTRENDS_AJAX_HOOKED__) {
    if (window.__KE_GTRENDS_DEBUG__) {
      console.log(injectPrefix, "ajax hook already installed via MAIN world script");
    }
    return;
  }
  let head = document.head || document.documentElement;
  let script = document.createElement("script");
  const ajaxUrl = chrome.runtime.getURL("js/cs-gtrends-ajax.js");
  script.src = ajaxUrl;
  script.async = false;
  script.addEventListener("load", function () {
    if (window.__KE_GTRENDS_DEBUG__) {
      console.log(injectPrefix, "page script loaded (fallback inject)", ajaxUrl);
    }
  });
  script.addEventListener("error", function () {
    console.error(injectPrefix, "failed to load page script", ajaxUrl);
  });
  head.append(script);
})();
