import {Circle, makeScene2D, Spline} from '@motion-canvas/2d';
import {createDeferredEffect, createRef, createSignal, loop, sequence, useRandom, Vector2} from '@motion-canvas/core';
import {appear} from "../../utilities";
import chroma from 'chroma-js';

export default makeScene2D(function* (view) {
    let random = useRandom(0xdeadbef2);

    // random circles at random base positions
    const circles = Array.from({length: 8 ** 2}, () => createRef<Circle>());
    const basePositions = Array.from({length: 8 ** 2}, () => new Vector2(random.nextInt(-600, 600), random.nextInt(-300, 300)));

    const circle = createRef<Circle>();

    let colors = chroma.scale(['#fafa6e', '#2A4858']).mode('lch')
        .colors(circles.length)

    view.add(
        <>
            <Circle ref={circle} fill={'white'}/>
            {
                circles.map((ref, i) =>
                    <Circle
                        x={basePositions[i].x}
                        y={basePositions[i].y}
                        ref={ref}
                        stroke={colors[i]} fill={colors[i]}
                        lineWidth={5} size={15}
                    />
                )
            }
        </>
    )

    circles.forEach(ref => ref().opacity(0));
    yield* sequence(0.01, ...circles.map(ref => appear(ref())));

    // create a repulsion force around the white circle
    createDeferredEffect(() => {
        circles.forEach((ref, i) => {
            const pos = basePositions[i];

            const vector = pos.sub(circle().position())

            const direction = vector.normalized;
            const distance = vector.magnitude;

            const strength = 1 / 50;

            // we need to push at least as much as the radius of the circle (to not collide)
            const pushStrength = Math.max(
                Math.sqrt(distance) * circle().width() * strength,
                circle().width(),
            )

            const pushVector = pos.add(direction.mul(pushStrength));

            ref().position(pushVector);
        });
    })

    yield* circle().size(100, 1);

    // move it using a nice hand-crafted spline :)
    const spline = createRef<Spline>();
    const progress = createSignal(0);

    let h = 150;
    let w = 400;

    view.add(
        <Spline
            ref={spline}
            points={[[0, 0], [0, -h], [-w, -h], [-w, h], [w, h], [w, -h], [0, -h], [0, 0]]}
            smoothness={0.6}
        />
    )

    circle().position(() => spline().getPointAtPercentage(progress()).position)

    // loop the size scaling indefinitely in the background to make the dots pulse
    // do this 3 times (loop can take a number of times :)
    yield loop(3, () => circle().size(50, 1).to(100, 1))

    yield* progress(1, 10);
});
