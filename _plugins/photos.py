#!/usr/bin/env python3
import os
from pathlib import Path
from datetime import datetime
import glob

os.chdir(os.path.dirname(os.path.realpath(__file__)))

OUTPUT = "../_includes/photos.md"
PHOTOS_DIR = "../photos/raw"

# Photo metadata - path as key, metadata dict as value
photo_metadata = {
    "2025-09-13-mouse.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lzyz2ytpn224"
    },
    "2025-09-12-waterfall.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lztvvrjb6222"
    },
    "2025-08-19-flower.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lxxby3v2zs24"
    },
    "2025-08-19-bee.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lxua6cpu622j"
    },
    "2025-08-19-birds.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lx5ocrhbd22n"
    },
    "2025-08-19-bird.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lxmlqdacn22e"
    },
    "2025-08-19-pig.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lxdbratzds25"
    },
    "2025-08-19-chipmunk.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lxaojufuk22b"
    },
    "2025-08-19-butterfly.jpg": {
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lx434ffo3c2a"
    },
    "2025-04-21-paraglider.jpg": {
        "instagram_url": "https://www.instagram.com/p/DItbRiuI-fM/"
    },
    "2025-03-16-droplets.jpg": {
        "instagram_url": "https://www.instagram.com/p/DHRsPwIIJhL/"
    },
    "2025-01-05-plant.jpg": {
        "instagram_url": "https://www.instagram.com/p/DEdHAJ2NqjM/"
    },
    "2025-01-02-berry.jpg": {
        "instagram_url": "https://www.instagram.com/p/DEVk3t3ghpc/",
        "bluesky_url": "https://bsky.app/profile/tomas.slama.dev/post/3lzqwaihxp22p"
    },
    "2024-12-30-plant.jpg": {
        "instagram_url": "https://www.instagram.com/p/DENzwA_tUXL/"
    },
    "2024-11-20-paris-duck.jpg": {
        "instagram_url": "https://www.instagram.com/p/DCmNLQtorUq/"
    },
    "2024-11-17-paris-statue.jpg": {
        "instagram_url": "https://www.instagram.com/p/DCd84NEI4B9/"
    },
    "2024-11-14-paris-eiffel.jpg": {
        "instagram_url": "https://www.instagram.com/p/DCWag7uIUkg/"
    },
    "2024-11-10-oviedo-seagul.jpg": {
        "instagram_url": "https://www.instagram.com/p/DCM2X8YoDex/"
    },
    "2024-11-06-oviedo-crow.jpg": {
        "instagram_url": "https://www.instagram.com/p/DCCBhNCoCfI/"
    },
    "2024-11-03-oviedo-lake.jpg": {
        "instagram_url": "https://www.instagram.com/p/DB6AlhnIr1m/"
    },
    "2024-10-31-oviedo-lizard.jpg": {
        "instagram_url": "https://www.instagram.com/p/DBzAUUYI6MV/"
    },
    "2024-10-28-oviedo-panorama.jpg": {
        "instagram_url": "https://www.instagram.com/p/DBrLFBBIBog/"
    },
    "2024-10-16-panorama.jpg": {
        "instagram_url": "https://www.instagram.com/p/DBMKqFVo8yn/"
    },
    "2024-10-13-fire.jpg": {
        "instagram_url": "https://www.instagram.com/p/DBEcVFSIYYM/"
    },
    "2024-10-10-bird.jpg": {
        "instagram_url": "https://www.instagram.com/p/DA8uhEutbjS/"
    },
    "2024-10-07-austria-10-cows.jpg": {
        "instagram_url": "https://www.instagram.com/p/DA0-9NWtBFq/"
    },
    "2024-10-04-austria-9-mountains.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAtQo4Xtpk7/"
    },
    "2024-10-01-austria-8-mountains.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAlloUrNi28/"
    },
    "2024-09-28-austria-7-otis.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAd0XEPtCIy/"
    },
    "2024-09-25-austria-6-water.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAWE0Yytsy3/"
    },
    "2024-09-23-austria-5-mountains.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAQ9B3ytjw8/"
    },
    "2024-09-21-austria-4-clouds.jpg": {
        "instagram_url": "https://www.instagram.com/p/DALy2oqtW3g/"
    },
    "2024-09-19-austria-3-water.jpg": {
        "instagram_url": "https://www.instagram.com/p/DAGpP9LN-pY/"
    },
    "2024-09-17-austria-2-stars.jpg": {
        "instagram_url": "https://www.instagram.com/p/DABfnHytIH-/"
    },
    "2024-09-15-austria-1-sunset.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_8VcJhtyq6/"
    },
    "2024-09-11-romania-9-forest.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_yC3rztXDn/"
    },
    "2024-09-10-romania-8-feather.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_vdfYGtpzB/"
    },
    "2024-09-09-romania-7-doggo.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_sxVMdNrY2/"
    },
    "2024-09-08-romania-6-doggo.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_qL6T-NekZ/"
    },
    "2024-09-07-romania-5-statue.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_nnElXtAw8/"
    },
    "2024-09-06-romania-4-doggo.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_lC4WINB3E/"
    },
    "2024-09-05-romania-3-crows.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_ic_17Nlvb/"
    },
    "2024-09-04-romania-2-dome.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_f3jZltPjF/"
    },
    "2024-09-03-romania-1-summit.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_dSzOitq8U/"
    },
    "2024-08-30-cabin.jpg": {
        "instagram_url": "https://www.instagram.com/p/C_TIOcVNtUo/"
    },
    "2024-08-25-frog.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-2xNP6tQNo/"
    },
    "2024-08-22-duck.jpg": {
        "instagram_url": "https://www.instagram.com/p/C--dPuqtePV/"
    },
    "2024-08-18-lizard.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-0I-8KNd2f/"
    },
    "2024-08-16-birdhouse.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-5Xo_fNDkg/"
    },
    "2024-08-12-moon.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-k_hBBtLsK/"
    },
    "2024-08-11-protab.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-iEwWLt4nI/"
    },
    "2024-08-07-cat.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-X7nbfiEKq/"
    },
    "2024-07-29-berd.jpg": {
        "instagram_url": "https://www.instagram.com/p/C-DNxsUN-di/"
    },
    "2024-07-26-tatry-1.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=3"
    },
    "2024-07-26-tatry-3.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=2"
    },
    "2024-07-26-tatry-4.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9m__DOtQt-/?img_index=1"
    },
    "2024-07-22-vrat.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9kXxFKN3-s/"
    },
    "2024-07-18-squirrel.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9uq4K5tiBR/?img_index=2"
    },
    "2024-07-14-moon.jpg": {
        "instagram_url": "https://www.instagram.com/p/C97fajytWD1/"
    },
    "2024-07-09-austria.jpg": {
        "instagram_url": "https://www.instagram.com/p/C9NV0xKNI1s/?img_index=1"
    },
    "2021-10-31-prague-4.jpg": {
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=4"
    },
    "2021-10-31-prague-3.jpg": {
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=3"
    },
    "2021-10-31-prague-2.jpg": {
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=2"
    },
    "2021-10-31-prague-1.jpg": {
        "instagram_url": "https://www.instagram.com/p/CVq_Gw3N-Y_/?img_index=1"
    },
    "2018-06-27-fire.jpg": {
        "instagram_url": "https://www.instagram.com/p/Bkg1_sKFDB4/"
    },
    "2017-12-25-christmas.jpg": {
        "instagram_url": "https://www.instagram.com/p/BdI2KnOH_If/?img_index=4"
    },
    "2017-12-25-winter.jpg": {
        "instagram_url": "https://www.instagram.com/p/BcgD6DYlo57/"
    },
    "2017-07-03-other.jpg": {
        "instagram_url": "https://www.instagram.com/p/BWFzjsglya6/"
    },
    "2017-02-26-winter.jpg": {
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    "2016-07-16-sunset.jpg": {
        "instagram_url": "https://www.instagram.com/p/BH7PSl9AS5a/"
    },
    "2016-06-30-sunset.jpg": {
        "instagram_url": "https://www.instagram.com/p/BHRgCv1AAVY/"
    },
    "2015-06-08-flower-2.jpg": {
        "instagram_url": "https://www.instagram.com/p/3rpA4whHD7/"
    },
    "2015-06-08-flower-1.jpg": {
        "instagram_url": "https://www.instagram.com/p/3rWUaeBHMQ/"
    },
    "2015-06-06-bee.jpg": {
        "instagram_url": "https://www.instagram.com/p/3k9LqVBHM5/"
    },
}

def get_all_photos():
    """Get all photo files from the photos directory."""
    if not os.path.exists(PHOTOS_DIR):
        print(f"Photos directory '{PHOTOS_DIR}' not found!")
        return []

    # Get all image files (common extensions)
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.gif']
    photos = []

    for ext in extensions:
        photos.extend(glob.glob(os.path.join(PHOTOS_DIR, ext)))
        photos.extend(glob.glob(os.path.join(PHOTOS_DIR, ext.upper())))

    # Convert to Path objects and get just the filename
    return [Path(photo).name for photo in photos]

def is_valid_date_format(filename):
    """Check if filename starts with YYYY-MM-DD format."""
    try:
        datetime.strptime(filename[:10], '%Y-%m-%d')
        return True
    except ValueError:
        return False

def process_photos():
    """Process all photos and generate HTML."""
    all_photos = get_all_photos()
    valid_photos = []

    for photo in all_photos:
        if is_valid_date_format(photo):
            path = Path(photo)

            # Parse date and skip future photos
            date = datetime.strptime(path.name[:10], '%Y-%m-%d')
            if date > datetime.now():
                print(f"Skipping future image '{photo}' ({date.strftime('%Y/%m/%d')} > today)")
                continue

            # Get metadata if available
            metadata = photo_metadata.get(photo, {})

            valid_photos.append({
                'path': path,
                'date': date,
                'metadata': metadata
            })
        else:
            print(f"Skipping '{photo}' - doesn't match YYYY-MM-DD format")

    # Sort by date (newest first)
    valid_photos.sort(key=lambda x: x['date'], reverse=True)

    return valid_photos

def generate_html(photos):
    """Generate HTML for photo gallery."""
    results = """
<div class='grid'>
"""

    for photo in photos:
        path = photo['path']
        date = photo['date']
        metadata = photo['metadata']

        date_string = date.strftime('%Y/%m/%d')
        photo_url = f"/photos/{path.with_suffix('.webp').name}"
        download_url = f"/photos/raw/{path}"

        # Build icons
        icons = f"""
            <a href="{download_url}" download class="icon download">
                <i class="fas fa-download"></i>
            </a>
        """

        # Add Instagram icon if URL exists
        if 'instagram_url' in metadata:
            icons += f"""
                <a href="{metadata['instagram_url']}" target="_blank" class="icon instagram">
                    <i class="fab fa-instagram"></i>
                </a>
            """

        # Add Bluesky icon if URL exists
        if 'bluesky_url' in metadata:
            icons += f"""
                <a href="{metadata['bluesky_url']}" target="_blank" class="icon bluesky">
                    <i class="fab fa-bluesky"></i>
                </a>
            """

        results += f"""
        <div class="no-invert">
            <div class="date">{date_string}</div>
            <img src="{photo_url}" alt="Image" class="gallery-img" data-full="{download_url}">
            <div class="icons">{icons}</div>
        </div>
        """

    results += """
</div>

<!-- Lightbox Modal -->
<div id="lightbox" class="lightbox no-invert" style="display: none;">
    <div class="lightbox-content">
        <span class="lightbox-close">&times;</span>
        <img id="lightbox-img" src="" alt="Enlarged image">
    </div>
</div>

<style>
/* Lightbox Styles */
.lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox-content {
    position: relative;
    max-width: 90%;
    max-height: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.lightbox-close {
    position: fixed;
    top: 20px;
    right: 20px;
    color: white;
    font-size: 40px;
    font-weight: bold;
    cursor: pointer;
    z-index: 1001;
    user-select: none;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.lightbox-close:hover {
    opacity: 0.7;
}

/* Make gallery images clickable */
.gallery-img {
    cursor: pointer;
    transition: opacity 0.2s;
}

.gallery-img:hover {
    opacity: 0.8;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const closeBtn = document.querySelector('.lightbox-close');
    const galleryImages = document.querySelectorAll('.gallery-img');

    // Add click event to each gallery image
    galleryImages.forEach((img) => {
        img.addEventListener('click', function() {
            showLightbox(this.dataset.full);
        });
    });

    function showLightbox(src) {
        lightboxImg.src = src;
        lightbox.style.display = 'flex';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    function hideLightbox() {
        lightbox.style.display = 'none';
        document.body.style.overflow = 'auto'; // Restore scrolling
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
</script>
"""
    return results

def main():
    """Main function to generate photo gallery."""
    photos = process_photos()
    html_content = generate_html(photos)

    # Save the HTML content to a file
    with open(OUTPUT, 'w') as file:
        file.write(html_content)

    print(f"Generated gallery with {len(photos)} photos.")

if __name__ == "__main__":
    main()
