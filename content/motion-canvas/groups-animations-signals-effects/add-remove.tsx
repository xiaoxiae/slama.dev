import {Circle, Layout, makeScene2D, Polygon, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence, Vector2, waitFor} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    // start with a square
    const square = createRef<Rect>();
    view.add(<Rect ref={square} fill={'white'} size={300}/>);

    yield* waitFor(1);

    // will be added to the very top (i.e. will now be the _last child of root_)
    const circle = createRef<Circle>();
    view.add(<Circle ref={circle} fill={'red'} size={350}/>);

    yield* waitFor(1);

    // this moves the object "to the bottom" (i.e. below the square)
    // this means that it will be the _first child of root_
    circle().moveToBottom();

    yield* waitFor(1);

    // circle: hi again!
    circle().moveToTop();

    yield* waitFor(1);

    // this is a bit more interesting; we move to the bottom, but also
    // increase the Z-index, which is the more important parameter wrt. rendering
    //
    // circle: I'm staying on top!
    circle().moveToBottom();
    circle().zIndex(10);
    circle().fill('blue');

    yield* waitFor(1);

    // circle: *dies*
    circle().remove();

    yield* waitFor(1);
});