// rv-chat.js — Widget chat AI cho Reformed Vietnam.
// Không framework, không script bên ngoài, không thu thập dữ liệu cá nhân.
// Cách dùng: chèn 2 dòng trong rv-chat-snippet.html vào cuối <body> của trang.
// API: POST /api/chat { question, history:[{q,a}] } -> { answer, source, link?, books?, removed_citations? }
(function () {
  'use strict';

  var API = '/api/chat';
  var MAX_LEN = 500;
  var DISCLAIMER = 'Câu trả lời do AI soạn — chưa được mục sư duyệt. Hãy đối chiếu với Kinh Thánh.';
  var SUGGESTIONS = [
    'Có sách nào về sự cầu nguyện?',
    'Ân điển là gì?',
    'Tìm sách của Spurgeon',
  ];

  var state = { open: false, ready: null, quotaHit: false, sending: false, history: [] };

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  }

  function svgIcon() {
    // Bong bóng chat — cùng phong cách SVG như nút "về đầu trang" của site.
    return '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>';
  }

  function build() {
    var root = el('div', 'rv-chat');
    root.id = 'rvChat';

    // Nút tròn nổi góc dưới-TRÁI (góc dưới-phải đã có nút "về đầu trang").
    var fab = el('button', 'rv-chat-fab');
    fab.type = 'button';
    fab.setAttribute('aria-label', 'Hỏi AI');
    fab.setAttribute('aria-expanded', 'false');
    fab.innerHTML = svgIcon();
    fab.appendChild(el('span', 'rv-chat-fab-label', 'Hỏi AI'));

    // Panel chat.
    var panel = el('div', 'rv-chat-panel');
    panel.setAttribute('role', 'dialog');
    panel.setAttribute('aria-label', 'Hỏi AI — Thư viện Reformed Vietnam');
    panel.hidden = true;

    var head = el('div', 'rv-chat-head');
    var titleWrap = el('div', 'rv-chat-titles');
    titleWrap.appendChild(el('strong', null, 'Hỏi AI — Thư viện Reformed Vietnam'));
    titleWrap.appendChild(el('span', 'rv-chat-sub', 'AI trả lời, chưa được mục sư duyệt.'));
    var closeBtn = el('button', 'rv-chat-close', '✕');
    closeBtn.type = 'button';
    closeBtn.setAttribute('aria-label', 'Đóng chat');
    head.appendChild(titleWrap);
    head.appendChild(closeBtn);

    var body = el('div', 'rv-chat-body');
    body.setAttribute('aria-live', 'polite');

    var suggest = el('div', 'rv-chat-suggest');
    SUGGESTIONS.forEach(function (s) {
      var b = el('button', 'rv-chat-chip', s);
      b.type = 'button';
      b.addEventListener('click', function () { send(s); });
      suggest.appendChild(b);
    });
    body.appendChild(suggest);

    var foot = el('div', 'rv-chat-foot');
    var input = document.createElement('input');
    input.type = 'text';
    input.maxLength = MAX_LEN;
    input.placeholder = 'Hỏi về Kinh Thánh, thần học, hoặc tìm sách…';
    input.setAttribute('aria-label', 'Câu hỏi của bạn');
    var sendBtn = el('button', 'rv-chat-send', 'Gửi');
    sendBtn.type = 'button';
    foot.appendChild(input);
    foot.appendChild(sendBtn);

    var links = el('div', 'rv-chat-links');
    var qa = document.createElement('a');
    qa.href = '/hoi-dap/';
    qa.textContent = 'Xem 95 câu hỏi đã trả lời';
    links.appendChild(qa);

    panel.appendChild(head);
    panel.appendChild(body);
    panel.appendChild(foot);
    panel.appendChild(links);
    root.appendChild(fab);
    root.appendChild(panel);
    document.body.appendChild(root);

    function toggle(open) {
      state.open = open;
      panel.hidden = !open;
      fab.setAttribute('aria-expanded', String(open));
      if (open) {
        if (state.ready === null) checkReady();
        input.focus();
      }
    }
    fab.addEventListener('click', function () { toggle(!state.open); });
    closeBtn.addEventListener('click', function () { toggle(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && state.open) toggle(false);
    });

    function setInputEnabled(on) {
      input.disabled = !on;
      sendBtn.disabled = !on;
    }

    // Kiểm tra function đã deploy + đã có key chưa (GET /api/chat).
    function checkReady() {
      fetch(API, { method: 'GET' })
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          if (d && d.ok) {
            state.ready = !!d.ready;
            if (!d.ready) showPreparing();
          } else {
            state.ready = false;
            showPreparing();
          }
        })
        .catch(function () {
          state.ready = false;
          showPreparing();
        });
    }
    function showPreparing() {
      setInputEnabled(false);
      var n = el('div', 'rv-chat-notice', 'Tính năng chat AI đang được chuẩn bị, mời bạn quay lại sau.');
      body.appendChild(n);
      body.scrollTop = body.scrollHeight;
    }

    function addMsg(kind, text) {
      var m = el('div', 'rv-chat-msg rv-chat-' + kind);
      var bubble = el('div', 'rv-chat-bubble', text);
      m.appendChild(bubble);
      if (kind === 'ai') {
        m.appendChild(el('div', 'rv-chat-disclaimer', DISCLAIMER));
      }
      body.appendChild(m);
      body.scrollTop = body.scrollHeight;
      return m;
    }

    function addLinkCard(url, label, sub) {
      var a = document.createElement('a');
      a.className = 'rv-chat-card';
      a.href = url;
      var b = el('strong', null, label);
      a.appendChild(b);
      if (sub) a.appendChild(el('span', null, sub));
      body.appendChild(a);
      body.scrollTop = body.scrollHeight;
    }

    function typing() {
      var m = el('div', 'rv-chat-msg rv-chat-ai');
      var b = el('div', 'rv-chat-bubble rv-chat-typing');
      b.appendChild(el('span'));
      b.appendChild(el('span'));
      b.appendChild(el('span'));
      m.appendChild(b);
      body.appendChild(m);
      body.scrollTop = body.scrollHeight;
      return m;
    }

    function send(text) {
      var q = (text !== undefined ? text : input.value).trim();
      if (!q || state.sending || state.quotaHit) return;
      if (state.ready === false) return; // đang chuẩn bị
      input.value = '';
      state.sending = true;
      setInputEnabled(false);
      addMsg('user', q);
      var t = typing();
      fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: q,
          history: state.history.slice(-2),
        }),
      })
        .then(function (r) { return r.json().then(function (d) { return { status: r.status, d: d }; }); })
        .then(function (res) {
          t.remove();
          var d = res.d || {};
          if (res.status === 200 && d.answer) {
            addMsg('ai', d.answer);
            if (d.link) addLinkCard(d.link, d.link_label || 'Đọc câu trả lời đầy đủ', 'Hỏi Đáp Cải Chánh');
            if (Array.isArray(d.books)) {
              d.books.forEach(function (bk) {
                addLinkCard(bk.url, bk.title, bk.author);
              });
            }
            state.history.push({ q: q, a: d.answer });
            if (state.history.length > 4) state.history = state.history.slice(-4);
          } else if (res.status === 429 && d.error === 'quota') {
            state.quotaHit = true;
            addMsg('ai', d.message || 'Hôm nay đã hết lượt trả lời miễn phí, mời bạn quay lại sau 0:00 giờ.');
          } else if (res.status === 429) {
            addMsg('ai', d.message || 'Bạn hỏi hơi nhanh, mời thử lại sau ít phút nhé.');
          } else if (res.status === 503) {
            state.ready = false;
            addMsg('ai', d.message || 'Tính năng chat AI đang được chuẩn bị, mời bạn quay lại sau.');
          } else {
            addMsg('ai', (d && d.message) || 'Có lỗi xảy ra, mời thử lại sau.');
          }
        })
        .catch(function () {
          t.remove();
          addMsg('ai', 'Không kết nối được, thử lại sau.');
        })
        .finally(function () {
          state.sending = false;
          if (!state.quotaHit && state.ready !== false) setInputEnabled(true);
          input.focus();
        });
    }

    sendBtn.addEventListener('click', function () { send(); });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') send();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
