import {Camera, Circle, Layout, makeScene2D, Polygon, Rect} from '@motion-canvas/2d';
import {all, createRef} from '@motion-canvas/core';


export default makeScene2D(function* (view) {
    const camera = createRef<Camera>();

    const circle = createRef<Circle>();
    const square = createRef<Rect>();
    const pentagon = createRef<Polygon>();

    // the scene must be set up in this way -- camera as the root, displaying its children
    view.add(
        <Camera ref={camera}>
            <Layout layout gap={50} alignItems={'center'}>
                <Circle ref={circle} size={200} stroke={'blue'} lineWidth={5} scale={0} />
                <Rect ref={square} size={300} stroke={'white'} lineWidth={5} scale={0} />
                <Polygon ref={pentagon} size={200} sides={5} stroke={'red'} lineWidth={5} scale={0} />
            </Layout>
        </Camera>
    );

    // for some reason, opacity doesn't play nice with Camera atm :(
    // that's why we're not using our standard appear animation
    //
    // https://github.com/motion-canvas/motion-canvas/issues/1057
    yield* square().scale(1, 1);

    yield* camera().zoom(1.5, 1);

    yield* all(
        circle().scale(1, 1),
        camera().centerOn(circle(), 1),
    );

    yield* all(
        pentagon().scale(1, 2),
        camera().zoom(camera().zoom() * 1.5, 2),
        camera().centerOn(pentagon(), 2),
        camera().rotation(180, 2),
    )

    // reset back to default
    yield* camera().reset(2);
});