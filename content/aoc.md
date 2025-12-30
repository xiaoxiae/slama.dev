---
title: Advent of Code
layout: default
noHeading: true
hidden: true
---

{{< aoc >}}

<script>
document.querySelectorAll('.aoc-silver, .aoc-gray, .aoc-gold').forEach((element) => {
  // Get the class name dynamically (either 'aoc-silver', 'aoc-gray', or 'aoc-gold')
  const className = element.classList.contains('aoc-silver') ? 'aoc-silver' : element.classList.contains('aoc-gray') ? 'aoc-gray' : 'aoc-gold';

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
