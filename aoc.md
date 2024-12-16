---
title: Advent of Code
layout: default
css: aoc
no-heading: True
hidden: True
---

{% include aoc.md %}


<script>
document.querySelectorAll('.silver, .gray, .gold').forEach((element) => {
  // Get the class name dynamically (either 'silver', 'gray', or 'gold')
  const className = element.classList.contains('silver') ? 'silver' : element.classList.contains('gray') ? 'gray' : 'gold';

  // Randomize the animation duration (between 1 and 3 seconds)
  const randomDuration = 1 + Math.random() * 2;

  // Randomize the offset (between 0 and 1 to loop over the animation)
  const randomOffset = Math.random();

  // Apply random duration, offset, and animation name
  element.style.animationDuration = `${randomDuration}s`;
  element.style.animationTimingFunction = 'ease-in-out';
  element.style.animationIterationCount = 'infinite';
  element.style.animationName = `pulse-${className}`;
  element.style.animationDelay = `-${randomOffset * randomDuration}s`; // Offset the animation without "pausing" the start

  // Add hover effect to spin the element in a random direction
  element.addEventListener('mouseenter', () => {
    const randomRotation = Math.random() < 0.5 ? 'rotate(360deg)' : 'rotate(-360deg)';
    element.style.transition = 'transform 2s';  // Smooth transition
    element.style.transform = randomRotation;
  });
});
</script>
