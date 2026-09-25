// Plays the {{< sound >}} links in place. Web Audio rather than an <audio>
// element: the clips are clicks a fifth of a second long, and an element only
// fetches, decodes and opens the output once clicked, which swallows most of
// the first play. So the file is decoded on hover, the output is woken on
// pointerdown, and the clip starts once the output is actually running.
(function () {
  var ctx = null;
  var playing = null;
  var seq = 0;

  function context() {
    return ctx || (ctx = new (window.AudioContext || window.webkitAudioContext)());
  }

  function link(e) {
    return e.target.closest ? e.target.closest('a.sound') : null;
  }

  function load(a) {
    return a.sound || (a.sound = fetch(a.href)
      .then(function (r) { return r.arrayBuffer(); })
      .then(function (data) { return context().decodeAudioData(data); }));
  }

  function stop() {
    seq++;
    if (!playing) return;
    playing.source.onended = null;
    playing.source.stop();
    playing.link.classList.remove('playing');
    playing = null;
  }

  function warm(e) {
    var a = link(e);
    if (a) load(a);
  }

  document.addEventListener('pointerover', warm);
  document.addEventListener('focusin', warm);
  document.addEventListener('pointerdown', function (e) {
    if (link(e)) context().resume();
  });

  document.addEventListener('click', function (e) {
    var a = link(e);
    // Leave middle-click and ctrl/cmd-click to open the raw file.
    if (!a || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();

    var toggledOff = playing && playing.link === a;
    stop();
    if (toggledOff) return;

    var mine = seq;
    var c = context();
    Promise.all([load(a), c.resume()]).then(function (r) {
      if (mine !== seq) return;
      var source = c.createBufferSource();
      source.buffer = r[0];
      source.connect(c.destination);
      source.onended = function () {
        a.classList.remove('playing');
        playing = null;
      };
      playing = { link: a, source: source };
      a.classList.add('playing');
      source.start();
    });
  });
})();
