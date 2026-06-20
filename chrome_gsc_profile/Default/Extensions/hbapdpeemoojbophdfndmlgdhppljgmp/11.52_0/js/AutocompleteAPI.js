const AutocompleteAPI = (() => {

  let services = {};
  let fnGetSettings;

  const init = params => {
    if (params.fnGetSettings) fnGetSettings = params.fnGetSettings;
  };


  const get = async (params) => {
    try {
      let settings = await fnGetSettings();
      let res = await services[params.service].get(params, settings);
      console.log(res);
      return res;
    } catch (e) {
      console.log(e);
    }
  };



  services.google = {
    name: 'google',
    async get (params) {
      let url = 'https://www.google.';
      if (params.tld) url += params.tld;
      else url += 'com';
      url += `/complete/search?`;
      if (params.cp) url += 'cp=' + params.cp + '&';
      url += `client=gws-wiz&xssi=t&hl=en&authuser=0&psi=AVxsX9KsAuOX4-EP94KmyAE.1600936964140&dpr=1&q=` + encodeURIComponent(params.query);
      let data = fetchData({url: url})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let jsonStr = text.replace(")]}'", '');
        let json = JSON.parse(jsonStr);
        let items = json[0];
        let res = [];
        items.map(item => {
          let kw = item[0];
          kw = kw.replace(/<\/?b>/g, '');
          res.push({keyword: kw, extra: item[1]});
        });
        // console.log(json, res);
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.youtube = {
    name: 'youtube',
    async get (params) {
      let url = `https://clients1.google.com/complete/search?client=youtube&hl=en&gl=${params.lng}&gs_rn=64&gs_ri=youtube&tok=qd7pItwW99nwgd8R-it9rQ&ds=yt&cp=3&gs_id=9&callback=google.sbox.p50&gs_gbg=09tlsZzNK0Dp4R&q=` + encodeURIComponent(params.query);
      let data = fetchData({url: url})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let jsonStr = text.replace(/^[^(]*?\(/, '');
        jsonStr = jsonStr.replace(/\)[^)]*?$/, '');
        let json = JSON.parse(jsonStr);
        let items = json[1];
        let res = [];
        items.map(item => {
          let kw = item[0];
          kw = kw.replace(/<\/?b>/g, '');
          res.push({keyword: kw, extra: item[1]});
        });
        // console.log(json, res);
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.bing = {
    name: 'bing',
    async get (params, settings) {
      let lng = 'en-us';
      let country = settings.country;
      if (country) {
        lng = 'en-' + country;
        if (country === 'uk') lng = 'en-gb';
      }
      let url = `https://www.bing.com/AS/Suggestions?pt=page.home&mkt=${lng}&cp=7&cvid=RANDOM&qry=` + encodeURIComponent(params.query);
      let data = fetchData({url: url})
        .then(data => {
          // let response = this.parse(data);
          // if (response.error) return response;
          return {error: false, data: {html: data, type: 'bing'}};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let dom = (new DOMParser()).parseFromString(text, "text/html");
        let lis = dom.querySelectorAll('ul li[role=option]');
        let res = [];
        for (let li of lis) {
          if (li.getAttribute('pw') === null && li.getAttribute('sw') === null) {
            res.push({keyword: $.trim(li.textContent)});
          }
        }
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.ebay = {
    name: 'ebay',
    async get (params) {
      let url = ` https://autosug.ebaystatic.com/autosug?_jgr=1&sId=0&_ch=0&callback=0&kwd=` + encodeURIComponent(params.query);
      let data = fetchData({url: url})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let json = JSON.parse(text);
        if (!json.res) return [];
        let items = json.res.sug;
        let res = [];
        items.map(item => {
          res.push({keyword: item});
        });
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.etsy = {
    name: 'etsy',
    async get (params) {
      let url = `https://www.etsy.com/suggestions_ajax.php?extras=%7B%26quot%3Bexpt%26quot%3B%3A%26quot%3Boff%26quot%3B%2C%26quot%3Blang%26quot%3B%3A%26quot%3Ben-GB%26quot%3B%2C%26quot%3Bextras%26quot%3B%3A%5B%5D%2C%26quot%3Bsearches%26quot%3B%3A%5B%5D%7D&version=10_12672349415_19&search_type=all&previous_query=&search_query=` + encodeURIComponent(params.query);
      let data = fetchData({url: url})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let json = JSON.parse(text);
        let items = json.results;
        if (items.length === 1 && items[0].link) return [];
        let res = [];
        items.map(item => {
          if (item.link) return;
          let kw = item.query;
          res.push({keyword: kw});
        });
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.pinterest = {
    name: 'pinterest',
    async get (params) {
      let source_url = `/search/pins/q=${encodeURIComponent(params.query)}&term_meta[]=`;
      let dataParam = `{"options":{"term":"${params.query}","pin_scope":"pins","no_fetch_context_on_resource":false},"context":{}}`;
      let url = 'https://www.pinterest.';
      if (params.tld) url += params.tld;
      else url += 'com';
      url += `/resource/AdvancedTypeaheadResource/get/?source_url=${source_url}&data=${dataParam}`;
      let data = fetchData({url: url, headers: {
        "x-pinterest-pws-handler": "www/search/[scope].js",
      }})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let json = JSON.parse(text);
        console.log(json);
        let items = json.resource_response.data.items;
        let res = [];
        items.map(item => {
          let kw = item.query;
          res.push({keyword: kw});
        });
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.instagram = {
    name: 'instagram',
    async get (params) {
      let url = `https://www.instagram.com/web/search/topsearch/?context=blended&query=${encodeURIComponent(params.query)}&include_reel=true`;
      let data = fetchData({url: url})
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    parse (text) {
      try {
        let json = JSON.parse(text);
        let items = json.hashtags;
        let res = [];
        items.map(item => {
          let kw = item.hashtag.name;
          let score = item.hashtag.media_count;
          res.push({keyword: kw, score: score});
        });
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    }
  };


  services.amazon = {
    name: 'amazon',
    async get (params) {
      const tld = params.tld || 'com';
      const host = 'https://www.amazon.' + tld;
      const url = this.buildSuggestionsUrl(host, params.query, tld);
      let data = fetchData({
        url: url,
        credentials: 'include',
        headers: {
          'Accept': 'application/json, text/javascript, */*; q=0.01',
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
        .then(data => {
          let response = this.parse(data);
          if (response.error) return response;
          return {error: false, data: response};
        })
        .catch(error => {
          return {error: true, data: error.message};
        });
      return data;
    },
    buildSuggestionsUrl (host, query, tld) {
      const mid = this.getMIDbyTLD(tld);
      const lop = this.getLopByTLD(tld);
      const plainMid = this.getPlainMidByTLD(tld);
      const prefix = encodeURIComponent(query || '');
      const lastPrefix = encodeURIComponent((query || '').replace(/\s/g, ''));
      const qs = [
        'limit=11',
        'prefix=' + prefix,
        'suggestion-type=WIDGET',
        'suggestion-type=KEYWORD',
        'page-type=Search',
        'alias=aps',
        'site-variant=desktop',
        'version=3',
        'event=onkeypress',
        'wc=',
        'lop=' + encodeURIComponent(lop),
        'last-prefix=' + lastPrefix,
        'avg-ks-time=1500',
        'fb=1',
        'predicted_text_accepted=',
        'estoken=',
        'session-id=',
        'request-id=',
        'mid=' + encodeURIComponent(mid),
        'plain-mid=' + encodeURIComponent(plainMid),
        'client-info=search-ui'
      ];
      return host + '/suggestions?' + qs.join('&');
    },
    parse (text) {
      try {
        let json = JSON.parse(text);
        let items = json.suggestions;
        let res = [];
        items.map(item => {
          if (item.type === 'KEYWORD') {
            res.push({keyword: item.value});
          }
        });
        return res;
      } catch (e) {
        console.log('Parse error', e, text);
        return {error: true, data: 'Parse error'};
      }
    },
    getLopByTLD (tld) {
      const mapping = {
        'com': 'en_US',
        'in': 'en_IN',
        'co.uk': 'en_GB',
        'ca': 'en_CA',
        'com.au': 'en_AU',
        'de': 'de_DE',
        'fr': 'fr_FR',
        'es': 'es_ES',
        'it': 'it_IT',
        'co.jp': 'ja_JP',
        'com.mx': 'es_MX',
        'com.br': 'pt_BR',
        'nl': 'nl_NL',
        'se': 'sv_SE',
        'ae': 'en_AE',
        'sa': 'en_SA',
        'sg': 'en_SG',
        'com.tr': 'tr_TR',
        'eg': 'en_EG'
      };
      return mapping[tld] || mapping.com;
    },
    getPlainMidByTLD (tld) {
      // Marketplace-specific value; US default "1" is rejected on some locales (e.g. .in).
      const mapping = {
        'in': '44571'
      };
      return mapping[tld] || '1';
    },
    getMIDbyTLD (tld) {
      let mapping = {
        "com.br": "A2Q3Y263D00KWC",
        "ca": "A2EUQ1WTGCTBG2",
        "com.mx": "A1AM78C64UM0Y8",
        "com": "ATVPDKIKX0DER",
        "ae": "A2VIGQ35RCS4UG",
        "de": "A1PA6795UKMFR9",
        "eg": "ARBP9OOSHTCHU",
        "es": "A1RKKUPIHCS9HS",
        "fr": "A13V1IB3VIYZZH",
        "co.uk": "A1F83G8C2ARO7P",
        "in": "A21TJRUUN4KGV",
        "it": "APJ6JRA9NG5V4",
        "nl": "A1805IZSGTT6HS",
        "sa": "A17E79C6D8DWNP",
        "se": "A2NODRKZP88ZB9",
        "com.tr": "A33AVAJ2PDY3EV",
        "sg": "A19VAU5U5O7RUS",
        "com.au": "A39IBJ37TRP1C6",
        "co.jp": "A1VC38T7YXB528"
      };
      let res = mapping[tld];
      if (!res) res = mapping.com;
      return res;
    }
  };


  const decodeParam = (value) => {
    if (!value) return '';
    try {
      return decodeURIComponent(String(value).replace(/\+/g, ' '));
    } catch (e) {
      return String(value);
    }
  };

  const normalizeGooglePlayParams = (params) => {
    return {
      query: (params.query || '').trim(),
      sourcePath: decodeParam(params.sourcePath) || '/store/games',
      hl: decodeParam(params.hl) || 'en',
      catalog: decodeParam(params.catalog) || 'apps',
      at: decodeParam(params.at),
      bl: decodeParam(params.bl),
      fSid: decodeParam(params.fSid)
    };
  };

  services.googleplay = {
    name: 'googleplay',
    async get (params) {
      const payload = normalizeGooglePlayParams(params);
      if (!payload.query) {
        return { error: true, data: 'Empty query' };
      }
      if (!payload.at) {
        return {
          error: true,
          data: 'Missing Play at token. Use Find keywords from a play.google.com page.'
        };
      }

      const built = PlayStoreAutocomplete.buildRequest(payload);
      try {
        const text = await fetchData({
          url: built.url,
          method: 'POST',
          credentials: 'include',
          headers: built.headers,
          body: built.body
        });
        const parsed = PlayStoreAutocomplete.parseResponse(text);
        if (parsed.error) return parsed;
        return { error: false, data: parsed.data };
      } catch (e) {
        return { error: true, data: e.message || 'Request failed' };
      }
    },
    parse (text) {
      return PlayStoreAutocomplete.parseResponse(text);
    }
  };


  const fetchData = async (params) => {
    let response = await fetch(params.url, {
      method: params.method || 'GET',
      credentials: params.credentials || 'omit',
      headers: {
        ...(params.headers || {})
      },
      body: params.body
    });
    if (!response.ok) {
      const msg = response.status;
      throw new Error(msg);
    }
    let data;
    if (params.json) {
      data = await response.json();
    }
    else data = await response.text();
    return data;
  };



  return {
    init,
    get
  };

})();
