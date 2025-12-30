import {Layout, makeScene2D, Rect} from '@motion-canvas/2d';
import {all, Color, createRef, delay, Reference, useRandom} from '@motion-canvas/core';
import chroma from "chroma-js";


/**
 * A nicer interpolation of colors using the 'lab' color space.
 */
export function colorLerp(from: any, to: any, value: number) {
    return Color.lerp(from, to, value, 'lab');
}

/**
 * Shuffle an array (deterministically).
 */
function shuffle<T>(array: T[]): T[] {
    let random = useRandom();

    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(random.nextFloat() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }

    return array;
}

export default makeScene2D(function* (view) {
    const inputString = `
#######################################################
#  #################            ##                    #
# ##################           ####                   #
# #################            ####                   #
#  ###############             #####               # ##
#      #########               #####               ####
#         ###                  ######            ######
#          ###            ##   #####    ###       #####
#          ####      ########   ####  #####        ## #
#          #####   ##########   ###  ########       # #
#         #####   ###########        ########         #
#         ####   ###########        ##########        #
#        ##      ###########        ##########        #
#      ####     ############      #############       #
#    ######     ############     #############        #
# #########  ## ###########     #########    #        #
# ############### #########     #######               #
# ###############   ######      ######                #
# ###############    #####       ####                 #
#   #############      #                ##            #
#     #  #######                       ########### ####
#          ###         #              #################
# ##                  ####            #################
#####                ######          ##################
######                ######         ##################
# ###      ###        #######  ###   ###############  #
#         ####         ############   ####  #######   #
#        #####          ############          ###     #
#         ###            ##########                   #
#######################################################`;

    const lines = inputString.trim().split('\n');
    const grid: string[][] = lines.map(line => line.split('').map(char => char));

    const gridReferences: Reference<Rect>[][] = grid.map(line => line.map(_ => createRef<Rect>()));

    let cols = gridReferences[0].length;
    let rows = gridReferences.length;

    let width = 1600;
    let gap = 1;

    view.add(
        <Layout layout width={width} wrap={'wrap'} gap={gap}>
            {
                ...gridReferences.flat().map(
                    (ref, i) => <Rect
                        ref={ref} size={(width - gap * (cols - 1)) / cols}
                        fill={(grid[Math.floor(i / cols)][i % cols] == '#') ? 'white' : 'black'}
                        lineWidth={gap + 1}
                        stroke={'rgb(255, 255, 255)'}
                        opacity={0}
                    />
                )
            }
        </Layout>
    )

    yield* all(
        ...shuffle(gridReferences.flat()).map((ref, i) => delay(0.0001 * i, ref().opacity(1, 1)))
    );

    const distances: number[][] = grid.map(line => line.map(_ => 0));

    const queue: [[number, number], number][] = [[[1, 1], 0]];
    const visited: Set<string> = new Set();  // what the fuck!?!?

    while (queue.length > 0) {
        const [[x, y], steps] = queue.shift()!;

        distances[y][x] = steps;

        if (visited.has(`${x},${y}`))
            continue;

        if (grid[y][x] == "#")
            continue;

        visited.add(`${x},${y}`);

        const moves = [
            [0, -1], // Up
            [0, 1], // Down
            [-1, 0], // Left
            [1, 0], // Right
        ];

        for (const [dx, dy] of moves) {
            const [nx, ny] = [x + dx, y + dy];

            if (!(nx >= 0 && nx < cols && ny >= 0 && ny < rows))
                continue

            queue.push([[nx, ny], steps + 1]);
        }
    }

    let maxDistance = distances.flat().reduce((a, b) => Math.max(a, b));

    let colors = chroma.scale(["#ef476f", "#ffd166", "#06d6a0", "#118ab2"]).colors(maxDistance + 1);

    yield* all(
        ...gridReferences.flat().map(
            (ref, i) => {
                let x = i % cols;
                let y = Math.floor(i / cols);

                let distance = distances[y][x];
                let color = grid[y][x] == "#" ? 'white' : colors[distance];

                return delay(0.05 * distance, ref().fill(color, 1, undefined, colorLerp));
            }
        )
    )
});
