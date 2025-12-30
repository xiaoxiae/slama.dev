import {Latex, Layout, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence, Vector2} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const rectangles = Array.from({length: 3}, () => createRef<Rect>());
    const numbers = Array.from({length: 3}, () => createRef<Latex>());

    // create the layout to place the things into
    const layout = createRef<Layout>();
    view.add(<Layout layout ref={layout} gap={50}>
        {rectangles.map((ref, i) =>
            <Rect ref={ref} grow={1} size={300} stroke={'white'} lineWidth={5}
                  justifyContent={'center'} alignItems={'center'}
            >
                <Latex tex={`${i}`}
                       ref={numbers[i]} fill={'white'}
                       scale={4} opacity={0}/>
            </Rect>
        )}
    </Layout>)

    // save this state of nodes (they should end up like this)
    rectangles.forEach(ref => ref().save())

    // disable the layout, moving the rects back to origin
    // in reality, their position has always been (0, 0),
    // but the layout previously dictated their position
    layout().layout(false);

    // scatter them around the screen to make it look cooler
    rectangles[0]().scale(0.5)
    rectangles[0]().position(new Vector2(100, 200))
    rectangles[0]().rotation(30)
    rectangles[0]().opacity(0)

    rectangles[1]().scale(0.7)
    rectangles[1]().position(new Vector2(-50, -100))
    rectangles[1]().rotation(230)
    rectangles[1]().opacity(0)

    rectangles[2]().scale(0.4)
    rectangles[2]().position(new Vector2(-200, 150))
    rectangles[2]().rotation(-150)
    rectangles[2]().opacity(0)

    yield* sequence(0.15, ...rectangles.map(ref => appear(ref())));

    // restoring them (in an animated way) returns them to the layout,
    // since we're restoring the absolute values of its attributes
    yield* all(...rectangles.map(ref => ref().restore(1)));

    // now we can re-enable the layout, since nothing will change
    layout().layout(true);

    yield* sequence(0.15, ...numbers.map(ref => appear(ref())));

    // since they're in a flexbox, we can do cool flexbox stuff!
    yield* all(
        layout().width(1200, 1),
        ...rectangles.map((ref, i) => ref().height(100 * (i + 3), 1)),
    )
});