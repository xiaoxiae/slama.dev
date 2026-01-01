import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Data - Jekyll first, then Hugo
labels = ["Jekyll", "Hugo"]
cached = [71.489, 3.47]
clean_additional = [265.46 - 71.489, 54.24 - 3.47]  # Additional time for clean build

# Colors - lighter for cached (base), darker for clean additional
jekyll_cached = "#e69999"
jekyll_clean = "#801a1a"
hugo_cached = "#99c2e6"
hugo_clean = "#1a4d80"

colors_cached = [jekyll_cached, hugo_cached]
colors_clean = [jekyll_clean, hugo_clean]

fig, ax = plt.subplots(figsize=(8, 6))

# Create stacked bars - cached as base, clean additional on top
bars_cached = ax.bar(labels, cached, color=colors_cached)
bars_clean = ax.bar(labels, clean_additional, bottom=cached, color=colors_clean)

# Add value labels - both above their respective sections
for i, (bar_c, bar_cl) in enumerate(zip(bars_cached, bars_clean)):
    total = cached[i] + clean_additional[i]
    # Cached value - above the cached section, colored to match
    ax.text(
        bar_c.get_x() + bar_c.get_width() / 2,
        cached[i] + 2,
        f"{cached[i]:.2f}s",
        ha="center",
        va="bottom",
        fontweight="bold",
        color=colors_cached[i],
    )
    # Total (clean) value - above the clean section, colored to match
    ax.text(
        bar_cl.get_x() + bar_cl.get_width() / 2,
        total + 2,
        f"{total:.2f}s",
        ha="center",
        va="bottom",
        fontweight="bold",
        color=colors_clean[i],
    )

ax.set_ylabel("Build Time (seconds)")
ax.set_title("Build Time Comparison: Jekyll vs Hugo")

# Custom legend with both colors side by side per framework
from matplotlib.legend_handler import HandlerBase
from matplotlib.patches import Rectangle


class TwoColorHandler(HandlerBase):
    def __init__(self, color1, color2):
        self.color1 = color1
        self.color2 = color2
        super().__init__()

    def create_artists(
        self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
    ):
        r1 = Rectangle(
            (xdescent, ydescent),
            width / 2,
            height,
            facecolor=self.color1,
            edgecolor="none",
            transform=trans,
        )
        r2 = Rectangle(
            (xdescent + width / 2, ydescent),
            width / 2,
            height,
            facecolor=self.color2,
            edgecolor="none",
            transform=trans,
        )
        return [r1, r2]


jekyll_patch = Patch(label="Jekyll (clean / cached)")
hugo_patch = Patch(label="Hugo (clean / cached)")

ax.legend(
    handles=[jekyll_patch, hugo_patch],
    handler_map={
        jekyll_patch: TwoColorHandler(jekyll_clean, jekyll_cached),
        hugo_patch: TwoColorHandler(hugo_clean, hugo_cached),
    },
    loc="upper right",
)

plt.tight_layout()
plt.savefig("build_times.svg", format="svg")
plt.savefig("build_times.png", dpi=150)
print("Saved build_times.svg and build_times.png")
