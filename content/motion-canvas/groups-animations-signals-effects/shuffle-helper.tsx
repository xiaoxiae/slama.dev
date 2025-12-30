import {Circle, makeScene2D, Spline} from '@motion-canvas/2d';
import {createRef, createSignal, easeInOutExpo} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
    const spline = createRef<Spline>();
    const progress = createSignal(0);

    view.add(
        <>
            <Spline
                ref={spline}
                lineWidth={8}
                stroke={'white'}
                points={[[-500, 0], [0, -250], [500, 0]]}
                smoothness={1}
            />
            <Circle
                size={100}
                fill={'white'}
                position={() => spline().getPointAtPercentage(progress()).position}
            />,
        </>,
    );

    yield* progress(1, 2, easeInOutExpo);
});