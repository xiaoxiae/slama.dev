import {Circle, makeScene2D} from '@motion-canvas/2d';
import {all, createRef, Vector2} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const circles = Array.from({length: 3}, () => createRef<Circle>());

    circles.forEach((ref, i) => {
        view.add(<Circle ref={ref} size={(1 + i) * 100} stroke={'white'} lineWidth={5}/>);
    });

    yield* all(...circles.map(ref => appear(ref())));

    // align squares next to one another
    yield* all(
        circles[0]().left(circles[1]().right().addX(25), 1),
        circles[2]().right(circles[1]().left().addX(-25), 1),
    );

    // align c1 and c2 such that their bottoms are the same as c2
    yield* all(
        circles[0]().bottom(new Vector2(circles[0]().position.x(), circles[1]().bottom().y), 1),
        circles[2]().bottom(new Vector2(circles[2]().position.x(), circles[1]().bottom().y), 1),
    );

    // align all circles such that their top touches a line going through the point
    yield* all(...circles.map(ref => ref().top(new Vector2(ref().top().x, -300), 1)));
});