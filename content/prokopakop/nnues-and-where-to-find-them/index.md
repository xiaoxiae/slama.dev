---
date: '2026-01-07'
title: NNUEs, and Where to Find Them
description: "Writing more of my chess engine from scratch, in Rust, commit by commit; this time with 56% more NNUEs."
end: <a href="/prokopakop/1/">Part 1</a>, <strong>→ Part 2 ←</strong>
draft: true
toc: true
---


It turns out that it's easier to start writing a chess engine than to stop writing it.
This is something I wish I had known when I was starting, but it's too late now so I might as well write another blog post to document the things that I've learned, and gloat a bit since [the **Prokopakop engine**](https://github.com/xiaoxiae/prokopakop) is now [much stronger](https://lichess.org/@/prokopakop).

When I was initially writing the engine, I was eyeing the [NNUE architecture](https://www.chessprogramming.org/NNUE), since replacing a painstakingly hand-crafted evaluation function with a gradient-(de)scented one sounded very appealing, but I wouldn't spare it too much time since most of the engine was on fire.

Now, with the search functionality mostly in-place (modulo a few stragglers), the limiting factor is once again the evaluation, which is what I'll spend most of this article on.

So, without further ado, **let's get some elo** and kop some prokops.

### Search

{{< image_section caption="A meme about search." >}}
{{< image_row "i-lied.png :: A meme about search." >}}
{{< /image_section >}}

Jokes aside, there are a few search techniques that I couldn't cover in the previous blog post because it was getting too long, so I'll sneak these in here and hope you won't mind.

<details class="skip-section" id="trap">
<summary>If you do, feel free to <a href="#">skip this section</a>...</summary>

...you thought you could get away?

The search section got **three times longer.**

There is no escape.

T̶h̴e̶r̸e̶ ̷i̷s̷ ̴n̴o̴ ̵e̷s̷c̴a̴p̷e̶.̷

T̶̩̏h̸̥̬̎͊̊̇͂̌̊ȩ̶̻̺̲̇͠r̵̢̛̺̥͖̟̙̫̆̂̑ę̷̘͔̼̤̉ ̵̯͚̰̺̾į̷̡̾́͆͑͐̃̿ş̷̜̺͉͙̱̙͝͠ ̷͎̝̦͉̣̦͛n̵̨̯̦̻͗̈́͋̓́ō̷̳̱̱̊ ̸̜̻̬͙̺̼̜́̋͆͑̓̕͠ë̷̳̝̞͇́̇̅͜͠s̴̙̺͉̒͑͋̉̓͜c̵̨̫̤͙͉̪̳͗̋͑͑̆͘a̷̛̫̠̓̌̑̿͝͝p̷͖̦̉̀͆̒͋͌͝ę̷̞̥̳̖̌̽͛͆̉̕̚ͅ.̷͓̰̖̂̃͗̕͝

<br/>

Just kidding again, here is [evaluations](#evaluation).
</details>

[`7cfbb74`](https://github.com/xiaoxiae/Prokopakop/commit/7cfbb74)
{.commit-header}

#### PV-search

The [**P**rincipal **V**ariation search](https://www.chessprogramming.org/Principal_Variation_Search) starts off, like most of the other optimizations that we discuss, with a simple observation -- the principal line that we explored in the previous iteration of iterative deepening was hopefully good, so we assume that we **won't deviate from it** in the next deepening iteration (except the last depth).

We can do this by doing two things:
- search the **first move** regularly, with a **full window** (`[alpha, beta]`)
- for **subsequent moves**, search with a **null window** (`[alpha, alpha + 1]`), and **re-search** if it fails

A null-window search noly answers the question **is this better than what I already have**, which is exactly what we want in this case to confirm that the PV is the best.
Since we're usually right and null-window searches are much faster (only answers yes/no, not by how much better), this saves time, even though we sometimes have to re-search if we're wrong about PV.

<!--
[`5ddad41`](https://github.com/xiaoxiae/Prokopakop/commit/5ddad41)
{.commit-header}

#### Improved TT

https://www.chessprogramming.org/Transposition_Table
-->

[`d00348d`](https://github.com/xiaoxiae/Prokopakop/commit/d00348d)
{.commit-header}

#### History Heuristic

> Back in my day...

In the [previous article](/a-chess-engine-commit-by-commit), we have implemented many move ordering heuristics, such as [MVV-LVA](/a-chess-engine-commit-by-commit/#move-ordering).
While these were all useful in their own right, quiet moves have remained mostly untouched, since they're... well... quiet, so it's hard to judge whether one is better than another.

The only thing we're doing right now for ordering quiet moves is the [killer heuristic](/a-chess-engine-commit-by-commit/#killer-moves), which remembers **moves** that **caused a beta cut-off** in other branches in the **same ply** of the search tree.
The **[history heuristic](https://www.chessprogramming.org/History_Heuristic)**[^history-heuristic] is what you get when you take this to the extreme --  if a move was **good** (i.e. caused a beta cut-off), we should **prioritize** it over **other quiet moves in ALL future searched positions**.

[^history-heuristic]: [This paper](https://webdocs.cs.ualberta.ca/~jonathan/publications/ai_publications/pami.pdf) by Jonathan Schaeffer gives a good overview of the history heuristic (among other things).

Implementation-wise, we can store `[side][sq_from][sq_to]`, which will keep track of how good these moves were in the past, and will be updated as follows; if a move
- causes **beta cutoff**: `[side][from][to] += depth * depth`
- **doesn't improve alpha**: `[side][from][to] -= (depth * depth) / 2`

The reason for using depth instead of constant values is that deeper cutoffs are more significant than shallower ones.

To make sure entry values don't explode, we can **decay** all entries over time (i.e. divide by 2 after each added move), or interpolate to some max value based on current value and depth for the given square (as Stockfish does).


[`7490eba`](https://github.com/xiaoxiae/Prokopakop/commit/7490eba)
{.commit-header}

#### (Reverse) Futility Pruning
> Resistance is futile. (Jar Jar Binks)

**[Futility pruning](https://www.chessprogramming.org/Futility_Pruning),** as well as its **[Reverse Futility Pruning](https://www.chessprogramming.org/Reverse_Futility_Pruning)** counterpart, prune positions that are **futile** (for either side), since they're unlikely to change the outcome at that point.

What this means is that if we're in a quiet position which, according to static evaluation, is **hopeless** and we are looking at a **quiet** move, it's a reasonable assumption that it's not going to help us and we can **skip it**; specifically (`static eval + margin(depth) <= alpha`).
The higher depth we have remaining, the larger the margin should be for us to not miss tactics (i.e. `[0, 100, 200, 300, ...]`).

Similarly, if our position is **amazing** (`static eval - reverse_margin(depth) >= beta`), we can **skip the branch entirely** since, no matter the type of move, we will not get to play it anyway (again setting margins depending on the remaining depth).

[`85e2dae`](https://github.com/xiaoxiae/Prokopakop/commit/85e2dae)
{.commit-header}

#### Improving Time Management
> Time goes by. So slowly. (Britney Spears)

I skipped this entirely in the [previous post](/a-chess-engine-commit-by-commit/) since I didn't have time (heh, get it?), but since this commit makes signiticant improvements in how time per move is allotted, it's a good idea to mention it here.

This is how much time Prokopakop currently assigns to each move:

```rust
let base_time = available_time / moves_until_increment.max(1);
let allocated_time = base_time + (increment * 8 / 10);
```

Since we're usually playing games without a fixed move count until time control, `moves_until_increment` defaults to \(30\) (or some other arbitrary value, based on how fast you want to decay), and so the remaining time decays exponentially as the moves go on.

While this sounds great on paper, implementing it like this is problematic -- when the time runs out for a given step, the engine has to **kill the current iterative deepening iteration** and **discard the result** (unless you're being very meticulous), since premature stopping can lead to incorrect move selection.

What this commit does to prevent this is to first calculate an **estimate** on how long the next iteration of iterative deepening will take, as a **multiple of the previous** (set to `2.5x`).
If the estimate exceeds the remaining time, the engine will **skip the next iteration** and **return the current best result**, since it's likely that the time would be wasted as the iteration wouldn't have completed.

While crude, it matches the search quite well, as seen on a plot of time vs. depth when searching from the starting position.
Although there are positions more/less complex than this, even a rough estimate is a good improvement over the naive kill+discard approach method.

{{< image_section caption="Search time / nodes vs. depth from the starting position." >}}
{{< image_row "scaling.png :: Search time / nodes vs. depth." >}}
{{< /image_section >}}

To see this in action, the image below shows the search time of an engine that **doesn't** implement this (white), and an engine that **does** (black).
Black won that game, because it's my engine and I wouldn't show you a loss.

{{< image_section caption="Time-per-move graph for <a href=\"https://lichess.org/@/RavenEngine\">RavenEngine</a> (white) vs <a href=\"https://lichess.org/@/Prokopakop\">Prokopakop</a> (black)." >}}
{{< image_row "time-management.png :: Time-per-move graph of two chess engines." >}}
{{< /image_section >}}

[`c056f9b`](https://github.com/xiaoxiae/Prokopakop/commit/c056f9b)
{.commit-header}

#### Static Exchange Evaluation

> To make alpha-beta faster, we must not use alpha-beta. (Sun Tzu, probably)

During [quiescence search](https://www.chessprogramming.org/Quiescence_Search), we're resolving tactical sequences to get rid of the [horizon effect](https://www.chessprogramming.org/Horizon_Effect).
This usually involves captures, since these are at the heart of many tactics, so resolving them quickly is important.

Until now, we've resolved them by simply playing them out as recursive quiescence search calls, but we can do better.
There are many capture sequences that we don't ever need to consider, since they're obviously bad (think `Qxp` followed by `pxQ`) and do not warrant a function call and all that comes with it.

This is where [**static exchange evaluation**](https://www.chessprogramming.org/Static_Exchange_Evaluation) comes in handy -- instead of recursive calls, we will do the evaluation **statically**, calculating the **overal result** instead of recursing, since that's the only thing we need in quiescence search.

While the implementation is a bit tricky to get both right and fast, the core idea is simple: there are **pieces attacking a square with a piece**. We want to calculate what is the **material gain of the sequence** by iteratively **simulating the captures**.

There are two observations that produce the algorithm that we'll use. The first observation is that each of the players can **stop** capturing at **any time**.
This means that while one player might have overwhelming material advantage (i.e. 2 queens), they shouldn't capture a pawn if it's being protected by a bistop.

The second observation is that it's **always optimal** to capture with your **lowest-value** piece[^checks], since the opponent can always chose to stop capturing and so you didn't help anything by sending higher-valued pieces earlier.

[^checks]: This is not true, since we're ignoring checks, in-between moves (usually checks), sacrifices, and other tactics. However, quiescence search is not the right place to explore these and they will be explored properly in alpha-beta afterwards anyway, so we're fine.

Here is the algorithm in a nutshell:

```rust
let mut gains = [0.0f32; 16];  // max 16 captures
let mut depth = 1;

// Player 1 starts with the value of the piece they captured
let mut captured_value = get_see_piece_value(target_piece);

// Simulate exchange
loop {
    // Find smallest attacker for current side
    let (attacker, attacker_sq) = match self.get_smallest_attacker(square, side, occupied) {
        Some(sq) => sq,
        None => break,
    };

    // Store what we're capturing
    gains[depth] = captured_value;

    // Update for next iteration
    occupied &= !attacker_sq.to_mask();  // take piece
    captured_value = get_see_piece_value(attacker);
    side = !side;
    depth += 1;

    if depth >= 16 {
        break;
    }
}

// Minimax: each side chooses stop vs continue
while depth > 1 {
    depth -= 1;
    gains[depth] -= gains[depth + 1].max(0.0);
}

gains[1]
```

The core of the algorithm is in the final while loop -- going from the end, **each player** makes the decision to **stop capturing** at that point if it's not optimal for them (this is what `max` is doing).
Since we're doing this as negamax (always subtracting and thus swapping between the colors), the player will **never** want to play out a sequence that will yield a **negative score**, which is what we're calculating by accumulating it from the end.

Besides quiescence search, you can use SEE to [**order capture moves**](https://www.chessprogramming.org/Static_Exchange_Evaluation#Move_Ordering) -- a lot of engines (mine included) do

\[... > \text{good captures} > \text{quiet moves} > \text{bad captures} > ...\]

since good captures tend to be better than the bad ones.

### Evaluation

With the search functionality working reasonably well, we can focus on improving the evaluation.

The current way we're doing it will not scale well, as it's hand-crafted.
We can improve it up to a point, but wouldn't it be so much easier to descent some gradients instead?

[`a91a3f2`](https://github.com/xiaoxiae/Prokopakop/commit/a91a3f2)~[`5063949`](https://github.com/xiaoxiae/Prokopakop/commit/5063949)
{.commit-header}

#### King Safety

Before we proceed to NNUEs, I've made some final improvements to the hand-crafted evaluation, namely king safety.
Until now, I haven't really paid attention to king safety, but it is arguably one of the most important parts of eval, as a king in danger can easily add \(\pm 500\) centipawns.

The implementation penalizes a few things; namely:
- **missing pawn shield** in front of the king,
- **(semi)-open files** next to the king and, most importantly,
- **attacks near the king** (in the king zone), **weighted** by the attacker

The first two are pretty self-explanatory, but the third one is interesting.
The idea behind it is that the more attacks there are around the king, the more exposed it is, with the values **per attacked square** being

```rust
const PAWN_ATTACK_WEIGHT: f32 = 1.0;
const KNIGHT_ATTACK_WEIGHT: f32 = 2.0;
const BISHOP_ATTACK_WEIGHT: f32 = 2.0;
const ROOK_ATTACK_WEIGHT: f32 = 3.0;
const QUEEN_ATTACK_WEIGHT: f32 = 5.0;
```

and the area around consisting of a \(3 \times 4\) square like so:

{{< chess >}}8 ........
7 ..♗.....
6 ...\....
5 ....!••.  the bishop hits
4 ....•!•.  3 squares, adding
3 ....•♚!.  penalty of 3x2=6
2 ....•••\
1 ........
  abcdefgh
{{< /chess >}}

To further emphasise that king safety is important, the penalty increases quadratically since danger doesn't increase linearly -- the more attackers, the worse it gets, _by quite a lot._

#### Removing Schizophrenia
I found this commit when looking through the Git history and thought it was funny.

```text
* 3d536e8 | 2025-09-30 | xiaoxiae | make the engine not schizophrenic
```

I did not remember what I did, and  as it's not particularly descriptive, I wondered what it contained.
Running `git show` revealed the following:

```diff
-    -danger * danger / SQUARE_ATTACK_FACTOR
+    -(danger * danger) * SQUARE_ATTACK_FACTOR
```

This, with `SQUARE_ATTACK_FACTOR` being `1/50` effectively meant that before this commit, the engine was **extremely paranoid** about king safety and would do anything to keep the king safe.

I stand by the commit message.

[`9cfd936`](https://github.com/xiaoxiae/Prokopakop/commit/9cfd936)~**current**
{.commit-header}

#### [NNUE](https://en.wikipedia.org/wiki/Efficiently_updatable_neural_network)s

**Ǝ**fficiently **U**pdatable **И**eural **И**etworks, are a relatively new addition to the game of chess (~2018), and have revolutionized chess engines unlike (arguably) anything that came before them.

Traditionally, an evaluation function would be fast and hand-crafted (possibly tuned via a learning algorithm), due to the fact that a quicker evaluation function means deeper search and thus (generally) a better engine.
This can work fine initially, but as the complexity of the function and the number of parameters increase, hand-crafting and tuning quickly becomes infeasible.

With the advent of [AlphaZero](https://www.chessprogramming.org/AlphaZero), neural networks came into the chess engine scene in a big way, as AlphaZero [decisively defeated Stockfish](https://en.wikipedia.org/wiki/AlphaZero#Final_results), the best chess engine in the world at the time  (arguably still is).
It used [Monte-Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) instead of alpha-beta, since the evaluation was significantly slower than a standard evaluation function (around **1000x**), and it wouldn't get too far going layer-by-layer.

Although the AlphaZero architecture was markedly different from classical chess engines and so couldn't be immediately applied, its massive success raised an important question -- would a small, carefully designed neural network, outperform hand-crafted evaluations?

Spoiler alert: **yes.**

##### Overview

Let's say we want to evaluate a chess position using a neural network.
The simplest thing we could do is to use a **fully-connected network** (see my [ML course lecture notes for details](http://localhost:1313/notes/introduction-to-machine-learning/#neural-networks)) with a suitable input and a single float output, which would tell us how good the position is.

The input can take many shapes, but the easiest would be a **one-hot encoding** of the board state, with each combination of square/piece/color corresponding to a single neuron, for a total of \[6 \times 2 \times 8 \times 8 = \mathbf{768}\] input neurons.

The core idea behind NNUEs is the following: after a move is made, **what values do we actually need to change to update the network**?
It will of course be the neurons in the first layer corresponding to the changed pieces, but how about the others?

Since we're dealing with a fully connected network, we only need to update the values of the neurons that the **changed input neuron is connected to** (and the subsequent layers), instead of having to re-calculate the entire network.
If the network is shallow enough (i.e. 1 hidden layer), the number of operations needed for the evaluation then corresponds **linearly** to the **size of the** (single) **hidden layer**.

![](network.svg "Basic NNEU architecture examples -- **A)** shows the portion of the network to be recalculated (blue),<br>**B)** shows an improved NNUE architecture with two accumulators,<br>**C)** adds two buckets for early/late game weights.")
{.no-invert}

Since the first hidden layer repeatedly adds/subtracts values based on how the pieces move on the board, it is referred to as the **accumulator**.
Usually, **two accumulators** are used instead, one for the **side to move** and the other for the **side not to move**, since this takes full advantage of the game symmetry and allows the network to learn different features for both the "player" (positive) and "opponent" (negative).

Updating code for adding a piece to the board is then as simple as

```rust
fn add_piece(square: Square, piece: Piece, color: Color, net: &Network) {
    // We're updating two accumulators, one from each point of view
    // 
    // In practice, we'll just call one 'white', the other 'black'
    // and swap them during evlauation, since the side-to-move switches
    let white_idx = Self::calculate_white_feature_idx(square, piece, color);
    let black_idx = Self::calculate_black_feature_idx(square, piece, color);
    
    self.white_accumulator.enable_index(white_idx, net);
    self.black_accumulator.enable_index(black_idx, net);
}
```

for

```rust
pub fn enable_index(&mut self, idx: usize, net: &Network) {
    let weights = &net.weights[idx].vals;
    
    // Accumulate weights for the activated neuron
    for (acc, weight) in self.vals.iter_mut().zip(weights) {
        *acc += weight;
    }
}
```

and analogously for removing a piece (just subtract instead).

The evaluation is then just

```rust
pub(crate) fn evaluate(&self) {
    let net = get_network();

    // Swap for side-to-move and side-not-to-move to be in the correct place
    match self.side == Color::White {
        true => net.evaluate(&self.white_accumulator, &self.black_accumulator),
        false => -net.evaluate(&self.black_accumulator, &self.white_accumulator),
    }
}
```

While this will work and you can train a really good chess engine this way, NNUEs have a few more tricks up their sleeves to make them faster and more accurate.

##### [Quantization](https://www.chessprogramming.org/NNUE#Quantization)

**Quantization** has become a rather well-known term in these times of LLMs.
By quantizing a network, we are converting the network layers to use **integer types** (i.e. `f32 -> i16`), since they have **faster multiplication**.
This can be done by simply **multiplying by a constant factor** (say `Q`), converting to int to fit within the required data type.

This will mean that we have to **keep track** of the current quantization factor so we can de-quantize as we go through the layers, and that the more layers the network has, the more the **quantization errors propagate** though the network, but these are non-issues since our network is very shallow -- in our case, the quantization is very manageable.

While the details are heavily dependent on the network architecture, I'll walk through how the one in Prokopakop works.
I'm using the **[Bullet library](https://github.com/jw1912/bullet)** for training NNUE training Rust library.
We'll be quantizing the input layer to `QA` and the hidden layer to `QB`, and will use **screlu** as the activation function:

{{< chess >}}   ----        ----
   side        side
    to        not to
   move        move
   ----        ----
    │           │
    ↓           ↓
   Linear(768, 128)      // quant = QA
    │           │
    ↓           ↓
 SCReLU()    SCReLU()    // quant = QA * QA
    │           │
    │  Concat   │
    └─────┬─────┘
          │
          ↓
    Linear(256, 1)       // quant = QA * QA * QB
          │
          ↓
       Output
{{< /chess >}}

You might think that it's strange for the quantization to have an extra `QA`, but that comes from the fact that we're using screlu which squares the input.

Putting this together, we get

```rust
impl Network {
    /// Calculates the output of the network, starting from the already
    /// calculated hidden layer (done efficiently during makemoves).
    pub fn evaluate(&self, us: &Accumulator, them: &Accumulator) -> i32 {
        // Initialise output.
        let mut output = 0;

        // Side-To-Move Accumulator -> Output.
        for (&input, &weight) in us.vals.iter().zip(&self.output_weights[..HIDDEN_SIZE]) {
            output += screlu(input) * i32::from(weight);
        }

        // Not-Side-To-Move Accumulator -> Output.
        for (&input, &weight) in them.vals.iter().zip(&self.output_weights[HIDDEN_SIZE..]) {
            output += screlu(input) * i32::from(weight);
        }

        // Reduce quantization from QA * QA * QB to QA * QB,
        // since bias has been quantized with QA * QB only.
        output /= i32::from(QA);

        // Add bias.
        output += i32::from(self.output_bias);

        // Apply eval scale.
        output *= SCALE;

        // Remove quantisation altogether.
        output /= i32::from(QA) * i32::from(QB);

        output
    }
}
```


##### Bucketing

TODO
