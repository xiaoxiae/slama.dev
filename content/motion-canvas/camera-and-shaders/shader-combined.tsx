import {Circle, makeScene2D, Shape} from '@canvas-commons/2d';
import {createRef, waitFor, all, ThreadGenerator} from '@canvas-commons/core';

import shader from './shader.glsl';
import shaderCombined from './shader-combined.glsl';


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

    view.add(
        <Circle
            size={400}
            lineWidth={50}
            ref={circle}
            shaders={[{fragment: shader}, {fragment: shaderCombined}]}
            fill={'rgb(255,0,0)'}
            stroke={'rgba(200,0,0,0.5)'}
        />
    );

    yield* appear(circle(), 2);
    yield* waitFor(3);
});
