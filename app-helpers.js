(function () {
  var utils = window.RV_UTILS = window.RV_UTILS || {};

  utils.esc = function (s) {
    return String(s).replace(/[&<>\"]/g, function (c) {
      return {"&":"&amp;","<":"&lt;", ">":"&gt;","\"":"&quot;"}[c];
    });
  };

  utils.saveLS = function (k, v) {
    try {
      localStorage.setItem(k, JSON.stringify(v));
    } catch (e) {}
  };

  utils.srcOf = function (b) {
    return b.read ? "ccel" : (b.au || "other");
  };

  utils.hasM = function (b, m) {
    if (m === "read") return !!b.read || !!(b.url && /\/doc\//.test(b.url));
    if (m === "pdf") return !!b.pdf || !!(b.dl && (b.dl.PDF || b.dl.pdf));
    if (m === "epub") return !!b.epub || !!(b.dl && (b.dl.EPUB || b.dl.epub));
    if (m === "audio") return !!(b.listen || b.audio || b.au === "lv" || (b.dl && (b.dl.audio || b.dl.AUDIO)));
    return false;
  };

  utils.typeOf = function (title, key, over) {
    if (over && over[key]) return over[key];
    var t = String(title).toLowerCase();
    if (/catechism|confession of faith|creeds/.test(t)) return "catechism";
    if (/commentar|exposition|expository|harmony of|annotations|treasury of david/.test(t)) return "commentary";
    if (/sermon/.test(t)) return "sermons";
    if (/systematic theology|institutes|institutio|dogmatic|body of divinity|body of practical divinity|doctrinal divinity|summary of christian doctrine|reformed doctrine of predestination/.test(t)) return "systematic";
    if (/^works of|practical works|miscellaneous/.test(t)) return "collected";
    if (/history|martyrs|life of|christian church|philosophy of revelation|person of christ/.test(t)) return "history";
    if (/morning and evening|checkbook|daily readings|everlasting rest|prayer|meditation|letters|contentment|holiness|crook|cordial|lovely|armour|saint indeed/.test(t)) return "devotional";
    return "doctrine";
  };

  utils.eraOf = function (y) {
    return y < 1500 ? "anc" : y < 1600 ? "ref" : y < 1700 ? "pur" : y < 1800 ? "aw" : y < 1900 ? "mod" : "c20";
  };
})();
