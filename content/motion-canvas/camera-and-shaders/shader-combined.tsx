import {Circle, makeScene2D} from '@canvas-commons/2d';
import {createRef, waitFor} from '@canvas-commons/core';

import shader from './shader.glsl';
import shaderCombined from './shader-combined.glsl';

import {appear} from "../../utilities";

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
