import {Circle, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence} from '@motion-canvas/core';


export default makeScene2D(function* (view) {
    // create square and circle objects
    const rect = createRef<Rect>();
    view.add(<Rect ref={rect} size={320} stroke={'red'} lineWidth={10} x={-300}/>);

    const circle = createRef<Circle>();
    view.add(<Circle ref={circle} size={320} stroke={'blue'} lineWidth={10} x={300}/>);

    // the first call is instant, while the second produces an animation
    yield* all(
        rect().scale(0).scale(1, 1),
        rect().opacity(0).opacity(1, 1),
        circle().scale(0).scale(1, 1),
        circle().opacity(0).opacity(1, 1),
    );

    // fading them from the scene
    // sequence() plays the animations with a delay
    yield* sequence(
        0.25,
        rect().opacity(0, 1),
        circle().opacity(0, 1),
    );
});