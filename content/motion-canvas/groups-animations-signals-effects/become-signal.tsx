import {Circle, Layout, makeScene2D, Rect, Txt, Node, Latex, Shape} from '@canvas-commons/2d';
import {all, createEaseInOutBack, createRef, sequence, useRandom, Vector2, ThreadGenerator} from '@canvas-commons/core';

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
    const circle = createRef<Circle>();
    const text = createRef<Txt>();

    view.add(
        <>
            <Circle ref={circle} stroke={'white'} lineWidth={5} size={300}/>
            <Latex ref={text} fill={'white'}
                // make the properties of text based on functions of the signals of the circle
                   tex={() => `p = [${circle().x().toFixed(0)}, ${circle().y().toFixed(0)}]`}
                   opacity={circle().opacity}
                   scale={circle().scale}
                   bottom={() => circle().top().addY(-30)}
            />
        </>
    );

    yield* appear(circle());

    yield* circle().position.x(100, 1);

    yield* all(
        circle().position(new Vector2(-200, -100), 1),
        circle().scale(1.25, 1),
    )

    yield* all(
        circle().position(new Vector2(0, 300), 1),
        circle().scale(.5, 1),
    )

    yield* all(
        circle().position(new Vector2(0, 0), 1),
        circle().scale(1, 1),
    )
});
