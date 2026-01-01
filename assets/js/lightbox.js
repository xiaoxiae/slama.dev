// Lightbox functionality for images with class "lightbox-trigger"
document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxThumb = document.getElementById('lightbox-thumb');
    const closeBtn = document.querySelector('.lightbox-close');
    const prevBtn = document.querySelector('.lightbox-prev');
    const nextBtn = document.querySelector('.lightbox-next');
    const triggers = Array.from(document.querySelectorAll('.lightbox-trigger'));

    let currentIndex = 0;

    // Add click event to each trigger
    triggers.forEach((trigger, index) => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            currentIndex = index;
            showLightbox(this.href, this.dataset.thumb);
        });
    });

    function showLightbox(fullSrc, thumbSrc) {
        // Reset state
        lightboxImg.style.display = 'none';
        lightboxThumb.style.display = 'block';
        closeBtn.style.display = 'flex';

        // Show/hide nav buttons based on number of images
        if (triggers.length > 1) {
            prevBtn.style.display = 'flex';
            nextBtn.style.display = 'flex';
        } else {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        }

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
        };
        fullImg.src = fullSrc;
    }

    function navigate(direction) {
        currentIndex = (currentIndex + direction + triggers.length) % triggers.length;
        const trigger = triggers[currentIndex];
        showLightbox(trigger.href, trigger.dataset.thumb);
    }

    function hideLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Event listeners
    closeBtn.addEventListener('click', hideLightbox);
    prevBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        navigate(-1);
    });
    nextBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        navigate(1);
    });

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
            } else if (e.key === 'ArrowLeft') {
                navigate(-1);
            } else if (e.key === 'ArrowRight') {
                navigate(1);
            }
        }
    });
});
