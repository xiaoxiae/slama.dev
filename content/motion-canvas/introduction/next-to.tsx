import {Circle, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const rectangle = createRef<Rect>();
    view.add(<Rect ref={rectangle} size={[600, 300]} stroke={'white'} lineWidth={5}/>);

    // array construct to create multiple objects
    const circles = Array.from({length: 4}, () => createRef<Circle>());

    // forEach syntax to add them all to the scene
    circles.forEach((ref) => {
        view.add(<Circle ref={ref} size={150} stroke={'white'} lineWidth={5}/>);
    });

    // map syntax for showing all elements
    yield* all(
        appear(rectangle()),
        ...circles.map(ref => appear(ref()))
    );

    // move the circles such that they surround the rectangle
    // use sequence instead of all for a delayed set of animations (it pretty :)
    yield* sequence(
        0.15,  // delay between animations
        circles[0]().right(rectangle().left().addX(-50), 1),
        circles[1]().bottom(rectangle().top().addY(-50), 1),
        circles[2]().left(rectangle().right().addX(50), 1),
        circles[3]().top(rectangle().bottom().addY(50), 1),
    );
});