// Ghost movement configuration
const ghostConfig = {
  // Animation timing
  updateInterval: 10, // milliseconds

  // Velocity-based movement
  maxVelocity: 50, // pixels per second
  accelerationRate: 0.8, // how quickly velocity changes direction
  waypointChangeInterval: 3000, // milliseconds between picking new waypoints

  // Boundary constraints
  boundaryOffset: 25,
  ghostSize: 60, // font-size of the ghost emoji

  // Opacity based on distance from cursor
  maxOpacity: 0.5,
  maxDistanceForOpacity: 800,

  // Ghost caught behavior
  bobFrequency: 3,
  bobAmplitude: 10,
  caughtDuration: 5, // seconds
};

// Mapping of navbar names and icons for halloween mode
const halloweenNameMapping = {
  Home: "Castle",
  Reading: "Tomes",
  CV: "Scripture",
  Climbing: "Adventure",
  Photos: "Negatives",
  Videos: "Horror",
  Stickers: "Stamps",
  "source code": "ancient manuscripts",
  "privacy policy": "blood oath",
};

const halloweenIconMapping = {
  // Maps original icon class to halloween icon class
  "fa-house": "fa-chess-rook",
  "fa-book": "fa-book-skull",
  "fa-id-card": "fa-scroll",
  "fa-bolt": "fa-person-hiking",
  "fa-camera": "fa-camera-retro",
  "fa-youtube": "fa-video",
  "fa-note-sticky": "fa-stamp",
};

// Icon family mappings (for converting between fa-brands, fa-solid, etc.)
const halloweenIconFamilyMapping = {
  "fa-youtube": { toFamily: "fa-solid", fromFamily: "fa-brands" },
};

// Author name mapping for footer
const halloweenAuthorMapping = {
  "Tomáš Sláma": '<em>the ArchMage <i class="fa-solid fa-hat-wizard"></i></em>',
};

function getCookie(name) {
  const nameEQ = name + "=";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.indexOf(nameEQ) === 0) {
      return cookie.substring(nameEQ.length);
    }
  }
  return null;
}

function setCookie(name, value, days = 365) {
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = "expires=" + date.toUTCString();
  document.cookie = name + "=" + value + ";" + expires + ";path=/";
}

function applyNavbarNameMapping() {
  const isHalloween = getCookie("halloween-mode") === "true";
  const navbarItems = document.querySelectorAll(".navbar-text a");

  navbarItems.forEach((link) => {
    // Handle icon mapping
    const iconElement = link.querySelector("i");
    if (iconElement) {
      const classes = Array.from(iconElement.classList);
      classes.forEach((cls) => {
        // Check if this is an original icon that needs halloween mapping
        if (halloweenIconMapping[cls]) {
          const mappedIcon = halloweenIconMapping[cls];
          if (isHalloween) {
            iconElement.classList.replace(cls, mappedIcon);
            // Handle family conversion if needed
            if (halloweenIconFamilyMapping[cls]) {
              const familyMap = halloweenIconFamilyMapping[cls];
              iconElement.classList.replace(
                familyMap.fromFamily,
                familyMap.toFamily,
              );
            }
          }
        } else {
          // Check if this is a halloween icon that needs to be reversed
          for (let [original, halloween] of Object.entries(
            halloweenIconMapping,
          )) {
            if (cls === halloween && !isHalloween) {
              iconElement.classList.replace(halloween, original);
              // Handle family conversion back if needed
              if (halloweenIconFamilyMapping[original]) {
                const familyMap = halloweenIconFamilyMapping[original];
                iconElement.classList.replace(
                  familyMap.toFamily,
                  familyMap.fromFamily,
                );
              }
              break;
            }
          }
        }
      });
    }

    // Handle name mapping
    for (let node of link.childNodes) {
      if (node.nodeType === Node.TEXT_NODE) {
        const currentText = node.textContent.trim();
        const mappedName = halloweenNameMapping[currentText];

        // Check if this is an original name that needs halloween mapping
        if (isHalloween && mappedName) {
          node.textContent = " " + mappedName;
        } else if (!isHalloween) {
          // Check if this is a halloween name that needs to be reversed
          for (let [original, halloween] of Object.entries(
            halloweenNameMapping,
          )) {
            if (currentText === halloween) {
              node.textContent = " " + original;
              break;
            }
          }
        }
        break; // Only replace the first text node
      }
    }
  });
}

function applyAuthorNameMapping() {
  const isHalloween = getCookie("halloween-mode") === "true";
  const authorElement = document.getElementById("author-name");

  if (authorElement) {
    const currentState = authorElement.getAttribute("data-halloween");

    for (let [original, halloween] of Object.entries(halloweenAuthorMapping)) {
      if (isHalloween && currentState !== "true") {
        authorElement.innerHTML = halloween;
        authorElement.setAttribute("data-halloween", "true");
      } else if (!isHalloween && currentState === "true") {
        authorElement.innerHTML = original;
        authorElement.setAttribute("data-halloween", "false");
      }
    }
  }
}

function applyFooterLinkMapping() {
  const isHalloween = getCookie("halloween-mode") === "true";
  const footerLinks = document.querySelectorAll("footer a");

  footerLinks.forEach((link) => {
    for (let [original, halloween] of Object.entries(halloweenNameMapping)) {
      if (
        original === "Home" ||
        original === "Reading" ||
        original === "CV" ||
        original === "Climbing" ||
        original === "Photos" ||
        original === "Videos" ||
        original === "Stickers"
      ) {
        // Skip navbar mappings
        continue;
      }

      const currentText = link.textContent.trim();
      if (isHalloween && currentText === original) {
        link.textContent = halloween;
      } else if (!isHalloween && currentText === halloween) {
        link.textContent = original;
      }
    }
  });
}

function applyHalloweenTheme() {
  const isHalloween = getCookie("halloween-mode") === "true";
  const root = document.documentElement;
  if (isHalloween) {
    root.classList.add("halloween");
  } else {
    root.classList.remove("halloween");
  }
}

function toggleHalloween() {
  const root = document.documentElement;
  const isCurrentlyHalloween = root.classList.contains("halloween");

  if (isCurrentlyHalloween) {
    setCookie("halloween-mode", "false");
    root.classList.remove("halloween");
  } else {
    setCookie("halloween-mode", "true");
    root.classList.add("halloween");
  }
  applyNavbarNameMapping();
  applyAuthorNameMapping();
  applyFooterLinkMapping();
  updateGhostCursorVisibility();
}

function updateGhostCursorVisibility() {
  const ghostCursor = document.getElementById("ghost-cursor");
  const isHalloween = getCookie("halloween-mode") === "true";
  ghostCursor.style.display = isHalloween ? "block" : "none";
}

// Ghost cursor position tracking (in percentage coordinates)
let ghostXPercent = 50; // percentage of window width
let ghostYPercent = 50; // percentage of window height
let velocityX = 0;
let velocityY = 0;
let targetXPercent = 50; // percentage of window width
let targetYPercent = 50; // percentage of window height
let cursorX = window.innerWidth; // Start cursor position far away
let cursorY = window.innerHeight;
let ghostCaught = false;
let caughtTime = 0;
let lastWaypointChange = 0;

// Spawn ghost at random location or load from storage
function spawnGhostRandomly() {
  const offsetPercent = (ghostConfig.boundaryOffset / window.innerWidth) * 100;
  const savedState = localStorage.getItem("ghostState");

  if (savedState) {
    const state = JSON.parse(savedState);
    ghostXPercent = state.xPercent;
    ghostYPercent = state.yPercent;
    velocityX = state.vx;
    velocityY = state.vy;
  } else {
    ghostXPercent = Math.random() * (100 - 2 * offsetPercent) + offsetPercent;
    ghostYPercent = Math.random() * (100 - 2 * offsetPercent) + offsetPercent;
    velocityX = 0;
    velocityY = 0;
  }
}

// Save ghost state (position and velocity) to localStorage
function saveGhostState() {
  localStorage.setItem(
    "ghostState",
    JSON.stringify({
      xPercent: ghostXPercent,
      yPercent: ghostYPercent,
      vx: velocityX,
      vy: velocityY,
    }),
  );
}

// Create wavy text animation
function createWavyText(text) {
  const letters = text.split("");
  const time = Date.now() / 200; // Speed of wave animation
  return letters
    .map((letter, index) => {
      const yOffset = Math.sin(index * 0.4 + time) * 5; // Amplitude of 5px, animated wave
      const charDisplay = letter === " " ? "&nbsp;" : letter;
      return `<span style="display: inline-block; transform: translateY(${yOffset}px);">${charDisplay}</span>`;
    })
    .join("");
}

// Generate random waypoint within screen bounds
function generateRandomWaypoint() {
  const offsetPercent = (ghostConfig.boundaryOffset / window.innerWidth) * 100;
  targetXPercent = Math.random() * (100 - 2 * offsetPercent) + offsetPercent;
  targetYPercent = Math.random() * (100 - 2 * offsetPercent) + offsetPercent;
  lastWaypointChange = Date.now();
}

// Track cursor position
document.addEventListener("mousemove", function (e) {
  cursorX = e.clientX;
  cursorY = e.clientY;
});

// Handle window resize - no scaling needed with percentage-based coordinates
window.addEventListener("resize", function () {
  // Percentage-based coordinates remain valid across all window sizes
  // Just ensure the ghost stays within bounds
  const offsetPercent = (ghostConfig.boundaryOffset / window.innerWidth) * 100;
  const maxXPercent = 100 - offsetPercent;
  const maxYPercent = 100 - offsetPercent;

  // Clamp positions to boundaries
  ghostXPercent = Math.max(offsetPercent, Math.min(maxXPercent, ghostXPercent));
  ghostYPercent = Math.max(offsetPercent, Math.min(maxYPercent, ghostYPercent));
  targetXPercent = Math.max(offsetPercent, Math.min(maxXPercent, targetXPercent));
  targetYPercent = Math.max(offsetPercent, Math.min(maxYPercent, targetYPercent));

  // Save the new state to localStorage
  saveGhostState();
});

// Set ghost target to cursor on click
document.addEventListener("mousedown", function (e) {
  targetXPercent = (e.clientX / window.innerWidth) * 100;
  targetYPercent = (e.clientY / window.innerHeight) * 100;
  lastWaypointChange = Date.now();

  // Add visual indicator
  const ghostCursor = document.getElementById("ghost-cursor");
  if (ghostCursor && ghostCursor.style.display !== "none") {
    // Flash effect by changing opacity
    ghostCursor.style.opacity = "0.8";
    setTimeout(() => {
      ghostCursor.style.opacity = ghostConfig.maxOpacity;
    }, 100);
  }
});

// Detect if device has cursor (not mobile)
function hasCursor() {
  return !(navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0);
}

// Initialize ghost animation after DOM loads
function initGhostAnimation() {
  const ghostCursor = document.getElementById("ghost-cursor");
  const ghostText = document.getElementById("ghost-text");

  if (!ghostCursor || !ghostText) return;

  // Spawn ghost at random location
  spawnGhostRandomly();
  // Generate initial waypoint
  generateRandomWaypoint();

  // Animate ghost with velocity-based movement
  setInterval(function () {
    if (ghostCursor && ghostCursor.style.display !== "none") {
      // Check if we need a new waypoint based on time interval
      if (
        Date.now() - lastWaypointChange >=
        ghostConfig.waypointChangeInterval
      ) {
        generateRandomWaypoint();
      }

      // Always move towards current target, regardless of distance
      // This ensures smoother movement even before waypoint is reached

      // Calculate direction to target (in percentage space)
      const dxPercent = targetXPercent - ghostXPercent;
      const dyPercent = targetYPercent - ghostYPercent;
      const distancePercent = Math.sqrt(dxPercent * dxPercent + dyPercent * dyPercent);

      // Update velocity towards target
      if (distancePercent > 0.5) {
        const dirX = dxPercent / distancePercent;
        const dirY = dyPercent / distancePercent;
        velocityX += dirX * ghostConfig.accelerationRate;
        velocityY += dirY * ghostConfig.accelerationRate;

        // Limit velocity to max (scaled for percentage coordinates)
        const currentSpeed = Math.sqrt(
          velocityX * velocityX + velocityY * velocityY,
        );
        if (currentSpeed > ghostConfig.maxVelocity) {
          const scale = ghostConfig.maxVelocity / currentSpeed;
          velocityX *= scale;
          velocityY *= scale;
        }
      }
      // Ghost continues with momentum towards waypoint
      // Velocity naturally decreases via air resistance (not explicitly decelerated)

      // Apply repulsive force from borders
      const offsetPercent = (ghostConfig.boundaryOffset / window.innerWidth) * 100;
      const repulsionRangePercent = (150 / window.innerWidth) * 100; // Distance at which repulsion starts
      const repulsionStrength = 0.2;

      // Left/Right borders
      if (ghostXPercent < offsetPercent + repulsionRangePercent) {
        const repulsion =
          (1 - (ghostXPercent - offsetPercent) / repulsionRangePercent) * repulsionStrength;
        velocityX += repulsion;
      } else if (ghostXPercent > 100 - offsetPercent - repulsionRangePercent) {
        const repulsion =
          (1 - (100 - offsetPercent - ghostXPercent) / repulsionRangePercent) *
          repulsionStrength;
        velocityX -= repulsion;
      }

      // Top/Bottom borders
      if (ghostYPercent < offsetPercent + repulsionRangePercent) {
        const repulsion =
          (1 - (ghostYPercent - offsetPercent) / repulsionRangePercent) * repulsionStrength;
        velocityY += repulsion;
      } else if (ghostYPercent > 100 - offsetPercent - repulsionRangePercent) {
        const repulsion =
          (1 - (100 - offsetPercent - ghostYPercent) / repulsionRangePercent) *
          repulsionStrength;
        velocityY -= repulsion;
      }

      // Update position (always, whether caught or not) - convert velocity to percentage change
      const deltaTime = ghostConfig.updateInterval / 1000;
      const velocityXPercent = (velocityX / window.innerWidth) * 100;
      const velocityYPercent = (velocityY / window.innerHeight) * 100;
      ghostXPercent += velocityXPercent * deltaTime;
      ghostYPercent += velocityYPercent * deltaTime;

      // Hard bounds to prevent going off-screen
      ghostXPercent = Math.max(offsetPercent, Math.min(100 - offsetPercent, ghostXPercent));
      ghostYPercent = Math.max(offsetPercent, Math.min(100 - offsetPercent, ghostYPercent));

      // Position using percentages with CSS
      ghostCursor.style.left = ghostXPercent + "%";
      ghostCursor.style.top = ghostYPercent + "%";
      ghostCursor.style.transform = "translate(-50%, -50%)";

      if (!ghostCaught) {
        // Save state periodically (every 500ms to avoid excessive writes)
        if (Math.random() < 0.05) {
          saveGhostState();
        }

        // Calculate distance to cursor and adjust opacity (only on devices with cursor)
        if (hasCursor()) {
          // Convert ghost percentage position to pixels for distance calculation
          const ghostPixelX = (ghostXPercent / 100) * window.innerWidth;
          const ghostPixelY = (ghostYPercent / 100) * window.innerHeight;
          const distanceToCursor = Math.sqrt(
            Math.pow(ghostPixelX - cursorX, 2) + Math.pow(ghostPixelY - cursorY, 2),
          );
          const maxDistance = ghostConfig.maxDistanceForOpacity;
          const opacity = Math.max(
            0,
            Math.min(
              ghostConfig.maxOpacity,
              ghostConfig.maxOpacity * (1 - distanceToCursor / maxDistance),
            ),
          );
          ghostCursor.style.opacity = opacity;
        } else {
          // On mobile without cursor, keep ghost at 0.5 opacity
          ghostCursor.style.opacity = 0.5;
        }
      } else {
        // When caught, show message and remain fully opaque
        ghostCursor.style.opacity = 1;

        // Update countdown
        caughtTime -= ghostConfig.updateInterval / 1000;
        const secondsLeft = Math.max(0, Math.ceil(caughtTime));
        const displayText = hasCursor()
          ? secondsLeft > 0
            ? "Goooot your cursoooor (" + secondsLeft + "s)"
            : "Got your cursor lmao"
          : "Leave me alooone!";
        ghostText.innerHTML = createWavyText(displayText);

        // Release cursor after configured duration
        if (caughtTime <= 0) {
          ghostCaught = false;
          document.body.style.setProperty("cursor", "auto", "important");
          // Reset cursor on all elements
          document.querySelectorAll("*").forEach((el) => {
            el.style.removeProperty("cursor");
          });
          ghostText.style.display = "none";
        }
      }
    }
  }, ghostConfig.updateInterval); // Update interval from config

  // Detect hover on ghost to steal cursor (desktop with cursor)
  ghostCursor.addEventListener("mouseenter", function () {
    if (!ghostCaught && ghostCursor.style.display !== "none" && hasCursor()) {
      ghostCaught = true;
      caughtTime = ghostConfig.caughtDuration;
      document.body.style.setProperty("cursor", "none", "important");
      // Also set cursor: none on all elements
      document.querySelectorAll("*").forEach((el) => {
        el.style.setProperty("cursor", "none", "important");
      });
      ghostText.style.display = "block";
    }
  });

  // Detect click on ghost (mobile devices without cursor)
  ghostCursor.addEventListener("click", function () {
    if (!ghostCaught && ghostCursor.style.display !== "none") {
      ghostCaught = true;
      caughtTime = ghostConfig.caughtDuration;
      ghostText.style.display = "block";
    }
  });
}

// Start animation when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initGhostAnimation);
} else {
  initGhostAnimation();
}

// Apply theme immediately (synchronous, runs before body renders)
applyHalloweenTheme();
