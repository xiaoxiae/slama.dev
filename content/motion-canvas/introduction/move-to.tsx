import {Latex, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, createRef, sequence} from '@motion-canvas/core';
import {appear} from "../../utilities";


export default makeScene2D(function* (view) {
    const rectangles = Array.from({length: 3}, () => createRef<Rect>());
    const numbers = Array.from({length: 3}, () => createRef<Latex>());

    rectangles.forEach((ref) => {
        view.add(<Rect ref={ref} size={300} stroke={'white'} lineWidth={5}/>);
    });

    yield* all(...rectangles.map(ref => appear(ref())));

    // align squares next to one another
    yield* all(
        rectangles[0]().right(rectangles[1]().left().addX(-50), 1),
        rectangles[2]().left(rectangles[1]().right().addX(50), 1),
    );

    // forEach can also take a second argument, which is the index!
    // set opacity to 0 to initially hide them
    numbers.forEach(
        (ref, i) => {
            view.add(<Latex tex={`${i}`} ref={ref} fill={'white'} scale={4} opacity={0}/>);
        }
    );

    // move the numbers to each of the squares
    numbers.forEach((ref, i) => {
        ref().position(rectangles[i]().position())
    })

    yield* sequence(
        0.15,
        ...numbers.map(ref => appear(ref()))
    );
});