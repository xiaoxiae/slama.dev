import {Camera, FlexDirection, Latex, Layout, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, easeInOutExpo, Reference, Vector2, waitFor} from '@motion-canvas/core';


function getSquare(ref: Reference<Rect>, value: number) {
    let size = value * 100;

    return <Rect
        ref={ref}
        lineWidth={10}
        size={size}
        stroke={'white'}
        alignItems={'center'}
        justifyContent={'center'}
    >
        <Latex fontSize={size * 0.5} fill={'white'} tex={`${value}^2`}></Latex>
    </Rect>;
}

export default makeScene2D(function* (view) {
    // let line = createRef<Line>();
    // let circle = createRef<Circle>();
    // let progress = createSignal(0);
    // let orbit = new Vector2();
    // // effect for rotating around a point
    // createDeferredEffect(() => {
    //     if (circle() === undefined)
    //         return;
    //     let alpha = progress() * 2 * Math.PI;
    //     let vector = new Vector2(Math.cos(alpha), Math.sin(alpha));
    //     let magnitude = orbit.sub(circle().position()).magnitude;
    //     circle().position(vector.mul(magnitude));
    // })
    // // effect for drawing a line
    // createDeferredEffect(() => {
    //     if (line() === undefined)
    //         return;
    //     line().add(<Knot position={circle().position()}/>)
    // })
    // view.add(
    //     <>
    //         <Circle ref={circle} x={300} size={50} fill={'white'}/>
    //         <Spline ref={line} lineWidth={10} stroke={'white'} zIndex={-1} smoothness={0}/>
    //     </>
    // )
    // yield* progress(1, 1);

    const camera = createRef<Camera>();
    let layout = createRef<Layout>();

    view.add(
        <Camera ref={camera}>
            <Layout layout ref={layout} alignItems={'center'}/>
        </Camera>
    )

    let firstSquare = createRef<Rect>();
    layout().add(getSquare(firstSquare, 1));
    yield* firstSquare().scale(0).scale(1, 1, easeInOutExpo);

    let directions: Array<FlexDirection> = ['row', 'column-reverse', 'row-reverse', 'column'];

    let a = 1, b = 1, n = 7;
    for (let i = 0; i < n; i++) {
        b = b + a;
        a = b - a;

        // new rectangle
        let newSquare = createRef<Rect>();
        layout().add(getSquare(newSquare, a));
        layout().remove();

        // new layout in the current direction
        let newLayout = createRef<Layout>();
        camera().add(
            <Layout layout direction={directions[(i + 1) % directions.length]}
                    ref={newLayout} alignItems={'center'}>
                {layout()}
            </Layout>
        );

        newSquare().save();

        yield* all(
            newSquare().size(new Vector2(0, 0)).restore(1, easeInOutExpo),
            newSquare().children()[0].scale(0).scale(1, 1, easeInOutExpo),
        );

        layout = newLayout;
    }

    // # create the squares
    // a = 1
    // b = 1
    // directions = [RIGHT, UP, LEFT, DOWN]
    // for i in range(n):
    // b = b + a
    // a = b - a

    // direction = directions[i % 4]

    // new_square = self.create_square(a).next_to(squares, direction, buff=0)
    // squares.add(new_square)

    // self.play(
    //     FadeIn(new_square, shift=direction * a / 3),
    //     self.get_camera_centering_animation(squares),
    // )

});