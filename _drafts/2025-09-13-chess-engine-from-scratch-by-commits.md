---
title: Chess Engine, Commit by Commit
excerpt: "Writing a chess engine from scratch, commit by commit."
css: chess
---

- .
{:toc}

A friend of mine recently challenged me to a chess engine duel, which consisted of making a chess bot from scratch and then dueling to see whose is better.
Naturally, I aggreed.
And thus **[Prokopakop](https://github.com/xiaoxiae/prokopakop)** was born.

It (unsurprisingly) turns out that there is a lot of things that go into making a chess bot, and I thought it would be interesting to cover my journey of writing the bot in the commits that I made, since they more-or-less correspond to the concepts that I learned along the way.

So, without further ado, let's write a chess bot!

### Chess

_Actually, here is a short ado of how chess rules work, for anyone not familiar with the game.
It also includes relevant terminology for the concepts covered later, so feel free to skim through even if you know chess.
[Skip if you are familiar/not interested](#move-generation)._

TODO

### Move Generation

Before beginning to write a chess bot that searches/evaluates positions, we need to make sure that we can generate them quickly, since we'll need those to search/evaluate over.

{: .commit-header}
#### [`a1f8b867`](https://github.com/xiaoxiae/Prokopakop/commit/a1f8b867c9818e411a491e8cfdbd115411f1beb1)

The first commit actually contains quite a bit of code, and should have likely been split into separate ones.
However, I wanted the first commit to actually contain something that remotely resembles a chess engine, so here we are.

##### Bitboards

The most important part of this commit is that it stored the board state position via [**bitboards**](https://www.chessprogramming.org/Bitboards), which are necessary for making the engine fast.
The concept is very simple -- since CPUs are heavily optimized for working with 64-bit numbers, and 64 turns out to be the exact number of squares on the board, we can use them to store (among other things) locations of pieces.

As an example, here is a bitboard (=64-bit unsigned integer) that stores pawn positions.

{% chess %}
0b00000000⏎     8 ........
  11111111⏎     7 ♙♙♙♙♙♙♙♙
  00000000⏎     6 ........
  00000000⏎     5 ........
  00000000⏎  →  4 ........
  00000000⏎     3 ........
  11111111⏎     2 ♟♟♟♟♟♟♟♟
  00000000      1 ........
                  abcdefgh
{% endchess %}

The main advantage of storing information in 64-bit numbers is that you can combine multiple bitboards using binary operations to obtain a particular set of squares you need.
Prokopakop stores them in the following way:

```rust
pub type Bitboard = u64;

pub enum Piece {
    Rook = 0,
    Bishop = 1,
    Queen = 2,
    Knight = 3,
    Pawn = 4,
    King = 5,
}

pub enum Color {
    Black = 0,
    White = 1,
}

pub struct Game {
    // two bitboards for black/white pieces
    pub color_bitboards: [Bitboard; Color::COUNT],

    // six bitboards for piece types
    pub piece_bitboards: [Bitboard; Piece::COUNT],

    // ...
}
```

As an example, to obtain all positions of _white rooks and bishops_, all you need to[^allyouneed] do is

```rust
let white_rooks_and_bishops = self.color_bitboards[Color::White]
                              & ( self.piece_bitboards[Piece::Rook]
                                | self.piece_bitboards[Piece::Bishop]);
```

There will be plenty more bitboard magic in the following commits, but this will do for now.

##### Perft tests

To ensure that the chess engine is generating the correct moves, this commit also sets up tests for checking [**perft**](https://www.chessprogramming.org/Perft) (short for **perf**ormance **t**est), which checks how many legal moves there are up until the given depth.
For example

- `perft(1) = 20` -- there are \(8 \* 2\) white pawn moves and \(4\) knight moves
- `perft(2) = 400` -- for each `perft(1)` position, there are `20` moves for black

I've borrowed a **[large perft table](https://github.com/elcabesa/vajolet/blame/master/tests/perft.txt)** from [Valojet](https://github.com/elcabesa/vajolet), a fellow chess engine, because testing perft for only the starting position won't help with debugging most of the trickier chess rules.

{: .commit-header}
#### [`6ddcef9c`](https://github.com/xiaoxiae/Prokopakop/commit/6ddcef9c1acda9e4d229fd95f76782660a307f1d)~[`67d0e64b`](https://github.com/xiaoxiae/Prokopakop/commit/67d0e64b105140242415647314e8c16e078c7e53)
Nothing particularly interesting here.

I've added **pre-computing of the possible moves/attacks** for pieces at compile time, which means that we can easily obtain squares for all pieces by simply accessing a table.
This notably **doesn't work for slider pieces** (rook, bishop, queen), because they can be blocked by other pieces... but that is a problem for a future commit.

I've also added en-passant functionality, for which we'll add 

```rust
pub struct Game {
    // ...

    // if a pawn just moved two squares,
    // 1 will be at the square over which it moved
    en_passant_bitmap: Bitboard,

    // ...
}
```

{: .commit-header}
#### [`178193d3`](https://github.com/xiaoxiae/Prokopakop/commit/178193d3b18c50a8084af5149ca03ca331438f78)

This commit adds [**magic bitboards**](https://www.chessprogramming.org/Magic_Bitboards), which truly hold up to their name, since they're awesome.

##### Magic bitboards

As I've previously mentioned, calculating legal moves for [slider pieces can be tricky, because they can be blocked.
It would be great if we could pre-compute moves for all possible combinations of blockers, since we'd otherwise have to "raycast" from each slider until we hit a piece, which is slow.

As an example, a rook on D5 with the following configuration of blockers should produce the following bitboard of moves + attacks (from now on, I'm leaving out the `0b` and `⏎`, but anything in this shape is still a `u64`):

{% chess %}
8 ...♙....      00000000
7 ........      00000000
6 ...♙....      00010000
5 ♙--♜-♙..      11101100
4 ...|....  →   00010000
3 ...|....      00010000
2 ...♙....      00010000
1 ........      00000000
  abcdefgh
{% endchess %}

The reason for why we can't precompute the moves naively is that we'd either have to use a hashmap of `blocker_state → bitboard`, which will be much slower than the raycasting approach, or create an enormous array of size \(2^{64}\) to use the blocker state as the index, in which case we'd need about 128 exabytes of memory, which I currently do not possess.

Magic bitboards solve this problem in a rather elegant way -- notice that in our example, we actually **only care about a portion of the squares**, since these are the only squares where placing blockers would limit the rook movement.
If we could use only those for indexing, then an array that stores the precomputed bitboards would be significantly smaller... the problem is that the relevant bits are all over the bitboard.

If we could somehow remap them to be in consecutive positions, we could use them for indexing.
To do this, we'll generate a **magic number** that, when multiplying the blocker number, does exactly that -- it **maps the bits we care about** to a combination of **consecutive positions** to be used for indexing, as outlined below:

{% chess %}
bits we       cool         bits
care      *   magic     =  we care
about         number       about,
                           together

........      10001110     17482605
...1....      01011010     39......
...2....      00000110     ........
.34♜567.      01000000     ........
...8....  *   11001101  =  ........
...9....      00000001     ........
...0....      10111111     ........
........      00100111     ........
{% endchess %}

Finally, we shift right to obtain only the bits we care about, obtaining the key we will use to access the precomputed array of rook/bishop moves:

{% chess %}
( bits we       cool   )      (64 - num)     key for
( care      *   magic  )  >>  (of bits )  =  indexing
( about         number )      (together)     the array
                              

(........      10001110)                     ........
(...1....      01011010)                     ........
(...2....      00000110)                     ........
(.34♜567.      01000000)                     ........
(...8....  *   11001101)  >>  (64 - 10)   =  ........
(...9....      00000001)                     ........
(...0....      10111111)                     ......17
(........      00100111)                     48260539
{% endchess %}

Putting this together, we can now retrieve the slider move bitboards by using **two arrays** -- an array to store the **magic numbers** + **number of bits** they map to + **offsets** to the main array where moves for that square start, and the main array storing the actual move bitboards.

In practice, magic numbers can be [generated rather quickly](https://www.chessprogramming.org/Looking_for_Magics) by trying random numbers (those with a low number of non-zero bits work the best), and either loaded from a file, or compiled in.

Pretty cool, isn't it?

{: .commit-header}
#### [`0371037b`](https://github.com/xiaoxiae/Prokopakop/commit/0371037bad4a7aa8449d832520b29e3cf8a65549)~[`33cbd8ec`](https://github.com/xiaoxiae/Prokopakop/commit/33cbd8ec94db534ab6c45c8ad1d41e7a2baafa01)

No particularly interesting things here, here is a short recap:
- added **promotion** (twice; the first implementation let you promote to a king)
- added **history**, so you can undo moves -- a bit tricky, since you need to store both the en-passant bitmap and information about castling
- added **attack bitboards** for both colors, which contained all squares attacked by the opponent -- won't cover these in more detail since they were removed later because they were too slow
- added **castling**, which requires that you keep track of whether you can castle kingside/queenside, and whether the squares over which the king would be moving aren't under attack

{: .commit-header}
#### [`dc9fc039`](https://github.com/xiaoxiae/Prokopakop/commit/dc9fc039d13bee308619bb6befc800f785b10036)

Another absolute banger of a commit, which implements iterative [**Zobrist hashing**](https://en.wikipedia.org/wiki/Zobrist_hashing).

##### Zobrist hashing

When doing search over chess positions, knowing which we've already seen (and can thus skip since we've evaluated it already) is crucial for making a chess engine fast.
We would like to be able to map `board_state → arbitrary_data`, but how do we find a suitable key?

To uniquely identify a chess position, we need
- \(64b\) for piece colors + \({\sim}3b * 64\) for piece types
- \(5b\) for en-passant index
- \(4b\) for castling information
- \(1b\) for whose turn it is

which is not a convenient number of bits to use for table indexing.
Ideally, we'd like to reduce those to 64, which is much nicer to work with and has an extremely low chance of collision over the runtime of a standard chess game.

Zobrist hashing does this in a rather simple way -- we **generate random numbers** for all of the things mentioned above, and **XOR all that apply**[^theplusone] to create the game identifier:

```rust
struct ZobristKeys {
    // every combination of color-piece-square
    pub pieces: [[[u64; 64]; Piece::COUNT]; Color::COUNT],

    // every combination of the 4 castling bits
    pub castling: [u64; 16],

    // every en-passant column; see footnote for explanation of +1
    pub en_passant: [u64; 8 + 1],

    // is it black's turn?
    pub side_to_move: u64,
}
```

It is **iterative**, because since XOR is commutative, we can XOR the current key with values based on what move was made and don't need to calculate it from scratch every time the board changes, adding essentially zero overhead.

I've also added Zobrist hashing to the current [perft implementation](#perft-tests), since that is a great way to test whether it works as it should (spoiler: it initially very much wasn't, but now is).

{: .commit-header}
#### [`a6156eec`](https://github.com/xiaoxiae/Prokopakop/commit/a6156eec2fcbf0b0954e85c608375be4df5cf278)~[`f0253eeb`](https://github.com/xiaoxiae/Prokopakop/commit/f0253eebc1ee2ec9fdd17dde95d1b9b039ae073f)

Removes attack bitboards in favor of simply checking whether any pieces are attacking a particular square, since most code doesn't need them anyway, but they needed to be recalculated after each move.
Also does a bit of refactoring, but nothing too exiting.

{: .commit-header}
#### [`d7c5b4db`](https://github.com/xiaoxiae/Prokopakop/commit/d7c5b4db78803fdc938c46d7f5c5e418d8782038)

This commit compacts a board move to \(16\) bits -- \(5 * 2\) for source + destination square indexes, and \(4\) for identifying a promotion piece (if applicable).
Might not seem like a big change, but board moves are used ubiquitously though the engine, so making them as compact as possible while not sacrificing too much speed is generally a good idea.

{: .commit-header}
#### [`dda91d36`](https://github.com/xiaoxiae/Prokopakop/commit/dda91d360500421c914d4310b4070b2c20898ff5)

##### Pins via Magic Bitboards

When a piece is pinned, we need to limit its movement along the ray of the pin (i.e. between the attacker and the king).
We can obviously do this by "raycasting", but that is boring and slow.
Instead, we can use a trick -- since we've [already implemented magic bitboards](#magic-bitboards), we can use them by pretending that the king is a queen, getting candidate blockers, removing those, and using them again to get the attackers.

{% chess %}
  magic bb                      magic bb
  to get         remove         to get
  blockers                      pinners

8 ........     8 ........     8 ........
7 .....♖..     7 .....♖..     7 .....♖..
6 .♗......     6 .♗......     6 .♗...|..
5 .....♟..     5 .....x..     5 ..\..|..
4 ...♟.|./  →  4 ...x....  →  4 ...\.|./
3 ....\|/.     3 ........     3 ....\|/.
2 -----♚--     2 .....♚..     2 -----♚--
1 ..../|\.     1 ........     1 ..../|\.
  abcdefgh       abcdefgh       abcdefgh
{% endchess %}

There is a slight catch: to obtain the positions of the blockers, you need either a third magic bitboard access from the position of the blocker, or precompute possible rays between points; I haven't been able to find a smarter way to do this, please let me know if there is one.

{: .commit-header}
#### [`896a48ce`](https://github.com/xiaoxiae/Prokopakop/commit/896a48ce3f51e5ee0c011add681f7180565c92d5)~[`5bc16a6b`](https://github.com/xiaoxiae/Prokopakop/commit/5bc16a6b05098bd50338504ebf85b356ec409e0d)

Currently, we are generating moves by generating all [_pseudo-legal moves_](https://www.chessprogramming.org/Pseudo-Legal_Move) (those where king can be under attack afterwards), making them, checking whether the king is under attack afterwards, and unmaking them.
This is as simple as it is slow, as we have to repeatedly modify the board state in order to check whether the move is legal or not, causing a lot of overhead.

##### Legal Move Generation

A faster approach is to generate [_legal moves_](https://www.chessprogramming.org/Legal_Move) directly, without having modify the board state.
This, however, requires significantly more care, as the king can come under attack in a number of tricky ways.
In prokopakop, I distinguish between three cases, depending on the **number of attacks** the king is under:
- **0**: normal generation
- **1**: king has to either **move,** or the attacker must be **captured**
- **2+**: king can **only move**

Separating the cases makes legal move generation more managable, and makes it much faster than make/unmake-based move generation.
Instead of going through the code (which, if you're interested, [can be found here](https://github.com/xiaoxiae/Prokopakop/blob/master/src/game/board.rs)), I'll point you towards [Peter Ellis Jones' blog post](https://peterellisjones.com/posts/generating-legal-chess-moves-efficiently/) on legal move generation, as it was a great resource when implementing it myself.

{: .commit-header}
#### [`99020474`](https://github.com/xiaoxiae/Prokopakop/commit/99020474e514d47bc72b25f46bc77fbd804b5dd7)~[`3ff11a44`](https://github.com/xiaoxiae/Prokopakop/commit/3ff11a44e6945f5de5cdded988b73f611b9e5f62)

Final commits in the move generation saga.

Besides small improvements/optimizations, the main change that I made was to repleace most of the move generation code by [**const generic**](https://www.chessprogramming.org/Generic_Programming) variants, i.e. changing from this
```rust
fn make_move(&mut self, board_move: BoardMove) { ... }
```

to this

```rust
fn make_move_const<P: ConstPiece, C: ConstColor>(&mut self, board_move: BoardMove) { ... }
```

which allows us to do compile-time optimizations like this:

```rust
// this will be evaluated compile-time!
if P::PIECE == Piece::Pawn {
    // ... will only run if the piece is a pawn ...
}
```




### Search & Evaluation



[^allyouneed]: Okay, not quite; you also need to cast `Color::White as usize`, but that's ugly and an implementation detail, so I skipped it for the sake of clarity. You can get rid of it by implementing indexing for the array type, but I haven't done that because I'm lazy.

[^theplusone]: This is done so that we don't need to check whether en-passant bit changed during the move (since that adds branching, which is slow) -- we therefore add an additional "no-op value", which will be used when en-passant didn't happen; since we're XORing twice, these cancel out and we don't need to branch!
