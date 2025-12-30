import {Circle, Latex, Line, makeScene2D, Txt} from '@motion-canvas/2d';
import {all, createDeferredEffect, createRef, delay, Reference, sequence, Vector2} from '@motion-canvas/core';
import {appear} from "../../utilities";

/**
 * Cross product of two 3D points.
 */
function cross(a: [number, number, number], b: [number, number, number]): [number, number, number] {
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    ];
}

/**
 * Calculate intersection coordinates of two lines.
 */
function lineIntersection(p1: Vector2, p2: Vector2, p3: Vector2, p4: Vector2): Vector2 {
    const pad = (point: Vector2): [number, number, number] => [point.x, point.y, 1];

    const line1Padded = [pad(p1), pad(p2)];
    const line2Padded = [pad(p3), pad(p4)];

    const line1Cross = cross(line1Padded[0], line1Padded[1]);
    const line2Cross = cross(line2Padded[0], line2Padded[1]);

    const intersection = cross(line1Cross, line2Cross);
    const [x, y, z] = intersection;

    // Return the intersection point in the xy-plane
    return new Vector2(x / z, y / z);
}

/**
 * Calculate the bisector of a given line segment.
 */
function perpendicularBisector(p1: Vector2, p2: Vector2): [Vector2, Vector2] {
    const diff = p1.sub(p2);

    let direction = cross([diff.x, diff.y, 0], [0, 0, 1]);
    let directionVector = new Vector2(direction[0], direction[1]);

    const midpoint = p1.add(p2).div(2);

    return [midpoint.add(directionVector), midpoint.sub(directionVector)];
}

/**
 * Calculate the position for the label of the given circle to always point towards the center of the triangle.
 */
function getLabelPosition(circle: Reference<Circle>, circles: Array<Reference<Circle>>): Vector2 {
    let center = new Vector2();

    circles.forEach(c => {
        center = center.add(c().position())
    });

    center = center.div(circles.length);

    const vector = circle().position().sub(center).normalized;

    return circle().position().add(vector.mul(70));
}


export default makeScene2D(function* (view) {
    const circles = Array.from({length: 3}, () => createRef<Circle>());
    const positions = [new Vector2(0, -300), new Vector2(-300, 200), new Vector2(300, 200)];

    const labels = Array.from({length: 3}, () => createRef<Txt>());
    const labelStrings = ['a', 'b', 'c'];

    const lines = Array.from({length: 3}, () => createRef<Line>());

    view.add(
        <>
            {circles.map((ref, i) =>
                <Circle
                    ref={ref} opacity={0} size={30} fill={'white'}
                    position={positions[i]}
                />
            )}
            {lines.map((ref, i) =>
                // always keep the lines on adjacent circles
                <Line
                    points={[circles[i]().position, circles[(i + 1) % circles.length]().position]}
                    ref={ref} stroke={'white'}
                    lineWidth={8} size={30}
                    end={0}
                />
            )}
            {labels.map((ref, i) =>
                // always keep the label away from the center of the triangle
                <Latex
                    tex={labelStrings[i]}
                    ref={ref} fill={'white'}
                    opacity={circles[i]().opacity}
                    scale={circles[i]().scale}
                    position={() => getLabelPosition(circles[i], circles)}
                    fontSize={70}
                />
            )}
        </>
    )

    const circumscribedCircle = createRef<Circle>();
    view.add(
        <Circle ref={circumscribedCircle}
                size={30} lineWidth={5} start={1} stroke={'red'} zIndex={-1}/>
    )

    // change the center and size of the circumscribed circle to be within the bisectors
    createDeferredEffect(() => {
        let position = lineIntersection(
            ...perpendicularBisector(circles[0]().position(), circles[1]().position()),
            ...perpendicularBisector(circles[1]().position(), circles[2]().position()),
        );

        let size = position.sub(circles[0]().position()).magnitude;

        circumscribedCircle().position(position);
        circumscribedCircle().size(size * 2);
    })

    // nice appearing
    yield* all(
        sequence(0.25, ...circles.map(ref => appear(ref()))),
        delay(
            0.5,
            sequence(0.25, ...lines.map(ref => ref().end(1, 0.5))),
        ),

        delay(
            1.5,
            circumscribedCircle().start(0, 1),
        )
    );

    // move circles
    yield* all(
        ...circles.map((ref, i) => ref().position(circles[(i + 1) % circles.length]().position(), 1))
    );

    // move circles again
    yield* all(
        circles[0]().position(circles[0]().position().addX(-100), 1),
        circles[1]().position(circles[1]().position().addX(100).addY(-300), 1),
        circles[2]().position(circles[2]().position().addY(100), 1),
    );
});
