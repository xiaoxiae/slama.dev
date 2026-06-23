import {makeScene2D, Rect, Shape} from '@canvas-commons/2d';
import {all, createRef, delay, ThreadGenerator} from '@canvas-commons/core';

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
    const rect = createRef<Rect>();
    view.add(<Rect ref={rect} size={320} fill={'red'} stroke={'red'} lineWidth={10} x={-300}/>);

    yield* appear(rect());

    let n = 5;

    yield* all(
        // change position
        rect().x(300, n),

        // at the same time as scale
        delay(
            n / 4,
            // we can chain two scale changes by using .to()
            rect().scale(1.5, n / 4).to(1, n / 4),
        ),

        // at the same time as rotation
        delay(
            n / 8 * 3,
            rect().rotation(-90, n / 4).to(90, n / 4),
        ),
    );
});