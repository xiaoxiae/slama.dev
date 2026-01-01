// Lightbox functionality for images with class "lightbox-trigger"
document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxThumb = document.getElementById('lightbox-thumb');
    const loader = document.querySelector('.lightbox-loader');
    const closeBtn = document.querySelector('.lightbox-close');
    const triggers = document.querySelectorAll('.lightbox-trigger');

    // Add click event to each trigger
    triggers.forEach((trigger) => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const fullSrc = this.href;
            const thumbSrc = this.dataset.thumb;
            showLightbox(fullSrc, thumbSrc);
        });
    });

    function showLightbox(fullSrc, thumbSrc) {
        // Reset state
        lightboxImg.style.display = 'none';
        lightboxThumb.style.display = 'block';
        loader.style.display = 'block';
        closeBtn.style.display = 'none';

        // Show thumbnail immediately
        lightboxThumb.src = thumbSrc;

        // Show lightbox
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        // Load full resolution image
        const fullImg = new Image();
        fullImg.onload = function() {
            lightboxImg.src = fullSrc;
            lightboxImg.style.display = 'block';
            lightboxThumb.style.display = 'none';
            loader.style.display = 'none';
            closeBtn.style.display = 'flex';
        };
        fullImg.onerror = function() {
            // If full image fails to load, hide loader but keep thumbnail
            loader.style.display = 'none';
            closeBtn.style.display = 'flex';
        };
        fullImg.src = fullSrc;
    }

    function hideLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Event listeners
    closeBtn.addEventListener('click', hideLightbox);

    // Close when clicking outside the image
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            hideLightbox();
        }
    });

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (lightbox.style.display === 'flex') {
            if (e.key === 'Escape') {
                hideLightbox();
            }
        }
    });
});
