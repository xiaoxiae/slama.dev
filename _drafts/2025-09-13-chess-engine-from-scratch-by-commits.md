---
title: A Chess Engine, Commit by Commit
excerpt: "Writing a chess engine from scratch, commit by commit."
css: chess
---

- .
{:toc}

[Prokop, a ginger and a friend of mine](https://rdck.dev/) (these are the same person, which is surprising) recently challenged me to a chess engine duel, which consisted of making a chess bot from scratch and then dueling to see whose is better.
Naturally, I agreed.
And thus **[Prokopakop](https://github.com/xiaoxiae/prokopakop)** (literally translates to _the one that kicked Prokop_) was born.

It (unsurprisingly) turns out that there is a lot of things that go into making a chess bot, and I thought it would be interesting to cover my journey of writing the bot in the commits that I made, since they more-or-less correspond to the concepts that I learned along the way.

So, without further ado, let's write a chess bot!

_I assume that you know chess, because you managed to stumble upon this exceedingly nerdy post about a chess engine.
If not, this will be a wild ride. 🕊_

### Move Generation

Before beginning to write a chess bot that searches/evaluates positions, we need to make sure that we can generate them quickly, since we'll need those to search/evaluate over.
If you're not too interested in how the moves are generated (which is a shame, since I'd say that this is the more interesting part), you can skip to **[search & evaluation](#search--evaluation)**.

{: .commit-header}
[`a1f8b8`](https://github.com/xiaoxiae/Prokopakop/commit/a1f8b867c9818e411a491e8cfdbd115411f1beb1)

The first commit actually contains quite a bit of code, and should have likely been split into separate ones.
However, I wanted the first commit to actually contain something that remotely resembles a chess engine, so here we are.

#### Bitboards

The most important part of this commit is that it stored the board state position via [**bitboards**](https://www.chessprogramming.org/Bitboards), which are necessary for making the engine fast.
The concept is very simple -- since CPUs are heavily optimized for working with 64-bit numbers, and 64 turns out to be the exact number of squares on the board, we can use them to store (among other things) locations of pieces.

As an example, here is a bitboard (=64-bit unsigned integer) that stores pawn positions.

{% chess %}0b00000000⏎     8 ........
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

#### Perft tests

To ensure that the chess engine is generating the correct moves, this commit also sets up tests for checking [**perft**](https://www.chessprogramming.org/Perft) (short for **perf**ormance **t**est), which checks how many legal moves there are up until the given depth.
For example

- `perft(1) = 20` -- there are \(8 \cdot 2\) white pawn moves and \(4\) knight moves
- `perft(2) = 400` -- for each `perft(1)` position, there are `20` moves for black

I've borrowed a **[large perft table](https://github.com/elcabesa/vajolet/blame/master/tests/perft.txt)** from [Vajolet](https://github.com/elcabesa/vajolet), a fellow chess engine, because testing perft for only the starting position won't help with debugging most of the trickier chess rules.

{: .commit-header}
[`6ddcef`](https://github.com/xiaoxiae/Prokopakop/commit/6ddcef9c1acda9e4d229fd95f76782660a307f1d)~[`67d0e6`](https://github.com/xiaoxiae/Prokopakop/commit/67d0e64b105140242415647314e8c16e078c7e53)

Nothing particularly interesting here.

I've added **pre-computing of the possible moves/attacks** for pieces at compile time, which means that we can easily obtain squares for all pieces by simply accessing a table.
This notably **doesn't work for [sliding pieces](https://www.chessprogramming.org/Sliding_Pieces)** (rook, bishop, queen), because they can be blocked by other pieces... but that is a problem for a future commit.

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
[`178193`](https://github.com/xiaoxiae/Prokopakop/commit/178193d3b18c50a8084af5149ca03ca331438f78)

This commit adds [**magic bitboards**](https://www.chessprogramming.org/Magic_Bitboards), which truly hold up to their name, since they're awesome.

#### Magic bitboards

As I've previously mentioned, calculating legal moves for slider pieces can be tricky, because they can be blocked.
It would be great if we could pre-compute moves for all possible combinations of blockers, since we'd otherwise have to "raycast" from each slider until we hit a piece, which is slow.

As an example, a rook on D5 with the following configuration of blockers should produce the following bitboard of moves + attacks (from now on, I'm leaving out the `0b` and `⏎`, but any zeros/ones in an 8x8 shape are still `u64`):

{% chess %}8 ...♙....      00000000
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
If we could use only the relevant squares for indexing, then an array that stores the precomputed bitboards would be significantly smaller.
The problem with is that the relevant bits are all over the bitboard.

If we could somehow **remap them to be in consecutive positions,** we could use them for indexing.
To do this, we'll generate a **magic number** that, when **multiplying** the blocker number, does exactly that -- it **maps the bits we care about** to a combination of **consecutive positions** to be used for indexing, as outlined below:

{% chess %}bits we       cool         bits
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

{% chess %}( bits we       cool   )      (64 - num)     key for
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
[`037103`](https://github.com/xiaoxiae/Prokopakop/commit/0371037bad4a7aa8449d832520b29e3cf8a65549)~[`33cbd8`](https://github.com/xiaoxiae/Prokopakop/commit/33cbd8ec94db534ab6c45c8ad1d41e7a2baafa01)

No particularly interesting things here, here is a short recap:
- added **promotion** (twice; the first implementation let you promote to a king)
- added **history**, so you can undo moves -- a bit tricky, since you need to store both the en-passant bitmap and information about castling
- added **attack bitboards** for both colors, which contained all squares attacked by the opponent -- won't cover these in more detail since they were removed later because they were too slow
- added **castling**, which requires that you keep track of whether you can castle kingside/queenside, and whether the squares over which the king would be moving aren't under attack

{: .commit-header}
[`dc9fc0`](https://github.com/xiaoxiae/Prokopakop/commit/dc9fc039d13bee308619bb6befc800f785b10036)

Another absolute banger of a commit, which implements iterative [**Zobrist hashing**](https://en.wikipedia.org/wiki/Zobrist_hashing).

#### Zobrist hashing

When doing search over chess positions, knowing which we've already seen (and can thus skip since we've evaluated it already) is crucial for making a chess engine fast.
We would like to be able to map `board_state → arbitrary_data`, but how do we find a suitable key?

To uniquely identify a chess position, we need
- \(64b\) for piece colors + \({\sim}3b * 64\) for piece types
- \(5b\) for en-passant index
- \(4b\) for castling information
- \(1b\) for whose turn it is

which is not a convenient number of bits to use for table indexing.
Ideally, we'd like to reduce those to 64, which is much nicer to work with and has an extremely low chance of collision over the runtime of a standard chess game.

Zobrist hashing does this in a rather simple way -- we **generate random numbers** for all of the things mentioned above, and **XOR all that apply** (with an aditional extra one for en-passant[^theplusone]) to create the game identifier:

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

It is **iterative**, because since XOR is commutative, we can XOR the current key with values based on what move was made and don't need to calculate it from scratch every time the board changes, adding virtually zero overhead.

I've also added Zobrist hashing to the current [perft implementation](#perft-tests), since that is a great way to test whether it works as it should.
Generally, you should only do this once the tests are passing for an implementation without, otherwise the debugging will be miserable.

{: .commit-header}
[`a6156e`](https://github.com/xiaoxiae/Prokopakop/commit/a6156eec2fcbf0b0954e85c608375be4df5cf278)~[`f0253e`](https://github.com/xiaoxiae/Prokopakop/commit/f0253eebc1ee2ec9fdd17dde95d1b9b039ae073f)

Removes attack bitboards in favor of simply checking whether any pieces are attacking a particular square, since most code doesn't need them anyway, but they needed to be recalculated after each move.
Also does a bit of refactoring, but nothing too exciting.

{: .commit-header}
[`d7c5b4`](https://github.com/xiaoxiae/Prokopakop/commit/d7c5b4db78803fdc938c46d7f5c5e418d8782038)

This commit compacts a board move to \(16\) bits -- \(5 * 2\) for source + destination square indexes, and \(4\) for identifying a promotion piece (if applicable).
Might not seem like a big change, but board moves are used ubiquitously though the engine, so making them as compact as possible while not sacrificing too much speed is generally a good idea.

{: .commit-header}
[`dda91d`](https://github.com/xiaoxiae/Prokopakop/commit/dda91d360500421c914d4310b4070b2c20898ff5)

#### Pins via Magic Bitboards

When a piece is pinned, we need to limit its movement along the ray of the pin (i.e. between the attacker and the king).
We can obviously do this by "raycasting" (i.e. iterating from the king square), but that is boring and slow.
Instead, we can use a trick -- since we've [already implemented magic bitboards](#magic-bitboards), we can use them by pretending that the king is a queen, getting candidate blockers, removing those, and using them again to get the attackers.

{% chess %}  magic bb                      magic bb
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
[`896a48`](https://github.com/xiaoxiae/Prokopakop/commit/896a48ce3f51e5ee0c011add681f7180565c92d5)~[`5bc16a`](https://github.com/xiaoxiae/Prokopakop/commit/5bc16a6b05098bd50338504ebf85b356ec409e0d)

Currently, we are generating moves by generating all [pseudo-legal moves](https://www.chessprogramming.org/Pseudo-Legal_Move) (those where king can be under attack afterwards), making them, checking whether the king is under attack afterwards, and unmaking them.
This is as simple as it is slow, as we have to repeatedly modify the board state in order to check whether the move is legal or not, causing a lot of overhead.

#### Legal Move Generation

A faster approach is to generate [legal moves](https://www.chessprogramming.org/Legal_Move) directly, without having modify the board state.
This, however, requires significantly more care, as the king can come under attack in a number of tricky ways.
In prokopakop, I distinguish between three cases, depending on the **number of attacks** the king is under:
- **0**: normal generation
- **1**: king has to either **move,** or the attacker must be **captured**
- **2+**: king can **only move**

Separating the cases makes legal move generation more managable, and makes it much faster than make/unmake-based move generation.
Instead of going through the code (which, if you're interested, [can be found here](https://github.com/xiaoxiae/Prokopakop/blob/master/src/game/board.rs)), I'll point you towards [Peter Ellis Jones' blog post](https://peterellisjones.com/posts/generating-legal-chess-moves-efficiently/) on legal move generation, as it was a great resource when implementing it myself.

{: .commit-header}
[`990204`](https://github.com/xiaoxiae/Prokopakop/commit/99020474e514d47bc72b25f46bc77fbd804b5dd7)~[`3ff11a`](https://github.com/xiaoxiae/Prokopakop/commit/3ff11a44e6945f5de5cdded988b73f611b9e5f62)

Final commits in the move generation saga.

Besides small improvements/optimizations, the main change that I made was to replace most of the move generation code by [**const generic**](https://www.chessprogramming.org/Generic_Programming) variants.
This is just a fancy way of saying that most functions in my code have multiple variants for pieces/colors, which reduces the number of branches in the code and thus speeds it up.

As an example, the outer `if` in this code:
```rust
// update castling rights when rook moves
if P::PIECE == Piece::Rook {
    let castling_flags = self.castling_flags
        & !match (C::COLOR, board_move.get_from()) {
            (Color::Black, BoardSquare::H8) => 0b00000001,
            (Color::Black, BoardSquare::A8) => 0b00000010,
            (Color::White, BoardSquare::H1) => 0b00000100,
            (Color::White, BoardSquare::A1) => 0b00001000,
            _ => 0,
        };

    self.update_castling_flags(castling_flags);
}
```

gets evaluated at **compile time** and thus all of this code will **only be present** when calling the function on a rook.
No branching, no problem!

#### Summary

As we have reached the end of the move generation portion of this article, here is the speed of move generation across the commits that we've discussed.


![](/assets/chess-engine-from-scratch-by-commits/benchmark.webp)

As you can see, two three places stand out in this graph:
- the **first major spike in speed** (commit [`f0253e`](https://github.com/xiaoxiae/Prokopakop/commit/f0253eebc1ee2ec9fdd17dde95d1b9b039ae073f)) was caused by **removing the attack bitboards;** since these were previously calculated every move and consisted of evaluating all attacks of all pieces on the board, this is not surprising
- the **first major crash** (commit [`1d8e55`](https://github.com/xiaoxiae/Prokopakop/commit/1d8e55)) was caused by **starting to move away from the make/unmake-based move generation** by splitting each move generation into different functions based on the number of attacks; as this only included the spitting, but no optimized code, this introduced a large amount of branching that killed the speed
- the **second major spike** (commits [`a67205`](https://github.com/xiaoxiae/Prokopakop/commit/a67205) and [`5bc16a`](https://github.com/xiaoxiae/Prokopakop/commit/5bc16a)) were caused by **finishing moving away from the make/unmake-free move generation** by introducing functions optimized for zero/one/two+ king attacks

The engine is slower than Stockfish (\(9.74\text{s}\) vs. \(8.71\text{s}\) for `perft(7)`), but this is simply too bad because I'm not spending more time on this when I haven't written any search & evaluation functionality yet.
Maybe I'll revisit to beat Stockfish at some point in the future, but we'll have to do with this.

### Search & Evaluation

Now that we can generate moves quickly (for some definition of quickly), we need to **search** through them to find the best one and **evaluate** the resulting positions.
Since chess is a zero-sum two-player game, we can simply assign each position a positive/negative score (white is positive, black is negative) based on piece positions/counts, and always pick the move that leads to the best score for the given player.

{% chess %}                     Current
                   (Max: +0.8)
                        │
       ┌────────────────┼────────────────┐   maximizing
       ↓                │                │
    Move A           Move B           Move C
   (Normal)        (Queen Sac)      (Pawn Sack)
  (Min: +0.8)      (Min: -6.1)      (Min: -0.7)
       │                │                │
       │                │                │
  ┌────┼────┐      ┌────┼────┐      ┌────┼────┐   minimizing
  ↓    │    │      ↓    │    │      │    │    ↓
+0.8 +1.2 +0.9   -6.1 -5.8 -7.2   -0.3 +0.1 -0.7
{% endchess %}

This is called the [minimax algorithm](https://www.chessprogramming.org/Minimax), and is at the heart of most[^lc0] strong chess engines (prokopakop included).
The algorithm works by recursively exploring all possible moves to a certain depth. When it's our turn (**max**imizing player), we want to pick the move that leads to the **highest** score. When it's the opponent's turn (**min**imizing player), they will pick the move that leads to the **lowest** score (best for them, worst for us).

At each **leaf node** (when we've reached our search depth), we evaluate the position, i.e. how good it is for the player whose turn it is.
Then we propagate these scores back up the tree: maximizing nodes take the maximum of their children's scores, minimizing nodes take the minimum.


{: .commit-header}
[`9fec3a0`](https://github.com/xiaoxiae/Prokopakop/commit/9fec3a0)

#### Alpha-Beta Search

While minimax is an important foundation to our search functionality, we can greatly improve it by using **[alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta)**, which I implemented in the first search & eval commit.

Let's say that we we have just fully explored the move `A`, which was a regular move that gave us a slight advantage.
We then proceed to `B`, which is actually a blunder, and we find this out quickly after exploring the first opponent response.
Since the opponent has a **strong response** that will already be **worse for us than the output of `A`**, we can **prune** the rest of `B` -- no matter what the other moves are, if the opponent picks this response, it will be worse for us than the output of `A`.

{% chess %}                     Current
                        │
       ┌────────────────┼────────────────┐
       │                │                │
    Move A           Move B           Move C
   (Normal)        (Queen Sac)      (Pawn Sack)
  (Min: +0.8)     (Min:<= -6.1)
       │                │
       │                │
  ┌────┼────┐      ┌────┼────┐
  ↓    │    │      ↓    │    │
+0.8 +1.2 +0.9   -6.1   ?    ?   pruned
{% endchess %}

Formally, we track the **best values the players can achieve** in the particular position as \(\alpha\) (white) and \(\beta\) (black), and induce a cutoff if \(\beta \le \alpha\) -- this is something that can only happen if, at some earlier point of the search tree, we had a better option to pick.


{% chess %}                     Current
                        │
       ┌────────────────┼────────────────┐
       │                │                │
    Move A           Move B           Move C
   (Normal)        (Queen Sac)      (Pawn Sack)
  α=-∞, β=+∞      α=+0.8, β=+∞
       │                │
       │                │
  ┌────┼────┐      ┌────┼────┐
  ↓    │    │      ↓    │    │
+0.8 +1.2 +0.9   -6.1   ?    ?

                     β <= α
                  -6.1 <= +0.8
                 CUTOFF INDUCED
{% endchess %}

In prokopakop (and essentially all other engines), I have implemented this via **[negamax](https://www.chessprogramming.org/Alpha-Beta#Negamax_Framework)**, which simplifies the implementation by **always maximizing** and **flipping + negating** the alpha/beta values and evaluation when doing the recursive call, as we're changing perspectives.
This is very convenient, because it simplifies both the implementation and the conceptual meaning of alpha and beta -- we can now always think of **alpha** as the **lower bound** (what we are _guaranteed_ somewhere in the search tree), and **beta** as the **upper bound** (what the _opponent won't allow us to exceed_ because of what he has guaranteed somewhere in the search tree).

I have also implemented **[iterative deepening](https://www.chessprogramming.org/Iterative_Deepening)** for time management, which runs alpha-beta search with depths \(1, 2, \ldots\) until time runs out and returns the best result found, so we can limit time spent on searching based on the current time control.

Note that for alpha-beta search to work well, we need to ensure that the moves are **sorted**, as exploring more interesting lines first will induce more cutoffs, as compared to when the moves are unordered -- we'll [implement this later](#mmv-lva).

#### Material Evaluation

As a final step in this initial seach/eval commit, I implemented a basic evaluation function, which simply counts material.
While this might seem like all you need, this is generally not sufficient as it doesn't take into account many nuances of the position, such as pawn structure, piece mobility, etc...

{: .commit-header}
[`8eeb84e`](https://github.com/xiaoxiae/Prokopakop/commit/8eeb84e)~[`6aec863`](https://github.com/xiaoxiae/Prokopakop/commit/6aec863)

#### Piece-Square Tables

This commit adds [**piece-square tables**](https://www.chessprogramming.org/Piece-Square_Tables) for positional evaluation.
These are a set of tables that, for each piece, provide information about how much it is worth when being on a particular square.
As an example, here is what a pawn table could look like:

{% chess %}const PAWN_TABLE: [f32; 64] = [
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   +1.0, +1.0, +1.0, +1.0, +1.0, +1.0, +1.0, +1.0,
   +0.2, +0.2, +0.4, +0.6, +0.6, +0.4, +0.2, +0.2,
   +0.1, +0.1, +0.2, +0.5, +0.5, +0.2, +0.1, +0.1,
    0.0,  0.0,  0.0, +0.4, +0.4,  0.0,  0.0,  0.0,
   +0.1, -0.1, -0.2,  0.0,  0.0, -0.2, -0.1, +0.1,
   +0.1, +0.2, +0.2, -0.4, -0.4, +0.2, +0.2, +0.1,
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
];
{% endchess %}

Positive values correspond to places where pawns are more valuable (closer to the opponent's back rank, in the center, etc...), while negative values correspond to those where they are less valuable.

We can also take this one step further, and have two tables -- one for "early" game, one for "late" game (for some suitable definitions of early and late, such as total remaining material), and interpolate between them during the game.
This is typically done for the king, as we want him to be more protected in the early game, and more aggressive in the late game.

{% chess %}const KING_EARLY_TABLE: [f32; 64] = [
   +0.2, +0.1, +0.1,  0.0,  0.0, +0.1, +0.1, +0.2,
   +0.2, +0.1, +0.1,  0.0,  0.0, +0.1, +0.1, +0.2,
   +0.2, +0.1, +0.1,  0.0,  0.0, +0.1, +0.1, +0.2,
   +0.2, +0.1, +0.1,  0.0,  0.0, +0.1, +0.1, +0.2,
   +0.3, +0.2, +0.2, +0.1, +0.1, +0.2, +0.2, +0.3,
   +0.4, +0.3, +0.3, +0.3, +0.3, +0.3, +0.3, +0.4,
   +0.7, +0.7, +0.5, +0.5, +0.5, +0.5, +0.7, +0.7,
   +0.7, +0.7, +1.0, +0.5, +0.5, +0.6, +1.0, +0.7,
];

const KING_LATE_TABLE: [f32; 64] = [
    0.0, +0.1, +0.2, +0.3, +0.3, +0.2, +0.1,  0.0,
   +0.2, +0.3, +0.4, +0.5, +0.5, +0.4, +0.3, +0.2,
   +0.2, +0.4, +0.7, +0.8, +0.8, +0.7, +0.4, +0.2,
   +0.2, +0.4, +0.8, +0.9, +0.9, +0.8, +0.4, +0.2,
   +0.2, +0.4, +0.8, +0.9, +0.9, +0.8, +0.4, +0.2,
   +0.2, +0.4, +0.7, +0.8, +0.8, +0.7, +0.4, +0.2,
   +0.2, +0.2, +0.5, +0.5, +0.5, +0.5, +0.2, +0.2,
    0.0, +0.2, +0.2, +0.2, +0.2, +0.2, +0.2,  0.0,
];
{% endchess %}

{: .commit-header}
[`53a09e5`](https://github.com/xiaoxiae/Prokopakop/commit/53a09e5)

#### Move Ordering

As mentioned in the [alpha-beta section](#alpha-beta-search), for the moves to be pruned efficiently, we need to pick the strongest lines early so that they can be searched first and used for pruning the later branches.
While general moves are difficult to order without branching on them first, we can use a simple heuristic to order **capturing moves**, and it is exactly what you're thinking of -- capture the **m**ost **v**aluable **v**ictim with the **l**east **v**aluable **a**ttacker ([MVV-LVA](https://www.chessprogramming.org/MVV-LVA)).

This, combined with always searching the moves from the **p**rincipal **v**ariation first (best line found in the previous iteration of iterative deepening), gives a decent ordering and provides a good speed-up to the alpha-beta search.

{: .commit-header}
[`bbef3be`](https://github.com/xiaoxiae/Prokopakop/commit/bbef3be)

#### Quiescence Search

Using alpha-beta search with iterative deepening means that we always, for depths \(1, \ldots, n\), explore until a certain depth and then evaluate the position.
This has an obvious flaw: what if we make blunder, like taking a queen for a pawn, in the final depth?
Since this was the last depth that we were searching, this wouldn't get caught, and we'd happily return positive evaluation, since we're up a pawn!

This is where [quiescence search](https://www.chessprogramming.org/Quiescence_Search)[^quiescence] comes in -- when reaching the final depth of the iteration, it **extends the search** to **all remaining captures** (and possibly checks), so that we are **only evaluating quiet positions** (i.e. those where there are no tactical sequences that can severely impact the score).
That way, we don't have crazy spikes in evaluation and avoid blunders.

{: .commit-header}
[`35f6fb6`](https://github.com/xiaoxiae/Prokopakop/commit/35f6fb6)

#### Transposition Table

Re-evaluating a position we have already reached and evaluated would be a waste, so let's not do that and implement [**transposition table**](https://www.chessprogramming.org/Transposition_Table) (TT for the rest of the article because I'm too lazy to type).
Since we've already implemented [zobrist hashing](#zobrist-hashing), we can quickly identify these positions and avoid needless computation... but what do we actually store?

Let's look at a minimax search first -- when evaluating a position, we examine **all moves** until a certain **depth**, so the calculated evaluation is **exact** up until the given depth.
When reaching this position again, we can use this already calculated value **if the depth we're searching to** is **less than or equal to the one we already did**.
In other words, if the depth we're searching to exceeds the one we already did, we need to actually do the computation, otherwise we return the stored result.

Alpha-beta makes this slightly more difficult, because alpha-beta means that certain calculations will no longer be exact.
They still, however, tell us important information about whether we have calculated an **upper bound** on the score, or a **lower bound** -- there are two additional things (besides the exact case) that can happen:

1. If we **prune** a branch (i.e. cause a **cut-off**), it is because we found a move that is **too good**, because the **other player** will play something that's better for him elsewhere in the tree.
   This means that the evaluation of this branch can **only get better** as we go through the moves, so we get a **lower bound**.
2. If we, on the other hand, go through **all moves** and **none of them improve alpha**, it means that the position can't score better than what we have found, and we have thus found an **upper bound**.

Adding these two cases, we store **three types** of nodes -- **exact**, **upper bound**, and **lower bound**.
Implementation-wise, we'd store something like this:

```rust
pub enum NodeType {
    Exact,       // no pruning happened
    LowerBound,  // beta cutoff at maximizing node
    UpperBound,  // alpha cutoff at minimizing node
}

pub struct TTEntry {
    pub key: u64,             // zobrist hash
    pub depth: u8,            // how far we searched
    pub evaluation: f32,      // evaluation of this branch
    pub node_type: NodeType,  // what type of information we obtained
}
```

For implementing the TT itself, we can use a nice trick: instead of using a hashmap, use a **fixed array** of size \(2^n\) and the **first \(\mathbf{n}\) bits** of the zobrist hash as an index... because why would we hash twice?

There are many other things to consider like [replacement strategies](https://www.chessprogramming.org/Transposition_Table#Replacement_Strategies) and more advanced TT implementations, such as using  [buckets](https://www.chessprogramming.org/Transposition_Table#Bucket_Systems), but I won't go into detail on those as we've covered the core idea behind TT and this article is already long enough.

As a final note: when doing research for this article, I found that the three [node categories](https://www.chessprogramming.org/Node_Types) described above are sometimes called **PV** (exact), **Cut** (lower bound) and **All** (upper bound) nodes, so don't be surprised when you see these terms used; they refer to the node types.
This mainly originates from a [2003 paper](https://dke.maastrichtuniversity.nl/m.winands/documents/Enhanced%20forward%20pruning.pdf) about pruning methods[^alphabeta].


[^allyouneed]: Okay, not quite; you also need to cast `Color::White as usize`, but that's ugly and an implementation detail, so I skipped it for the sake of clarity. You can get rid of it by implementing indexing for the array type, but I haven't done that because I'm lazy.

[^theplusone]: This is done so that we don't need to check whether en-passant bit changed during the move (since that adds branching, which is slow) -- we therefore add an additional "no-op value", which will be used when en-passant didn't happen; since we're XORing twice, these cancel out and we don't need to branch!

[^lc0]: Some chess engines, like [Leela Chess Zero](https://lczero.org/), use [Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) instead. This is because their position evaluation is orders of magnitude slower but much more advanced, so they do a deeper search on promising lines instead of a wide one on all of them.

[^quiescence]: I'm not a native speaker, so this seemed like a strange usage of this word. The definition of "quiescence" is, according to the Cambridge English Dictionary, _the state of being temporarily quiet and not active_, so this makes sense -- we want to **search for quiet positions** and only evaluate those.
