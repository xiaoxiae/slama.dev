"""Generate lightext SVG images from markdown files.

Lightext encodes text into colorful SVG patterns where characters are represented
by gradient-colored shapes based on their frequency in the source text.
"""

import hashlib
import re
import string
import sys
from collections import defaultdict
from pathlib import Path

import svgwrite


def count_characters(text: str) -> dict[str, int]:
    """Count ASCII letter frequencies in text."""
    histogram = defaultdict(int)
    target_chars = set(string.ascii_letters)

    for char in text.lower():
        if char in target_chars:
            histogram[char] += 1

    return histogram


def get_encoding(text: str) -> dict[str, tuple[int, ...]]:
    """Build character encoding based on frequency.

    Most frequent characters get the most distinct patterns.
    Encoding uses 4 bits: 1 for shape (full/half), 3 for RGB color.
    """
    histogram = sorted(count_characters(text).items(), key=lambda x: -x[1])

    encoding = {}
    i = 0
    idx = 0
    over = False

    while idx < len(histogram):
        char = histogram[idx][0]

        # Skip value 0 (must have some light)
        if i & 0b111 == 0:
            i += 1
            continue

        encoding[char] = (i, (i & 0b0111) if not over else (i & 0b1111))
        idx += 1
        i += 1

        if i >= 14:
            i = 0
            over = True

    # Special characters
    encoding[","] = (14, 14)
    encoding[" "] = (15,)
    encoding["."] = (15, 15)

    return encoding


def get_sequence(sentence: str, encoding: dict) -> list:
    """Convert sentence to visual sequence using encoding."""
    sequence = []

    for char in sentence.lower():
        if char not in encoding:
            continue

        bits = encoding[char]

        if isinstance(bits, tuple):
            for bit in bits:
                sequence.append(
                    (
                        (bit & 0b1000) >> 3,
                        (
                            (bit & 0b100) >> 2,
                            (bit & 0b10) >> 1,
                            (bit & 0b1),
                        ),
                    )
                )
        else:
            sequence.append(bits)

    return sequence


def save_svg(path: Path, sequence: list) -> None:
    """Save sequence as SVG file."""

    def format_color(rgb: tuple) -> str:
        return f"rgb({rgb[0] * 255}, {rgb[1] * 255}, {rgb[2] * 255})"

    def get_element(dwg, i: int, pair: tuple, c1: tuple, c2: tuple):
        if pair == (1, 0):
            c1, c2 = c2, c1

        gradient = dwg.defs.add(
            dwg.linearGradient(id=f"grad{i}", start=("0%", "50%"), end=("100%", "50%"))
        )
        gradient.add_stop_color(0, format_color(c1))
        gradient.add_stop_color(1, format_color(c2))

        if pair == (1, 1):
            return dwg.rect(
                insert=(i * square_size[0], 0), size=square_size, fill=f"url(#grad{i})"
            )
        elif pair == (0, 0):
            return dwg.rect(
                insert=(i * square_size[0], square_size[0]),
                size=(square_size[0], square_size[1] * 0.5),
                fill=f"url(#grad{i})",
            )
        elif pair == (0, 1):
            return dwg.path(
                d="M 0.250114,9.1067087e-7 V 0.99942311 C 0.1277849,0.99997481 "
                "0.1216577,0.74967071 0,0.74982601 V 0.24959811 C 0.1216577,0.24975341 "
                "0.1277849,-5.5078933e-4 0.250114,9.1067087e-7 Z",
                fill=f"url(#grad{i})",
                transform=f"translate({i * square_size[0]}, 0)",
            )
        else:
            return dwg.path(
                d="M 0.250114,9.1067087e-7 V 0.99942311 C 0.1277849,0.99997481 "
                "0.1216577,0.74967071 0,0.74982601 V 0.24959811 C 0.1216577,0.24975341 "
                "0.1277849,-5.5078933e-4 0.250114,9.1067087e-7 Z",
                fill=f"url(#grad{i})",
                transform=f"translate({(i + 1) * square_size[0]}, 0) scale(-1, 1)",
            )

    square_size = (0.25, 1)
    dwg = svgwrite.Drawing(
        str(path),
        profile="tiny",
        size=((len(sequence) - 1) * square_size[0], square_size[1]),
    )

    for i in range(len(sequence) - 1):
        if isinstance(sequence[i], str) or isinstance(sequence[i + 1], str):
            continue

        pair = (sequence[i][0], sequence[i + 1][0])
        c1 = sequence[i][1]
        c2 = sequence[i + 1][1]

        dwg.add(get_element(dwg, i, pair, c1, c2))

    dwg.save()


def process_markdown(md_path: Path) -> None:
    """Process markdown file and generate lightext SVGs.

    Finds {{< lightext "text" >}} shortcodes and generates corresponding SVGs.
    The shortcode handles rendering; this just generates the image files.
    """
    content = md_path.read_text()
    output_dir = md_path.parent

    # Extract story text for character frequency analysis
    # Remove YAML front matter and HTML tags
    story_text = re.sub(r"^---.*?---", "", content, flags=re.DOTALL)
    story_text = re.sub(r"<[^>]+>", "", story_text)
    story_text = re.sub(r"\{\{<.*?>}}", "", story_text)

    encoding = get_encoding(story_text)

    # Find all lightext tags: {{< lightext "text" >}}
    pattern = r'\{\{<\s*lightext\s+"([^"]+)"\s*>\}\}'
    matches = list(re.finditer(pattern, content))

    if not matches:
        print(f"No lightext tags found in {md_path}")
        return

    # Generate SVGs (hash-based naming so shortcode can find them)
    for match in matches:
        sentence = match.group(1)
        # Use short hash of sentence for filename
        text_hash = hashlib.md5(sentence.encode()).hexdigest()[:8]
        svg_name = f"lightext-{text_hash}.svg"
        svg_path = output_dir / svg_name

        sequence = get_sequence(sentence, encoding)
        save_svg(svg_path, sequence)
        print(f"Generated {svg_path}: {sentence!r}")


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run scripts/lightext.py <markdown_file>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    if not md_path.exists():
        print(f"File not found: {md_path}")
        sys.exit(1)

    process_markdown(md_path)


if __name__ == "__main__":
    main()
