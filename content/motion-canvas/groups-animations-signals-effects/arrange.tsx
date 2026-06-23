import {Circle, Layout, makeScene2D, Shape} from '@canvas-commons/2d';
import {all, createRef, sequence, useRandom, ThreadGenerator} from '@canvas-commons/core';

/**
 * Animate the appearance of an object.
 */
function* appear(object: Shape, duration = 1): ThreadGenerator {
    let scale = object.scale();

    yield* all(
        object.scale(0).scale(scale, duration),
        object.opacity(0).opacity(1, duration),
    );
}

export default makeScene2D(function* (view) {
    let random = useRandom(0xdeadbeef);

    const circles = Array.from({length: 15}, () => createRef<Circle>());
    const layout = createRef<Layout>();

    view.add(
        <Layout layout gap={50} ref={layout} alignItems={'center'}>
            {circles.map((ref, i) =>
                <Circle
                    x={random.nextInt(-700, 700)}
                    y={random.nextInt(-300, 300)}
                    ref={ref} opacity={0} stroke={'red'}
                    lineWidth={5} size={random.nextInt(10, 100)}
                />
            )}
        </Layout>
    )

    layout().children().forEach(ref => ref.save())
    layout().layout(false);

    yield* sequence(0.05, ...circles.map(ref => appear(ref())));

    yield* sequence(0.05,
        ...circles.map(ref => all(
            ref().restore(1),
            ref().opacity(1, 1)
        )),
    );

    layout().layout(true);

    // some layout properties are not supported yet :(
    // https://github.com/motion-canvas/motion-canvas/issues/363
    yield* all(
        layout().gap(10, 1),
        layout().direction('column', 1),
    );
});
