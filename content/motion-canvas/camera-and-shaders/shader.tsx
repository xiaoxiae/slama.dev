import {Circle, makeScene2D} from '@motion-canvas/2d';
import {createRef, waitFor} from '@motion-canvas/core';

import shader from './shader.glsl';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const circle = createRef<Circle>();

    view.add(
        <Circle
            size={400}
            lineWidth={50}
            ref={circle}
            shaders={shader}
            fill={'rgb(255,0,0)'}
            stroke={'rgba(200,0,0,0.5)'}
        />
    );

    yield* appear(circle(), 2);
    yield* waitFor(3);
});
