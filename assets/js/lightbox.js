document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const content = lightbox.querySelector('.lightbox-content');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxThumb = document.getElementById('lightbox-thumb');
    const captionEl = document.getElementById('lightbox-caption');
    const closeBtn = lightbox.querySelector('.lightbox-close');
    const prevBtn = lightbox.querySelector('.lightbox-prev');
    const nextBtn = lightbox.querySelector('.lightbox-next');

    // The [href$=".mp4"] guard is load-bearing: the legend at the top of
    // /climbing/ hand-writes <a>F</a> / <a>A</a> with no href and no class.
    const GROUP_DEFS = [
        { type: 'image', selector: 'a.lightbox-trigger' },
        { type: 'video', selector: 'a.climbing-link[href$=".mp4"]' },
    ];

    const groups = GROUP_DEFS.map(function(def) {
        return { type: def.type, items: Array.from(document.querySelectorAll(def.selector)) };
    }).filter(function(group) {
        return group.items.length > 0;
    });

    if (groups.length === 0) return;

    const HASH_PREFIX = '#v=';

    let current = null;
    let videoEl = null;
    let pushedHash = false;

    groups.forEach(function(group) {
        group.items.forEach(function(trigger, index) {
            trigger.addEventListener('click', function(e) {
                // Leave middle-click and ctrl/cmd-click to open the raw file.
                if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
                e.preventDefault();
                open(group, index, true);
            });
        });
    });

    function getVideoEl() {
        if (videoEl) return videoEl;
        videoEl = document.createElement('video');
        videoEl.id = 'lightbox-video';
        videoEl.controls = true;
        videoEl.preload = 'none';
        videoEl.playsInline = true; // iOS plays inline rather than going fullscreen
        videoEl.addEventListener('click', togglePlay);
        content.appendChild(videoEl);
        return videoEl;
    }

    function togglePlay() {
        if (!videoEl) return;
        if (videoEl.paused) {
            const p = videoEl.play();
            if (p && p.catch) p.catch(function() {});
        } else {
            videoEl.pause();
        }
    }

    function releaseVideo() {
        if (!videoEl) return;
        videoEl.pause();
        // Not src = '', which resolves against the page URL and makes the
        // browser load the document itself as media. load() then frees the
        // buffer and aborts the in-flight fetch.
        videoEl.removeAttribute('src');
        videoEl.removeAttribute('poster');
        videoEl.load();
        videoEl.style.display = 'none';
    }

    function render() {
        const group = current.group;
        const trigger = group.items[current.index];

        releaseVideo();
        lightboxImg.style.display = 'none';
        lightboxImg.classList.remove('lightbox-media');
        lightboxThumb.style.display = 'none';
        closeBtn.style.display = 'flex';

        const many = group.items.length > 1;
        prevBtn.style.display = many ? 'flex' : 'none';
        nextBtn.style.display = many ? 'flex' : 'none';

        if (group.type === 'video') renderVideo(trigger);
        else renderImage(trigger);
    }

    function renderImage(trigger) {
        setCaption('');
        lightboxThumb.src = trigger.dataset.thumb;
        lightboxThumb.style.display = 'block';

        const full = new Image();
        full.onload = function() {
            // May resolve after the user has already arrowed on.
            if (!current || current.group.items[current.index] !== trigger) return;
            lightboxImg.src = trigger.href;
            lightboxImg.style.display = 'block';
            lightboxThumb.style.display = 'none';
        };
        full.src = trigger.href;
    }

    // An <img>, not a paused <video>: browsers paint their own overlay play
    // button over a paused video, and Firefox's lives in the shadow DOM where
    // page CSS cannot reach it. Every X.mp4 has a sibling X.webp poster.
    function renderVideo(trigger) {
        lightboxImg.classList.add('lightbox-media');
        lightboxImg.src = posterFor(trigger);
        lightboxImg.style.display = 'block';
        setCaption(describe(trigger));
    }

    function startPlayback() {
        if (!current || current.group.type !== 'video') return;
        const trigger = current.group.items[current.index];
        const video = getVideoEl();
        video.poster = posterFor(trigger);
        video.src = trigger.getAttribute('href');
        video.style.display = 'block';
        lightboxImg.style.display = 'none';
        const p = video.play();
        if (p && p.catch) p.catch(function() {}); // refused autoplay leaves the controls
    }

    function posterFor(trigger) {
        return trigger.getAttribute('href').replace(/\.mp4$/i, '.webp');
    }

    function describe(trigger) {
        const parts = [];
        const href = trigger.getAttribute('href') || '';

        // The month-header "best send" link sits in an <h4>, with no <mark> and
        // no data-wall above it. The same file is always also listed inside its
        // own session, so borrow that copy's caption.
        if (!trigger.closest('mark.climbing-diary-record')) {
            const twin = findTwin(trigger, href);
            if (twin) return describe(twin);
        }

        // scripts/climbing.py names files <wall>-<colour|grade>-<date>-<rand8>.mp4.
        // Reading the date from there works on both pages; the session <li id>
        // only exists on the diary.
        const d = /(\d{4})-(\d{2})-(\d{2})-[a-z]{8}\.mp4$/.exec(href);
        if (d) parts.push(Number(d[3]) + '. ' + Number(d[2]) + '. ' + d[1]);

        const mark = trigger.closest('mark.climbing-diary-record');

        // Board sections label themselves with a <strong> before the <mark>
        // ("Tension Board (40°): "); every other wall carries data-wall.
        let wall = null;
        if (mark) {
            let node = mark.previousElementSibling;
            while (node && node.tagName !== 'STRONG') node = node.previousElementSibling;
            if (node && /:\s*$/.test(node.textContent)) {
                wall = node.textContent.replace(/\s*\([^)]*\)\s*:\s*$/, '').replace(/:\s*$/, '').trim();
            }
        }
        if (!wall) {
            const scope = trigger.closest('[data-wall]');
            if (scope) wall = scope.getAttribute('data-wall');
        }
        if (wall) parts.push(wall);

        // Graded walls put the grade in the leading <strong> ("7a:"); colour
        // walls only encode it as a climbing-<colour>-text class.
        if (mark) {
            const strong = mark.querySelector('strong');
            const text = strong ? strong.textContent.trim() : '';
            if (/:$/.test(text)) {
                parts.push(text.replace(/:$/, ''));
            } else {
                Array.prototype.forEach.call(mark.classList, function(c) {
                    const m = /^climbing-(.+)-text$/.exec(c);
                    if (m && m[1] !== 'other') parts.push(m[1].replace(/-/g, ' '));
                });
            }
        }

        return parts.join(' · ');
    }

    function findTwin(trigger, href) {
        for (let g = 0; g < groups.length; g++) {
            if (groups[g].type !== 'video') continue;
            const items = groups[g].items;
            for (let i = 0; i < items.length; i++) {
                if (items[i] !== trigger &&
                    items[i].getAttribute('href') === href &&
                    items[i].closest('mark.climbing-diary-record')) {
                    return items[i];
                }
            }
        }
        return null;
    }

    function setCaption(text) {
        if (!captionEl) return;
        captionEl.textContent = text;
        captionEl.style.display = text ? 'block' : 'none';
    }

    function open(group, index, pushHash) {
        current = { group: group, index: index };
        render();
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        if (pushHash) syncHash();
    }

    function syncHash() {
        if (!current || current.group.type !== 'video') return;
        const file = current.group.items[current.index].getAttribute('href').split('/').pop();
        // pushState rather than location.hash, so Back closes the spotlight.
        history.pushState({ lightbox: true }, '', HASH_PREFIX + file);
        pushedHash = true;
    }

    function navigate(direction) {
        if (!current) return;
        const n = current.group.items.length;
        current.index = (current.index + direction + n) % n;
        render();
        if (pushedHash && current.group.type === 'video') {
            const file = current.group.items[current.index].getAttribute('href').split('/').pop();
            history.replaceState({ lightbox: true }, '', HASH_PREFIX + file);
        }
    }

    function hideLightbox(popHash) {
        releaseVideo();
        setCaption('');
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';

        // Rolling across a year boundary can leave the current send inside a
        // collapsed <details>.
        if (current) {
            const trigger = current.group.items[current.index];
            let d = trigger.closest('details');
            while (d) {
                d.open = true;
                d = d.parentElement ? d.parentElement.closest('details') : null;
            }
            trigger.scrollIntoView({ block: 'center' });
        }
        current = null;

        if (popHash && pushedHash) {
            pushedHash = false;
            history.back();
        } else {
            pushedHash = false;
        }
    }

    closeBtn.addEventListener('click', function() { hideLightbox(true); });
    prevBtn.addEventListener('click', function(e) { e.stopPropagation(); navigate(-1); });
    nextBtn.addEventListener('click', function(e) { e.stopPropagation(); navigate(1); });

    lightboxImg.addEventListener('click', function(e) {
        if (current && current.group.type === 'video') {
            e.stopPropagation();
            startPlayback();
        }
    });

    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) hideLightbox(true);
    });

    document.addEventListener('keydown', function(e) {
        if (lightbox.style.display !== 'flex') return;
        if (e.metaKey || e.ctrlKey || e.altKey) return;
        if (e.key === 'Escape') {
            hideLightbox(true);
        } else if (e.key === 'ArrowLeft') {
            e.preventDefault();
            navigate(-1);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            navigate(1);
        } else if (e.key === ' ' && current && current.group.type === 'video') {
            e.preventDefault();
            if (videoEl && videoEl.style.display !== 'none') togglePlay();
            else startPlayback();
        }
    });

    function findByFile(file) {
        for (let g = 0; g < groups.length; g++) {
            if (groups[g].type !== 'video') continue;
            const items = groups[g].items;
            for (let i = 0; i < items.length; i++) {
                if (items[i].getAttribute('href').split('/').pop() === file) {
                    return { group: groups[g], index: i };
                }
            }
        }
        return null;
    }

    function openFromHash() {
        if (location.hash.indexOf(HASH_PREFIX) !== 0) return false;
        const hit = findByFile(location.hash.slice(HASH_PREFIX.length));
        if (!hit) return false;
        open(hit.group, hit.index, false); // already the current history entry
        pushedHash = true;
        return true;
    }

    window.addEventListener('popstate', function() {
        if (location.hash.indexOf(HASH_PREFIX) === 0) {
            const hit = findByFile(location.hash.slice(HASH_PREFIX.length));
            if (hit) { open(hit.group, hit.index, false); return; }
        }
        if (lightbox.style.display === 'flex') hideLightbox(false);
    });

    openFromHash();
});
