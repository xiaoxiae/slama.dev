import {Circle, Layout, makeScene2D, Rect, Txt, Node} from '@motion-canvas/2d';
import {all, createRef, sequence, useRandom} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const outerSquare = createRef<Rect>();
    const innerSquare = createRef<Rect>();
    const text = createRef<Txt>();

    view.add(
        // we're using two squares, since rotation changes the position of the top
        // view the scene graph in the UI editor if it's unclear what we're doing
        <Rect ref={outerSquare} size={300}>
            <Rect ref={innerSquare} stroke={'white'} lineWidth={5} size={300}/>
        </Rect>
    );

    view.add(
        <Txt ref={text} text={"A neat square."} fill={'white'}
             // make the properties of text based on signals of the square
             opacity={outerSquare().opacity}
             bottom={outerSquare().top}
             scale={outerSquare().scale}
             padding={30}
        />
    );

    yield* appear(outerSquare());

    // we change the position of outer, dragging the text with
    yield* outerSquare().position.x(-300, 1);

    // we change the rotation of the inner, meaning that the text doesn't change
    // (it relies only on the attributes of the outer square)
    yield* innerSquare().rotation(-180, 1);

    yield* all(
        innerSquare().rotation(0, 1),
        outerSquare().scale(0.5, 1),
        outerSquare().position.x(0, 1),
    )

    // now we add another signal -- we want the text to rotate according to the outer square
    text().rotation(outerSquare().rotation);

    yield* all(
        outerSquare().rotation(-90, 1),
        outerSquare().scale(2, 1),
    )
});
