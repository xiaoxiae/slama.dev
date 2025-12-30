import {Layout, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const rectangles = Array.from({length: 3}, () => createRef<Rect>());

    // we can use any of the names from the X11 color standard!
    // a nice website for picking colors: https://x11.linci.co/
    const rectangleColors = ['crimson', 'forestgreen', 'deepskyblue'];

    const layout = createRef<Layout>();

    view.add(
        <Layout layout gap={50} ref={layout}>
            {rectangles.map((ref, i) =>
                <Rect
                    ref={ref} opacity={0} stroke={rectangleColors[i]}
                    lineWidth={5} size={300}
                />
            )}
        </Layout>
    )

    yield* sequence(0.15, ...rectangles.map(ref => appear(ref())));

    // scale the entire group
    yield* all(
        layout().scale(1.5, 1),
        layout().position.y(-200, 1),
    )

    // suppress the layout for a while and remember the positions
    layout().children().forEach(ref => ref.save())
    layout().layout(false);
    layout().children().forEach(ref => ref.restore())

    // now we can move it
    yield* rectangles[1]().position.y(300, 1);

    // layout doesn't have attributes of the children, so setting colors on it won't work
    yield* all(...rectangles.map(ref => ref().stroke('white', 1)));
    yield* all(...rectangles.map(ref => ref().fill('white', 1)));
});