import {Circle, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, createSignal, easeInOutExpo, loop, sequence, Vector2} from '@motion-canvas/core';

import shader from './shader-advanced.glsl';


export default makeScene2D(function* (view) {
    const circle = createRef<Circle>();
    const square = createRef<Rect>();

    view.add(
        <>
            <Circle
                size={300} lineWidth={30}
                ref={circle}
                fill={'rgb(255,0,0)'} stroke={'rgb(200,0,0)'}
                x={-300}
                scale={0} opacity={0}
            />,
            <Rect
                size={300} lineWidth={30}
                ref={square}
                fill={'rgb(0,0,255)'} stroke={'rgb(0,0,200)'}
                x={300}
                scale={0} opacity={0}
            />
            <Rect
                width={1920}
                height={1080}
                shaders={ {
                    fragment: shader,
                    // notice that they are signals!
                    uniforms: {
                        aPos: circle().position,
                        aOpacity: circle().opacity,
                        aScale: circle().scale,
                        bPos: square().position,
                        bOpacity: square().opacity,
                        bScale: square().scale,
                    },
                } }
                zIndex={-1}
            />
        </>
    );

    yield* sequence(
        0.5,
        all(
            circle().scale(1, 1),
            circle().opacity(1, 1),
        ),
        all(
            square().scale(1, 1),
            square().opacity(1, 1),
        ),
    );

    // alternate sizes of object A and object B
    yield loop(() => circle().scale(0.5, 1).to(1, 1))
    yield loop(() => square().scale(1, 1).to(0.5, 1))

    // rotate a few times around origin
    let progress = createSignal(0);

    circle().position(() => Vector2.fromRadians(progress()).mul(-300));
    square().position(() => Vector2.fromRadians(progress()).mul(300));
    square().rotation(() => square().position().degrees)

    yield* progress(2 * Math.PI, 10, easeInOutExpo);
});