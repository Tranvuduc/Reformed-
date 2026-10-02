(function () {
  var util = window.RV_UTILS = window.RV_UTILS || {};

  util.getInitialState = function () {
    var state = {
      f: 'all',
      q: '',
      an: '',
      sr: 'all',
      md: 'all',
      ty: 'all',
      er: 'all',
      so: '0',
      limit: 48,
      saved: [],
      prog: {},
      lang: 'vi'
    };

    try {
      state.saved = JSON.parse(localStorage.getItem('rv.saved') || '[]');
      state.prog = JSON.parse(localStorage.getItem('rv.prog') || '{}');
      var l = localStorage.getItem('rv.lang');
      if (l) state.lang = l;
    } catch (e) {}

    return state;
  };

  util.setStateValue = function (state, key, value) {
    state[key] = value;
    return state;
  };

  util.trimToLower = function (text) {
    return String(text || '').trim().toLowerCase();
  };

  util.isHomeView = function (state) {
    return state.f === 'all' && !state.q && state.sr === 'all' && !state.an && state.md === 'all' && state.ty === 'all' && state.er === 'all' && state.so === '0' && !state.br;
  };

  util.filtersOn = function (state) {
    return state.sr !== 'all' || !!state.an || state.md !== 'all' || state.ty !== 'all' || state.er !== 'all' || state.so !== '0' || state.q !== '' || state.f !== 'all';
  };

  util.nAct = function (state) {
    return (state.sr !== 'all') + (!!state.an) + (state.md !== 'all') + (state.ty !== 'all') + (state.er !== 'all') + (state.so !== '0');
  };
})();
