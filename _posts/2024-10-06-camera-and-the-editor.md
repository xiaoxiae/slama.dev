---
title: Camera and the Editor
category: "Motion Canvas"
category_icon: /assets/category-icons/motion-canvas.svg
category_part: 3
css: motioncanvas photos manim
redirect_from:
- /motion-canvas/3/
end: <a href="/motion-canvas/1/">Part 1</a>, <a href="/motion-canvas/2/">Part 2</a>, <strong>→ Part 3 ←</strong>
hidden: true
---

- .
{:toc}

### Camera

#### Controlling

#### Multi-camera

### Editor

#### Timing animations

#### Waiting for events

<script>
const toggleButtons = document.querySelectorAll('button');

toggleButtons.forEach(button => {
  button.addEventListener('click', function() {
    const parentSection = this.parentElement;

    let childDivs = parentSection.querySelectorAll('.ct');

    if (childDivs[0].style.display === 'none') {
      childDivs[0].style.display = 'block';
      childDivs[1].style.display = 'none';
    } else {
      childDivs[0].style.display = 'none';
      childDivs[1].style.display = 'block';
    }

    childDivs = parentSection.querySelectorAll('.bt');

    if (childDivs[0].style.display === 'none') {
      childDivs[0].style.display = 'block';
      childDivs[1].style.display = 'none';
    } else {
      childDivs[0].style.display = 'none';
      childDivs[1].style.display = 'block';
    }
  });
});
</script>
