import {Knot, makeScene2D, Spline} from '@motion-canvas/2d';
import {all, createRef, Reference, Vector2} from '@motion-canvas/core';


export default makeScene2D(function* (view) {
    const getSpline = (ref: Reference<Spline>, positions: Vector2[]) => {
        return <Spline
            ref={ref}
            lineWidth={5}
            stroke={'white'}
            smoothness={0}
            end={0}
        >
            {positions.map(pos => (<Knot position={pos}/>))}
        </Spline>
    }

    let size = 300;
    let iterations = 3;

    let line = createRef<Spline>();

    let positions = [new Vector2(-size, size), new Vector2(-size, -size), new Vector2(size, -size), new Vector2(size, size)];

    view.add(getSpline(line, positions))

    yield* line().end(1, 1);

    // not pretty code, but not sure how to do this cleaner / clearer
    for (let i = 1; i <= iterations; i++) {
        let lineRef = line().clone();
        lineRef.opacity(0);
        view.add(lineRef)

        let newSegmentScale = (2 ** (i) - 1) / (2 ** (i + 1) - 1)

        yield* all(
            line().scale(newSegmentScale, 1),
            line().topLeft(line().topLeft(), 1),
            line().stroke('gray', 1)
        )

        let l2 = line().clone();
        view.add(l2);

        yield* all(
            l2.topRight(lineRef.topRight(), 1),
        )

        let l3 = line().clone();
        let l4 = l2.clone();

        view.add(l3);
        view.add(l4);

        yield* all(
            l3.bottomRight(lineRef.bottomLeft(), 1),
            l3.rotation(90, 1),
            l4.bottomLeft(lineRef.bottomRight(), 1),
            l4.rotation(-90, 1),
        )

        let newPositionKnots = [
            ...l3.children().reverse(),
            ...line().children(),
            ...l2.children(),
            ...l4.children().reverse(),
        ]

        let newPositions = newPositionKnots.map(pos => pos.absolutePosition().sub(lineRef.absolutePosition()));

        let newLine = createRef<Spline>();

        view.add(getSpline(newLine, newPositions))

        yield* newLine().end(1, 1);

        line().remove();
        l2.remove();
        l3.remove();
        l4.remove();

        line = newLine;
    }
});
