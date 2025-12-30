import {Camera, Circle, Layout, makeScene2D} from '@motion-canvas/2d';
import {all, createRef, sequence, useRandom, Vector2} from '@motion-canvas/core';
import chroma from 'chroma-js';


export default makeScene2D(function* (view) {
    let random = useRandom(0xdeadbeef);

    const circles = Array.from({length: 12 ** 2}, () => createRef<Circle>());
    const layout = createRef<Layout>();

    let colors = chroma.scale(['#fafa6e', '#2A4858']).mode('lch').colors(circles.length)

    const camera = createRef<Camera>();

    view.add(
        // initially, the circle we're following's position is undefined, so we'll default to 0,0
        <Camera ref={camera} position={() => (circles[30]().position() ?? new Vector2(0, 0))}>
            <Layout layout gap={50} ref={layout} wrap={'wrap'} width={1400}
                    alignItems={'center'}
            >
                {circles.map((ref, i) =>
                    <Circle
                        x={random.nextInt(-600, 600)}
                        y={random.nextInt(-300, 300)}
                        ref={ref} stroke={colors[i]} fill={colors[i]}
                        lineWidth={5} size={random.nextInt(10, 50)}
                    />
                )}
            </Layout>
        </Camera>
    )

    layout().children().forEach(ref => ref.save())
    layout().layout(false);

    circles.forEach(ref => ref().scale(0));
    yield* all(
        camera().scale(0).scale(1, 3),
        sequence(0.01, ...circles.map(ref => ref().scale(1, 1))),
    );

    yield* sequence(
        0.001,
        ...circles.map(ref => all(ref().restore(1), ref().opacity(1, 1))),
    );

    layout().layout(true);

    yield* all(
        layout().gap(30, 2),
        layout().width(1200, 2),
    );

    yield* all(
        layout().gap(60, 2),
        layout().width(1600, 2),
    );
});