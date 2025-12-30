import {Circle, Layout, Rect, makeScene2D} from '@motion-canvas/2d';
import {all, createRef} from '@motion-canvas/core';

export default makeScene2D(function* (view) {
    // yoinked directly from the documentation, not my code!

    const col1 = createRef<Layout>();
    const col3 = createRef<Layout>();
    const redBox = createRef<Layout>();

    view.add(
        <Layout layout gap={10} padding={30} width={1000} height={600}>
            <Rect ref={col1} grow={1} fill={'#242424'} radius={20}/>
            <Layout gap={10} direction="column" grow={3}>
                <Rect
                    ref={redBox}
                    grow={8}
                    fill={'red'}
                    radius={50}
                    stroke={'#fff'}
                    lineWidth={10}
                    margin={5}
                    justifyContent={'center'}
                    alignItems={'center'}
                >
                    <Circle width={20} height={20} fill={'#fff'}/>
                </Rect>
                <Rect grow={2} fill={'#242424'} radius={20}/>
            </Layout>
            <Rect ref={col3} grow={3} fill={'#242424'} radius={20}/>
        </Layout>
    );

    yield* all(col3().grow(1, 0.8), col1().grow(2, 0.8));
    yield* redBox().grow(1, 0.8);
    yield* all(col3().grow(3, 0.8), col1().grow(1, 0.8));
    yield* redBox().grow(8, 0.8);
});