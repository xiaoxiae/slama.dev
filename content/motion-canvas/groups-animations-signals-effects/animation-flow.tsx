import {Layout, makeScene2D, Rect, Txt} from '@motion-canvas/2d';
import {all, any, chain, createRef, delay, loop, sequence, waitFor} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const rectangles = Array.from({length: 3}, () => createRef<Rect>());
    const rectangleColors = ['crimson', 'forestgreen', 'deepskyblue'];

    const text = createRef<Txt>();

    view.add(
        <Layout gap={50} fontSize={100} layout direction={'column'} alignItems={'center'}>
            <Txt ref={text} fill={'white'}></Txt>
            <Layout layout gap={50}>
                {rectangles.map((ref, i) =>
                    <Rect
                        ref={ref} opacity={0} stroke={rectangleColors[i]}
                        lineWidth={5} size={300}
                    />
                )}
            </Layout>
        </Layout>
    )

    yield* text().text('sequence(t, ...)', 1)

    // sequence: launch animations in a delayed sequence
    yield* sequence(
        0.15, ...rectangles.map(ref => appear(ref()))
    );

    yield* text().text('all(...)', 1)

    // all: launch all animations together
    yield* all(
        ...rectangles.map(ref => ref().opacity(0, 1))
    )

    yield* text().text('chain(...)', 1)

    // chain: launch animations one after another
    yield* chain(
        rectangles[0]().opacity(1, 0.5),
        rectangles[1]().opacity(1, 1),
        rectangles[2]().opacity(1, 0.25),
    )

    yield* text().text('delay(t, .)', 1)

    // delay: launch animations with a delay
    // we can also nest!
    yield* all(
        delay(0.6, rectangles[0]().opacity(0, 1)),
        delay(0.3, rectangles[1]().opacity(0, 1)),
        delay(0.9, rectangles[2]().opacity(0, 1)),
    )

    // any: continue when at least one finishes!!!
    yield* text().text('any(...)', 1)

    yield* any(
        delay(1, rectangles[0]().opacity(1, 1)),
        delay(0.25, rectangles[1]().opacity(1, 1)),
        delay(2, rectangles[2]().opacity(1, 1)),
    )

    yield* text().text('one finished!', 1)

    yield* waitFor(1);

    yield* text().text('loop(...)', 1)

    // loop: starts an infinite animation; expects an animation factory to do this
    // because of this, we have to use yield (without star!), running this in the background
    yield loop(
        () => rectangles[1]().opacity(0, 0.25).to(1, 0.25),
    )

    yield* waitFor(1);

    // we can, however, still animate some of its other properties!
    yield* all(
        rectangles[1]().scale(0.5, 3),
        text().text('change while looping!', 1),
    );
});
