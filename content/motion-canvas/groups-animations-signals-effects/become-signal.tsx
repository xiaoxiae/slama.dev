import {Circle, Layout, makeScene2D, Rect, Txt, Node, Latex} from '@motion-canvas/2d';
import {all, createEaseInOutBack, createRef, sequence, useRandom, Vector2} from '@motion-canvas/core';
import {appear} from "../../utilities";

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
