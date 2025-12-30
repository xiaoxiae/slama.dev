import {Latex, makeScene2D, Txt} from '@motion-canvas/2d';
import {all, createRef} from '@motion-canvas/core';
import {appear} from "../../utilities";

export default makeScene2D(function* (view) {
    const text = createRef<Txt>();
    const math = createRef<Latex>();

    view.add(<>
        // text is empty for now since we're animating writing it
        <Txt ref={text} fill={"white"} x={-300}></Txt>

        // we're separating things to be diffed with double braces
        <Latex ref={math} fill={"white"} x={300} tex={"{{\\sum_{i = 0}}}{{^\\infty}} {{\\frac{1}{2^i}}} = {{2}}"}></Latex>
    </>)

    yield* all(
        text().text("Hello Motion Canvas!", 1),
        appear(math(), 1),
    );

    // can be diffed!
    yield* all(
        text().text("Hello everyone!", 1),
        math().tex("{{\\sum_{i = 0}}}{{^{42}}} {{\\frac{1}{2^i}}} = {{13}}", 1),
    );
});
