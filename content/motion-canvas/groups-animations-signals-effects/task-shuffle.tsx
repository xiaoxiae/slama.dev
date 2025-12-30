import {Circle, Curve, Layout, makeScene2D, Spline} from '@motion-canvas/2d';
import {
    all,
    createRef,
    createSignal,
    easeInOutExpo,
    sequence,
    ThreadGenerator,
    useRandom,
    Vector2
} from '@motion-canvas/core';
import {appear} from "../../utilities";


/**
 * Swaps the positions of two layouts in a visual view by animating them along spline paths.
 *
 * @param {Layout} view - The parent layout that contains both `a` and `b`.
 * @param {Layout} a - The first layout to be swapped.
 * @param {Layout} b - The second layout to be swapped.
 * @param duration - How long should the animation be?
 */
function* swap(view: Layout, a: Layout, b: Layout, duration: number = 1): ThreadGenerator {
    let start = a.position();
    let end = b.position();

    let mid = new Vector2().add(start).add(end).div(2);

    const progress = createSignal(0);

    let s1 = createRef<Spline>();
    let s2 = createRef<Spline>();

    let yOffset = Math.abs(a.position().x - b.position().x) / 2.5;

    view.add(<Spline ref={s1} points={[start, mid.addY(yOffset), end]} smoothness={1}/>)
    view.add(<Spline ref={s2} points={[end, mid.addY(-yOffset), start]} smoothness={1}/>)

    a.position(() => s1().getPointAtPercentage(progress()).position)
    b.position(() => s2().getPointAtPercentage(progress()).position)

    yield* progress(1, duration, easeInOutExpo);  // nicer curve :)

    // don't clutter the scene!
    s1().remove();
    s2().remove();
}

/**
 * Highlight a curve object.
 */
function* highlightCircle(object: Curve): ThreadGenerator {
    yield* all(
        object.stroke('red', 1).to('white', 1),
        object.lineWidth(20, 1).to(object.lineWidth(), 1),
        object.fill('red', 1).to('white', 1)
    );
}

export default makeScene2D(function* (view) {
    const circles = Array.from({length: 5}, () => createRef<Circle>());

    const layout = createRef<Layout>();
    view.add(<Layout layout ref={layout} gap={100}>
        {circles.map(ref =>
            <Circle ref={ref} size={170} fill={'white'} stroke={'white'} opacity={0}/>
        )}
    </Layout>)

    // position them using the layout and stop using it so we can move the nodes freely
    circles.forEach(ref => ref().save())
    layout().layout(false);
    circles.forEach(ref => ref().restore())

    yield* sequence(0.15, ...circles.map(ref => appear(ref())));

    yield* highlightCircle(circles[0]());

    let swaps = 20;
    let speedStart = 1;
    let speedEnd = 0.15;

    // use MotionCanvas' RNG so that the results are seeded
    let random = useRandom(0xdeadbeef);

    for (let i = 0; i < swaps; ++i) {
        let s1 = Math.floor(random.nextFloat() * circles.length);
        let s2;
        do {
            s2 = Math.floor(random.nextFloat() * circles.length);
        } while (s2 === s1);

        let duration = speedStart - Math.abs(speedStart - speedEnd) / swaps * i;

        yield* swap(
            view,
            circles[s1](),
            circles[s2](),
            duration,
        );
    }

    yield* highlightCircle(circles[0]());
});