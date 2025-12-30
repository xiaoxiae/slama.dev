import { Layout, makeScene2D, Rect, Shape } from "@motion-canvas/2d";
import {
  all,
  createRef,
  Reference,
  sequence,
  ThreadGenerator,
  useRandom,
} from "@motion-canvas/core";

/**
 * Set colors for the rectangles.
 * @param i First highlighted rectangle.
 * @param j Second highlighted rectangle.
 * @param sortedStart Where the sorted array starts.
 */
function* setColors(
  rectangles: Array<Reference<Shape>>,
  i: number,
  j: number,
  duration: number,
  sortedStart: number,
): ThreadGenerator {
  yield* all(
    ...rectangles.map((ref, idx) => {
      if (idx >= sortedStart) {
        return ref().fill("rgb(89,255,79)", duration);
      } else if (idx == i || idx == j) {
        return ref().fill("yellow", duration);
      } else {
        return ref().fill("white", duration);
      }
    }),
  );
}

/**
 * Swap the two rectangles.
 * @param i First rectangle to swap.
 * @param j Second rectangle to swap.
 */
function* swap(
  rectangles: Array<Reference<Shape>>,
  i: number,
  j: number,
  duration: number,
): ThreadGenerator {
  yield* all(
    rectangles[i]().height(rectangles[j]().height(), duration),
    rectangles[j]().height(rectangles[i]().height(), duration),
  );
}

export default makeScene2D(function* (view) {
  let random = useRandom();
  let n = 20;

  const rectangles = Array.from({ length: n }, () => createRef<Rect>());
  const values = Array.from({ length: n }, () => random.nextFloat());

  const layout = createRef<Layout>();
  view.add(
    <Layout
      layout
      ref={layout}
      gap={20}
      width={1400}
      height={800}
      alignItems={"end"}
    >
      {rectangles.map((ref) => (
        // if the width is not set, fucky things happen... idk man
        // I think this is a flexbox thing that I don't understand yet
        <Rect
          ref={ref}
          grow={1}
          width={(1400 - (n - 1) * 20) / 20}
          stroke={"white"}
          fill={"white"}
        />
      ))}
    </Layout>,
  );

  yield* sequence(
    0.025,
    ...rectangles.map((ref, i) =>
      ref().height(values[i] * layout().height(), 1),
    ),
  );

  let speedSlow = 0.5;
  let speedFast = 0.07;

  // bubble sort go brrrrrrrr
  for (let i = 0; i < n - 1; i++) {
    let swapped = false;

    let speed = i == 0 ? speedSlow : speedFast;

    for (let j = 0; j < n - i - 1; j++) {
      yield* setColors(rectangles, j, j + 1, speed, n - i);

      if (values[j] > values[j + 1]) {
        // Swap elements
        [values[j], values[j + 1]] = [values[j + 1], values[j]];
        yield* swap(rectangles, j, j + 1, speed);
        swapped = true;
      }
    }

    // If no two elements were swapped in the inner loop, then the array is already sorted.
    if (!swapped) break;
  }

  yield* setColors(rectangles, 0, 1, 1, -1);
});
