import {Circle, Layout, makeScene2D} from '@motion-canvas/2d';
import {all, createRef, sequence, useRandom} from '@motion-canvas/core';
import {appear} from "../../utilities";
import chroma from 'chroma-js';

export default makeScene2D(function* (view) {
    let random = useRandom(0xdeadbeef);

    const circles = Array.from({length: 12 ** 2}, () => createRef<Circle>());
    const layout = createRef<Layout>();

    // we can use chroma.js for nice color shenanigans
    // we're using the lightness-chroma-hue for a nicer-looking scale
    let colors = chroma.scale(['#fafa6e', '#2A4858']).mode('lch')
        .colors(circles.length)

    view.add(
        <Layout layout gap={50} ref={layout} wrap={'wrap'} width={1400}
                alignItems={'center'}
        >
            {circles.map((ref, i) =>
                <Circle
                    x={random.nextInt(-600, 600)}
                    y={random.nextInt(-300, 300)}
                    ref={ref} opacity={0} stroke={colors[i]}
                    lineWidth={5} size={random.nextInt(10, 50)}
                />
            )}
        </Layout>
    )

    layout().children().forEach(ref => ref.save())
    layout().layout(false);

    yield* sequence(0.01, ...circles.map(ref => appear(ref())));

    yield* sequence(
        0.01,
        ...circles.map(ref => all(ref().restore(1), ref().opacity(1, 1))),
    );

    layout().layout(true);

    yield* all(
        layout().gap(30, 1),
        layout().width(1200, 1),
    );

    yield* all(
        layout().gap(60, 1),
        layout().width(1600, 1),
    );
});