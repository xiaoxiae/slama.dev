import {Camera, Circle, makeScene2D, Node, Rect, Spline} from '@motion-canvas/2d';
import {
    all,
    createDeferredEffect,
    createRef,
    createSignal,
    loop,
    sequence,
    useRandom,
    Vector2
} from '@motion-canvas/core';
import chroma from 'chroma-js';

export default makeScene2D(function* (view) {
    let random = useRandom(0xdeadbef2);

    const circles = Array.from({length: 8 ** 2}, () => createRef<Circle>());
    const basePositions = Array.from({length: 8 ** 2}, () => new Vector2(random.nextInt(-600, 600), random.nextInt(-300, 300)));

    let colors = chroma.scale(['#fafa6e', '#2A4858']).mode('lch')
        .colors(circles.length)

    // we got two cameras now
    const mainCamera = createRef<Camera>();
    const sideCamera = createRef<Camera>();

    // we also want to animate where the side camera is looking
    // these objects will visualize where the side camera is focused on
    const circle = createRef<Circle>();
    const circleCameraRect = createRef<Rect>();

    const sideWidth = view.width() / 6;
    const sideHeight = view.height() / 6;
    const sideZoom = 1.5;

    // for multi-camera stuff, we need a node that we'll pass to the cameras
    let scene = <Node>
        <Circle ref={circle} fill={'white'}/>
        <Rect ref={circleCameraRect}
              lineWidth={3} stroke={'#444'}
              scale={0} size={[sideWidth, sideHeight]}
              position={circle().position}
              radius={10}
        />
        {
            circles.map((ref, i) =>
                <Circle
                    x={basePositions[i].x}
                    y={basePositions[i].y}
                    ref={ref}
                    stroke={colors[i]} fill={colors[i]}
                    lineWidth={5} size={15}
                    rotation={random.nextInt(0, 360)}
                />
            )
        }
    </Node>;

    // add the cameras, both of which will look at the same node
    view.add(
        <>
            <Camera.Stage
                cameraRef={mainCamera}
                scene={scene}
                size={[view.width(), view.height()]}
            />
            <Camera.Stage
                cameraRef={sideCamera}
                scene={scene}
                size={[sideWidth, sideHeight]}
                position={new Vector2(view.width() / 2, -view.height() / 2)
                    .sub(new Vector2(sideWidth / 2 * sideZoom, -sideHeight / 2 * sideZoom))
                    .sub(new Vector2(50, -50))}
                stroke={'#aaa'}
                fill={'000a'}
                scale={0}
                lineWidth={3}
                radius={10}
                smoothCorners
            />
        </>,
    );

    // the side camera should keep looking at the circle
    sideCamera().position(circle().position);

    // show circles
    circles.forEach(ref => ref().scale(0));
    yield* sequence(0.01, ...circles.map(ref => ref().scale(1, 1)));

    // create a repulsion force around the white circle
    createDeferredEffect(() => {
        circles.forEach((ref, i) => {
            const pos = basePositions[i];

            const vector = pos.sub(circle().position())

            const direction = vector.normalized;
            const distance = vector.magnitude;

            const strength = 1 / 50;

            // we need to push at least as much as the radius of the circle (to not collide)
            const pushStrength = Math.max(
                Math.sqrt(distance) * circle().width() * strength,
                circle().width(),
            )

            const pushVector = pos.add(direction.mul(pushStrength));

            ref().position(pushVector);
        });
    })

    // to animate appearing the side camera, we need a reference **to its rectangle**
    // this is because Camera.Stage is a shorthand for the following:
    //
    // <Rect >  // want to get reference to this!
    //   <Camera ref={sideCamera} scene={scene} />
    // </Rect>
    //
    // using ref={...} doesn't work at the moment (likely a bug), so we do this instead
    const rect = view.children()[view.children.length - 1];

    yield* all(
        circle().size(100, 1),
        rect.scale(0).scale(sideZoom, 1),
        circleCameraRect().scale(1, 1),
    );

    // move it using a nice hand-crafted spline :)
    const spline = createRef<Spline>();
    const progress = createSignal(0);

    let h = 150;
    let w = 400;

    view.add(
        <Spline
            ref={spline}
            points={[[0, 0], [0, -h], [-w, -h], [-w, h], [w, h], [w, -h], [0, -h], [0, 0]]}
            smoothness={0.6}
        />
    )

    circle().position(() => spline().getPointAtPercentage(progress()).position)

    // loop the size scaling indefinitely in the background to make the dots pulse
    // also loop the camera
    yield loop(() => circle().size(50, 1).to(100, 1))

    yield* progress(1, 10);
});
