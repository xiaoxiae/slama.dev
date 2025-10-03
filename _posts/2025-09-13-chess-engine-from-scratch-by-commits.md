---
title: A Chess Engine, Commit by Commit
excerpt: "Writing a chess engine from scratch, commit by commit."
css: chess
category_icon: /assets/category-icons/prokopakop.svg
hidden: true
---

- .
{:toc}

[Prokop, a ginger and a friend of mine](https://rdck.dev/) (these are the same person, which is surprising) recently challenged me to a chess engine duel, which consisted of making a chess bot from scratch and then dueling to see whose is better.
Naturally, I agreed.
And thus **[Prokopakop](https://github.com/xiaoxiae/prokopakop)** (literally translates to _the one that kicked Prokop_) was born.

It (unsurprisingly) turns out that there is a lot of things that go into making a chess bot, and I thought it would be interesting to cover my journey of writing the bot in the commits that I made, since they correspond to the order in which I learned the various techniques and algorithms that a chess engine uses.

While this article is intended to be read top-to-bottom for beginners to chess-bot-related things, I've also added headings for specific topics so that people who are only interested in those can skip around -- **all sections are self-sustained** (as much as they can be), so skipping around is very much encouraged.

So, without further ado, let's write a chess bot!

Also, [**go play it on Lichess**](https://lichess.org/@/prokopakop); just keep in mind that it **won't play more than one game at a time,** because the server it's running on only has two cores, and using both would take this website down.

---

_I assume that you know chess rules, because you managed to stumble upon this exceedingly nerdy post about a chess engine.
If not, this will be a wild ride. 🕊_

### Move Generation

Before beginning to write a chess bot that searches/evaluates positions, we need to make sure that we can generate them quickly.
If you're not too interested in how the positions are generated (which is a red flag, since I'd say that this is the more interesting part), you can skip to the **[search & evaluation](#search--evaluation)** portion of the article.

{: .commit-header}
[`a1f8b8`](https://github.com/xiaoxiae/Prokopakop/commit/a1f8b867c9818e411a491e8cfdbd115411f1beb1)

The first commit actually contains quite a bit of code, and should have likely been split into separate ones.
However, I wanted the first commit to actually contain something that remotely resembles a chess engine, so here we are.

#### Bitboards

The most important part of this commit is that it stored the board state position via [**bitboards**](https://www.chessprogramming.org/Bitboards), which are necessary for making the engine fast.
The concept is very simple -- since CPUs are heavily optimized for working with 64-bit numbers, and 64 turns out to be the exact number of squares on the board, we can use them to store (among other things) locations of pieces!

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
    pub color_bb: [Bitboard; Color::COUNT],

    // six bitboards for piece types
    pub piece_bb: [Bitboard; Piece::COUNT],

    // ...
}
```

As an example, to obtain all positions of _white rooks and bishops_, all you need to[^all-you-need] do is

```rust
self.color_bb[Color::White] & ( self.piece_bb[Piece::Rook]
                              | self.piece_bb[Piece::Bishop]);
```

There will be plenty more bitboard magic in the following commits, but this will do for now.

#### Perft tests

To ensure that the chess engine is generating the correct moves, this commit also sets up tests for checking [**perft**](https://www.chessprogramming.org/Perft) (short for **perf**ormance **t**est), which checks how many legal moves there are up until the given depth.
For example

- `perft(1) = 20` -- there are \(8 \cdot 2\) white pawn moves and \(4\) knight moves
- `perft(2) = 400` -- for each `perft(1)` position, there are `20` moves for black

I've borrowed a **[large perft table](https://github.com/elcabesa/vajolet/blame/master/tests/perft.txt)** from [Vajolet](https://github.com/elcabesa/vajolet), a fellow chess engine, because testing perft for only the starting position won't help with debugging most of the trickier chess rules.
This is especially true in the beginning, when the engine is also very slow and can't get to the tricky positions too quickly.

{: .commit-header}
[`6ddcef`](https://github.com/xiaoxiae/Prokopakop/commit/6ddcef9c1acda9e4d229fd95f76782660a307f1d)~[`67d0e6`](https://github.com/xiaoxiae/Prokopakop/commit/67d0e64b105140242415647314e8c16e078c7e53)

I've added **pre-computing of the possible moves/attacks** for pieces at compile time, which means that we can easily obtain squares for all pieces by simply accessing a table.
This notably **doesn't work for [sliding pieces](https://www.chessprogramming.org/Sliding_Pieces)** (rook, bishop, queen), because they can be blocked by other pieces... but that is a problem [for a future commit](#magic-bitboards).

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

Although this is a bit wasteful since we could just store the column (chess people call them files, but I'm not falling for the propaganda), but having a bitmap is nice since we can more easily check if a pawn can "capture" that square.

{: .commit-header}
[`178193`](https://github.com/xiaoxiae/Prokopakop/commit/178193d3b18c50a8084af5149ca03ca331438f78)

#### Magic bitboards

As I've previously mentioned, calculating legal moves for slider pieces can be tricky, because they can be blocked.
It would be great if we could pre-compute moves for all possible combinations of blockers, since we'd otherwise have to "raycast" from each slider until we hit a piece, which is slow.

As an example, a rook on d5 with the following configuration of blockers should produce the following bitboard of moves + attacks (from now on, I'm leaving out the `0b` and `⏎`, but any zeros/ones in an 8x8 shape are still `u64`):

{% chess %}8 ...♙....     00000000
7 ........     00000000
6 ...♙....     00010000
5 ♙--♜-♙..     11101100
4 ...|....  →  00010000
3 ...|....     00010000
2 ...♙....     00010000
1 ........     00000000
  abcdefgh
{% endchess %}

The reason for why we can't precompute the moves naively is that we'd either have to use a hashmap of `blocker_state → bitboard`, which will be much slower than the raycasting approach, or create an enormous array of size \(2^{64}\) to use the blocker state as the index, in which case we'd need about 128 exabytes of memory, which I currently do not possess.

[**Magic bitboards**](https://www.chessprogramming.org/Magic_Bitboards) solve this problem in a rather elegant way -- notice that in our example, we actually **only care about a portion of the squares** (in this case the row + column the rook is in), since these are the **only squares where placing blockers would limit the rook movement**.
If we could use only the relevant squares for indexing, then an array that stores the precomputed bitboards would be significantly smaller.

If we could somehow **remap them to be in consecutive positions,** we could use them for indexing.
To do this, we will, for each square, generate a **magic number** that, when **multiplying** the blocker bitmap, does exactly that -- it **maps the bits we care about** to a combination of **consecutive positions** to be used for indexing, as seen in the following diagram:

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

Finally, we **shift right** to obtain only the bits we care about, obtaining the key we will use to access the precomputed array of rook/bishop moves.
This is the reason for why we'd like the consecutive positions to start from the **most significant bits** -- that way a single `shr` operation is enough to obtain the index (otherwise we'd need two shifts, or some masking).

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

{: .commit-header}
[`037103`](https://github.com/xiaoxiae/Prokopakop/commit/0371037bad4a7aa8449d832520b29e3cf8a65549)~[`33cbd8`](https://github.com/xiaoxiae/Prokopakop/commit/33cbd8ec94db534ab6c45c8ad1d41e7a2baafa01)

No particularly interesting things here, here is a short recap:
- added **promotion** (twice; the first implementation let you promote to a king)
- added **history**, so you can undo moves -- a bit tricky, since you need to store both the en-passant bitmap and information about castling
- added **attack bitboards** for both colors, which contained all squares attacked by the opponent -- won't cover these in more detail since they were removed later due to being too slow
- added **castling**, which requires that you keep track of whether you can castle kingside/queenside, and whether the squares over which the king would be moving aren't under attack

These changes expand our `Game` struct:

```rust
pub struct Game {
    // ...

    // 0x0000KQkq, where kq/KQ is one if black/white king and queen
    castling_flags: u8,

    // store the move, which piece was there, and en-passant + castling flags
    // the flags can NOT be calculated as an arbitrary position can have those
    // (move, captured_piece, castling_flags, en_passant_bitmap)
    pub history: Vec<(BoardMove, Option<ColoredPiece>, u8, Bitboard)>,
}
```

{: .commit-header}
[`dc9fc0`](https://github.com/xiaoxiae/Prokopakop/commit/dc9fc039d13bee308619bb6befc800f785b10036)

#### Zobrist hashing

When doing search over chess positions, knowing which we've already seen (and can thus skip since we've evaluated it already) is crucial for making a chess engine fast.
We would like to be able to map `board_state → arbitrary_data`, but how do we find a suitable key?

To uniquely[^unique-chess-position] identify a chess position, we store
- \(64b\) for piece colors + \({\sim}3b * 64\) for piece types
- \(64b\) for en-passant bitmap
- \(4b * 2\) for castling information
- \(1b\) for whose turn it is

which is too many to use as a key for a hash table, if we want it to be fast.
Ideally, we'd like to reduce those to 64, which is much nicer to work with while still having an extremely low chance of collision over the runtime of a standard chess game.

[**Zobrist hashing**](https://en.wikipedia.org/wiki/Zobrist_hashing) does this in a rather simple way -- we **generate random numbers** for all of the things mentioned above, and **XOR all that apply** (with an additional extra one for en-passant[^the-plus-one]) to create the game identifier:

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

It is **iterative**, because since XOR is commutative, we can XOR the current hash on what move was made, and don't need to calculate it from scratch every time the board changes.

I've also added Zobrist hashing to the current [perft implementation](#perft-tests), since that is a great way to test whether it works as it should.
Generally, you should only do this once the tests are passing without hashing, otherwise the debugging will be miserable (speaking from personal experience).

{: .commit-header}
[`a6156e`](https://github.com/xiaoxiae/Prokopakop/commit/a6156eec2fcbf0b0954e85c608375be4df5cf278)~[`f0253e`](https://github.com/xiaoxiae/Prokopakop/commit/f0253eebc1ee2ec9fdd17dde95d1b9b039ae073f)

Removes attack bitboards in favor of simply checking whether any pieces are attacking a particular square, since most code doesn't need them anyway, but they needed to be recalculated after each move.
Also does a bit of refactoring, but nothing too exciting.

{: .commit-header}
[`d7c5b4`](https://github.com/xiaoxiae/Prokopakop/commit/d7c5b4db78803fdc938c46d7f5c5e418d8782038)

Compacts a board move to \(16\) bits -- \(5 * 2\) for source + destination square indexes, and \(4\) for identifying a promotion piece (if applicable).
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

#### Legal Move Generation

Currently, we are generating legal moves by first **generating all [pseudo-legal moves](https://www.chessprogramming.org/Pseudo-Legal_Move)** (those where king can be under attack afterwards), **making** them, **checking** whether the king is in check afterwards, and finally **unmaking** them.

A faster approach is to generate [legal moves](https://www.chessprogramming.org/Legal_Move) directly, without having to modify the board state.
This, however, is much more complicated, as the king can come under attack in a number of tricky ways (most of which having to do with en-passant; curse the French!).
In prokopakop, I distinguish between three cases, depending on the **number of attacks** the king is under:
- **0 attacks**: normal generation, just watch for pins
- **1 attack**: king has to either **move away,** or the attacker must be **captured**; also watch for pins
- **2 attacks+**: king can **only move away**

Separating the cases makes legal move generation more manageable, and makes it much faster than make/unmake-based move generation.
Instead of going through the code (which, if you're interested, [can be found here](https://github.com/xiaoxiae/Prokopakop/blob/master/src/game/board.rs)), I'll point you towards **[Peter Ellis Jones' excellent blog post](https://peterellisjones.com/posts/generating-legal-chess-moves-efficiently/)** on legal move generation, as it was a great resource when implementing it myself.

{: .commit-header}
[`990204`](https://github.com/xiaoxiae/Prokopakop/commit/99020474e514d47bc72b25f46bc77fbd804b5dd7)~[`3ff11a`](https://github.com/xiaoxiae/Prokopakop/commit/3ff11a44e6945f5de5cdded988b73f611b9e5f62)

#### Const Generics

Besides small improvements/optimizations, the main change that I made was to replace most of the move generation code by [**const generic**](https://www.chessprogramming.org/Generic_Programming) variants.
This is just a fancy way of saying that most functions in my code have multiple variants for pieces/colors, which reduces the number of branches in the code and thus speeds it up.

It's important to note here that we're not talking about **runtime** variants, where a function takes a `Piece` and does different things depending on which piece it is.
In out case, this happens at **compile-time** -- instead of `make_move(piece, ...)`, we have `make_rook_move(...)` (as well as all other pieces).

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

gets evaluated at **compile time**, so all of this code will **only be included** in the **rook version** of the function.
No branching, no problem!

#### Summary

As we have reached the end of the move generation portion of this article, here is the speed of move generation across the commits that we've discussed.

![](/assets/chess-engine-from-scratch-by-commits/benchmark.webp)

As you can see, two three places stand out in this graph:
- the **first major spike in speed** (commit [`f0253e`](https://github.com/xiaoxiae/Prokopakop/commit/f0253eebc1ee2ec9fdd17dde95d1b9b039ae073f)) was caused by **removing the attack bitboards;** since these were previously calculated every move and consisted of evaluating all attacks of all pieces on the board, this is not surprising
- the **first major crash** (commit [`1d8e55`](https://github.com/xiaoxiae/Prokopakop/commit/1d8e55)) was caused by **starting to move away from the make/unmake-based move generation** by splitting each move generation into different functions based on the number of attacks; as this only included the spitting, but no optimized code, this introduced a large amount of branching that killed the speed
- the **second major spike** (commits [`a67205`](https://github.com/xiaoxiae/Prokopakop/commit/a67205) and [`5bc16a`](https://github.com/xiaoxiae/Prokopakop/commit/5bc16a)) were caused by **finishing moving away from the make/unmake-free move generation** by introducing functions optimized for zero/one/two+ king attacks

The engine is slower than Stockfish (\(9.74\text{s}\) vs. \(8.71\text{s}\) for `perft(7)`), but this is simply a skill issue because I'm not spending more time on this when I haven't written any search & evaluation functionality yet.
Maybe I'll revisit to take my revenge on Stockfish at some point in the future, but this will have to do for now.

### Search & Evaluation

Now that we can generate moves quickly (for some definition of quickly), we need to **search** through them to find the best one and **evaluate** the resulting positions.
Since chess is a zero-sum two-player game, we can simply **assign each position a score** (white is positive, black is negative) based on things like piece positions, counts, etc., and always pick the move that leads to the best score for the moving player.

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

While minimax is an important foundation to our search functionality, we can greatly improve it, as the first commit in this part of the article does, by using **[alpha-beta pruning](https://www.chessprogramming.org/Alpha-Beta)**.

Let's say that we we have just fully explored the move `A`, which was a regular move that gave us a slight advantage.
We then proceed to `B`, which is actually a blunder, and we find this out quickly after exploring the first opponent response, which is extremely strong.
Since the opponent has a **strong response**, which if he were to play would put us in a **worse position than `A`**, we can **prune** the rest of `B` -- no matter what the other moves are, if the opponent picks this response, it will be worse for us than the output of `A`, so we won't bother exploring just how bad it is for us.

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

We can see how these values get updated on the example we just covered -- first, exploring branch `A` returns {% chess inline %}+0.8{% endchess %}, which is then used to update \(\alpha\).
Next, exploration of branch `B` is started, with the first move returning {% chess inline %}-6.1{% endchess %}, which is then used to update \(\beta\).
At this point, we can see that \(\beta \le \alpha\), so we can prune the rest of the tree.

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

In prokopakop (as in most other engines), I have implemented this via **[negamax](https://www.chessprogramming.org/Alpha-Beta#Negamax_Framework)**, which simplifies the implementation by **always maximizing** and **flipping + negating** the alpha/beta values and evaluation when doing the recursive call, as we're changing perspectives.
This is very convenient, because it simplifies both the implementation and the conceptual meaning of alpha and beta -- we can now always think of **alpha** as the **lower bound** (what we are _guaranteed_ somewhere in the search tree), and **beta** as the **upper bound** (what the _opponent won't allow us to exceed_ because of what he has guaranteed somewhere in the search tree).

I have also implemented **[iterative deepening](https://www.chessprogramming.org/Iterative_Deepening)** for time management, which runs alpha-beta search with depths \(1, 2, \ldots\) until time runs out and returns the best result found, so we can limit time spent on searching based on the current time control.

Note that for alpha-beta search to work well, we need to ensure that the moves are **ordered** from strongest to the weakest, as exploring more interesting lines first will induce more cutoffs, as compared to when the moves are unordered -- we'll [implement this later](#mmv-lva).

#### Material Evaluation

As a final step in this initial seach/eval commit, I implemented a basic evaluation function, which simply counts material.
While this might seem like all you need, this is generally not sufficient as it doesn't take into account many nuances of the position, such as pawn structure, piece mobility, etc...

{: .commit-header}
[`8eeb84e`](https://github.com/xiaoxiae/Prokopakop/commit/8eeb84e)~[`6aec863`](https://github.com/xiaoxiae/Prokopakop/commit/6aec863)

#### Piece-Square Tables

This commit adds [**piece-square tables**](https://www.chessprogramming.org/Piece-Square_Tables) for positional evaluation.
These are a set of tables that, for each piece, provide information about how much it is worth when being on a particular square.
As an example, here is a pawn table:

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

Positive values correspond to places where pawns are more valuable, while negative values correspond to those where they are less valuable.
For pawns, these values try to incentivize center pawn pushes and promotions, and discourage advances of pawns used to protect the king.

For certain pieces, we can take this one step further and have **two tables** -- one for "early" game and one for "late" game (for some suitable definitions of early and late, such as total remaining material), and interpolate between them based on the current game phase.
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

As mentioned in the [alpha-beta section](#alpha-beta-search), for the moves to be pruned efficiently, we need to pick the strongest moves early so that they can be searched first and used for pruning the later branches.
While this is quite difficult to do in general, we can use heuristics that perform well in practice.
The most straightforward one is for ordering **capturing moves**, and it is exactly what you're thinking of -- capture the **m**ost **v**aluable **v**ictim with the **l**east **v**aluable **a**ttacker ([MVV-LVA](https://www.chessprogramming.org/MVV-LVA)).

This, combined with always searching the moves from the **p**rincipal **v**ariation first (best line found in the previous iteration of iterative deepening), gives a decent ordering and provides a good speed-up to the alpha-beta search.

{: .commit-header}
[`bbef3be`](https://github.com/xiaoxiae/Prokopakop/commit/bbef3be)

#### Quiescence Search

Using alpha-beta search with iterative deepening means that we always, for depths \(1, \ldots, n\), explore until a certain depth and then evaluate the position.
This has an obvious flaw: what if we make blunder, like taking a queen for a pawn, in the final depth?
Since this was the last depth that we were searching, this wouldn't get caught, and we'd happily return positive evaluation, since we're up a pawn!

This is where [quiescence search](https://www.chessprogramming.org/Quiescence_Search)[^quiescence] comes in -- when reaching the final depth of the iteration, it **extends the search** until **all remaining captures** (and possibly **checks**) are resolved, so that we are **only evaluating quiet positions** (i.e. those where there are no tactical sequences that can severely impact the score).
This way, we don't make obvious blunders because of a search cut short.

{: .commit-header}
[`35f6fb6`](https://github.com/xiaoxiae/Prokopakop/commit/35f6fb6)

#### Transposition Table

Re-evaluating a position we have already reached and evaluated would be a waste, so let's not do that and implement a [**transposition table**](https://www.chessprogramming.org/Transposition_Table) (TT).
Since we've already implemented [zobrist hashing](#zobrist-hashing), we can quickly identify explored positions and avoid needless computation... but what do we actually store?

Let's look at a minimax search first -- when evaluating a position, we examine **all moves** until a certain **depth**, so the calculated evaluation is **exact** up until the given depth.
When reaching this position again, we can use this already calculated value **if the depth we're searching to** is **less than or equal to the one we already did**.
Conversely, if the depth we're searching to exceeds the one we already explored, we need to actually do the computation.

Alpha-beta makes this slightly more difficult, because we're not exploring the entire tree.
This means that while we sometimes only get **bounds** on the evaluation, this is still useful information.
We distinguish two new cases:

1. If we **prune** a branch (i.e. cause a **beta cut-off**), it is because we found a move that is **too good** and the **other player** won't allow us to play it because they'll play something elsewhere in the tree (the move **fails high**).
   This means that the evaluation of this branch can **only get better** for us as we go through the moves, so we get a **lower bound** (/).
2. If we, on the other hand, go through **all moves** and **none of them improve alpha** (the move **fails low**), it means that the position can't score better than what we have found, and we have thus found an **upper bound**.

Adding these two cases, we store **three types** of nodes -- **exact**, **lower bound** and **upper bound**.
Implementation-wise, we'd store something like this:

```rust
pub enum NodeType {
    Exact,
    LowerBound,
    UpperBound,
}

pub struct TTEntry {
    pub key: u64,             // zobrist hash
    pub depth: u8,            // how far we searched
    pub evaluation: f32,      // evaluation of this branch
    pub node_type: NodeType,  // what type of information we obtained

    // These are not required, but useful
    pub best_move: Move,      // best move found
    pub age: u8,              // age of this entry, so we can clear the old ones
}
```

For implementing the TT itself, we can use a nice trick: instead of using a hashmap, use a **fixed array** of size \(2^n\) and the **first \(\mathbf{n}\) bits** of the zobrist hash as an index... because why would we hash twice?

There are many other things to consider like [replacement strategies](https://www.chessprogramming.org/Transposition_Table#Replacement_Strategies) and more advanced TT implementations, such as using  [buckets](https://www.chessprogramming.org/Transposition_Table#Bucket_Systems), but I won't go into detail on those as we've covered the core concepts behind TTs.

_A small terminology note: when doing research for this article, I found that the three [node categories](https://www.chessprogramming.org/Node_Types) described above are sometimes called **PV** (exact), **Cut** (lower bound) and **All** (upper bound) nodes, so don't be surprised when you see these terms used; they refer to the node types.
This mainly originates from a [2003 paper](https://dke.maastrichtuniversity.nl/m.winands/documents/Enhanced%20forward%20pruning.pdf) about pruning methods[^alpha-beta]._

{: .commit-header}
[`ff14c29`](https://github.com/xiaoxiae/Prokopakop/commit/ff14c29)~[`6c4e7ee`](https://github.com/xiaoxiae/Prokopakop/commit/6c4e7ee)

I've added threefold repetition detection, but only for the first few [plys](https://www.chessprogramming.org/Ply) (this is what the chess people call turns, and corresponds to the current depth we're in[^ply]), since the check can be rather expensive.
In addition, I've improved the evaluation function to incentivize [passed pawns](https://www.chessprogramming.org/Passed_Pawn), penalize [doubled pawns](https://www.chessprogramming.org/Doubled_Pawn), and account for [piece mobility](https://www.chessprogramming.org/Mobility) by counting moves available to each piece from both sides.

{: .commit-header}
[`a28d291`](https://github.com/xiaoxiae/Prokopakop/commit/a28d291)

#### Killer Moves

In certain positions, there are responses that can act as refutations to multiple moves that the opponent might like to play.
As an example, if pushing a pawn kicks out an annoying knight, it can also be a good response to the opponent's other moves, like blocking a bishop, threatening a pushed pawn, etc...

More specifically: if a move **causes a beta cut-off**, it means that it's likely a good response and should be prioritized in sibling branches.
To do this, we **remember it for this ply** and **prioritize it in move order**.
Since we already have [MVV-LVA](#move-ordering), which handles capture ordering well, we will only do this for non-capture (i.e. quiet) moves.

In practice, it is usually better to store **two** moves for each ply, because there can be cutoffs that are not really killer and could mess with the move ordering.
The implementation itself is very easy (with suitable updates as we traverse the search tree):

```rust
pub struct KillerMoves {
    // 2 killer moves per ply
    killers: Vec<[BoardMove; 2]>,
}
```

{: .commit-header}
[`2c1a839`](https://github.com/xiaoxiae/Prokopakop/commit/2c1a839)

#### Delta Pruning

Up until now, all of the things[^quiescence-is-not-exact] that we implemented were a part of the classical alpha-beta algorithm, which means that the calculated score for the given depth was **exact**... but that's still too slow for us.
Let's start cutting corners 😎.

We'll begin by implementing [**delta pruning**](https://www.chessprogramming.org/Delta_Pruning) for quiescence search.
It's a rather intuitive heuristic on whether we should explore a particular move -- if **capturing the piece** + some **safety margin** (usually two pawns), is **not sufficient to raise alpha**, then we don't bother exploring the move at all since we are, as the kids say, beyond cooked and the position is hopeless.

While this will speed up the search because we're no longer exploring likely hopeless positions, we can miss certain tactical sequences, especially those that swing the evaluation by more than the safety margin (since that's the maximum we're assuming we could gain).
It is therefore recommended to **not use this heuristic when approaching the endgame**, because we might need to sacrifice some material for positional advantage and conversion.

Techniques that prune branches with the risk of overlooking things are referred to as [**forward pruning**](https://www.chessprogramming.org/Pruning#Forward_pruning_techniques), and we'll be implementing a lot more of them in the next few commits, since we've mostly run out of the regular (sometimes called "backward") pruning techniques that keep the evaluation exact.

{: .commit-header}
[`10c64e9`](https://github.com/xiaoxiae/Prokopakop/commit/10c64e9)

#### Null Move Pruning

Let's cut the corners even further!

**[Null move pruning](https://www.chessprogramming.org/Null_Move_Pruning)** uses the simple observation that **skipping a turn** (i.e. making a null move) is almost[^nmp] always worse than **making the best move** in the position.
Therefore, it's a relatively safe assumption that if making a null move causes a **beta cut-off** (i.e. even not making any move is so good and the opponent wouldn't let us play it), we can **prune this entire branch** without exploring any of the moves, since the best move is bound to be better than no move at all.

Implementation-wise, two things to mention:
- The search on the null move uses a **reduced depth** (either flat or progressive), because it should usually be apparent quite quickly whether a beta cut-off will occur or not.
- If the evaluation of the current position is **below beta** (with some margin), we **don't need to try null move pruning**, since it extremely unlikely to result in a beta cut-off anyway.

{: .commit-header}
[`5047857`](https://github.com/xiaoxiae/Prokopakop/commit/5047857)

#### Late Move Reduction

The shape of our engine is still not spherical enough -- more corner cutting!

With move ordering implemented ([MVV-LVA](#move-ordering), [principal variation](#move-ordering), [killer moves](#killer-moves) and [transposition table](#transposition-table)), we usually have a good idea on which moves look promising, and we explore those first to induce as many cut-offs as possible.
It therefore stands to reason that **quiet moves** that come **later in the move order** (hence the name **[late move reduction](https://www.chessprogramming.org/Late_Move_Reduction)**) are **not that interesting**.

To not waste time, we explore them with a **reduced depth** and distinguish two cases:
- If they **don't improve alpha** (fail low), we were right -- they are not interesting and we **do not** explore them further.
- If, on the other hand, they **do exceed alpha**, we need to **re-run the search with the original depth**, since we don't want to miss a potentially interesting line.

Take note that in this case, we **don't care about beta** when checking the result of the reduced search, since we're expecting the moves to be bad anyway -- we only care about checking that they're worse than alpha and so not worth consideration.

{: .commit-header}
[`da6dbb0`](https://github.com/xiaoxiae/Prokopakop/commit/da6dbb0)

#### Aspiration Windows

When doing iterative deepening, each successive iteration returns an evaluation of the position.
If we have a well-behaved alpha-beta implementation and evaluation function, the evaluation will not swing wildly as the search goes on, but instead stabilize around some "true" evaluation of the position.

[**Aspiration window search**](https://www.chessprogramming.org/Aspiration_Windows) takes advantage of this observation by **setting the alpha and beta bounds** in alpha-beta search to **the previous iterative deepening iteration result** \(\pm\) some **margin** (usually half a pawn).

Running this search, two things can happen with the root result:
- The evaluation is **within the bounds** of the aspiration window, which means we were correct and this is the **true evaluation**. Yippie!
- The evaluation is **outside the bounds** (either fail low or fail high), which means that the guess was wrong; in that case we need to **re-search** with a **larger window** (usually extending the side of the bound that failed), until the search succeeds. Boo!

Aspiration windows were difficult for me to understand initially, so here is the observation that made it click: if the value calculated from alpha-beta search **falls within the alpha-beta bounds**, then it is **exact**.
This is because we found a line that leads to a position with the expected evaluation, and there is no line that is better/worse than the provided bounds.

If we missjudge the position, and there is a line outside of this evaluation, then this will lead to a fail (low or high) and the aspiration window search will return only a bound -- since we don't know what the actual value is, we have to re-run.

{: .commit-header}
**To be continued?**

#### Summary

I'll end the article here (at least for now), since I'm still actively developing the engine, so waiting until it's complete would likely mean that I would take this to my grave.
If people find this interesting, I'll keep updating it as more commits come in, but this is definitely more than enough to write an engine that will beat most chess players with relative ease.

Here is a table of engine performance against previous versions.
As you can see, it's getting smarter, and if we interpolate

[^all-you-need]: Okay, not quite; you also need to cast {% ihighlight rust %}Color::White as usize{% endihighlight %}, but that's ugly and an implementation detail, so I skipped it for the sake of clarity. You can get rid of it by implementing indexing for the array type, but I haven't done that because I'm lazy.

[^the-plus-one]: This is done so that we don't need to check whether en-passant bit changed during the move (since that adds branching, which is slow) -- we therefore add an additional "no-op value", which will be used when en-passant didn't happen; since we're XORing twice, these cancel out and we don't need to branch!

[^lc0]: Some chess engines, like [Leela Chess Zero](https://lczero.org/), use [Monte Carlo tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) instead. This is because their position evaluation is orders of magnitude slower but much more advanced, so they do a deeper search on promising lines instead of a wide one on all of them.

[^unique-chess-position]: This is not quite correct, as we're wasting a bit; e.g. there are 6 pieces and we're using 3 bits. If we really tried, we could get it down to \[\log_2(\left(2 \cdot 6\right)^{64} \cdot 16 \cdot 8 \cdot 2) \cong 237.4 \] which saves a couple of bits, but still doesn't solve the problem.

[^quiescence]: I'm not a native speaker, so this seemed like a strange usage of this word. The definition of "quiescence" is, according to the Cambridge English Dictionary, _the state of being temporarily quiet and not active_, so this makes sense -- we want to **search for quiet positions** and only evaluate those.

[^ply]: The origin of the word "ply" comes from _pli_, [which is old French](https://www.etymonline.com/word/ply) for "layer".

[^alpha-beta]: As a side-note, they refer to alpha-beta seach as \(\alpha\beta\) search and I find that very funny.

[^nmp]: This is not true for [Zugzwangs](https://www.chessprogramming.org/Zugzwang), which, by definition, are positions where making a move is worse than not making a move. These usually happen in pawn endgames, so it's best to turn NMP off in those cases.

[^quiescence-is-not-exact]: Okay, this is not quite true. We've already implemented quiescence search, which in and of itself is not exact as we're skipping non-capture and non-check moves. This is a bit tricky, however, since we could think of it as an extended static evaluation.

<!--
// TODO topics; ignore these
// ## PV-search
// - Implemented Principal Variation (PV) search algorithm
// - Significant improvement to the search tree exploration
// - Enhanced move ordering and search efficiency through better handling of expected best moves
//
// ## ordering via move history
// - Implemented move history heuristics for improved move ordering
// - Added historical move scoring to guide search prioritization
// - Enhanced search efficiency through better move selection
//
// ## Quiet move pruning
// - Implemented quiet move pruning techniques to reduce search tree size
// - Added sophisticated pruning logic to skip unlikely quiet moves in certain positions
// - Improved search efficiency without sacrificing playing strength
//
// ## basic king safety + factor out eval magic constants + eval command
// - Implemented fundamental king safety evaluation
// - Added king zone attack calculations and weightings
// - Introduced eval command for position analysis
// - Refactored evaluation constants for better maintainability
//
// ## king zone attacks & more significant king zone attack weight
// - Enhanced king safety evaluation with detailed king zone attack analysis
// - Increased the weight of king zone attacks in position evaluation
// - Improved tactical awareness around king safety
-->
