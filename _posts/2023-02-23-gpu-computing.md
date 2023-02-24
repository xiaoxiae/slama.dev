---
title: GPU Computing
category: "notes"
category_icon: /assets/category-icons/heidelberg.webp
---

- .
{:toc}

{% lecture_notes_preface_heidelberg Kazem Shekofteh|2022/2023%}

### Lecture overview

1. Introduction [[slides](/assets/gpu-computing/01.pdf)]
2. CUDA programming [[slides](/assets/gpu-computing/02.pdf)]
3. Basic architecture [[slides](/assets/gpu-computing/03.pdf)]
4. Matrix multiplication optimizations [[slides](/assets/gpu-computing/04.pdf)]
5. Parallel computing [[slides](/assets/gpu-computing/05.pdf)]
6. Profiling [[slides](/assets/gpu-computing/06.pdf)]
7. Scheduling optimizations [[slides](/assets/gpu-computing/07.pdf)]
8. \(n\)-body optimization [[slides](/assets/gpu-computing/08.pdf)]
9. TODO [[slides](/assets/gpu-computing/09.pdf)]
10. TODO [[slides](/assets/gpu-computing/10.pdf)]
11. TODO [[slides](/assets/gpu-computing/11.pdf)]
12. TODO [[slides](/assets/gpu-computing/12.pdf)]
13. TODO [[slides](/assets/gpu-computing/13.pdf)]

### Bulk-Synchronous Parallel (BSP) model
- established in 1990
- attempt to describe GPU computing
- parallel programs are split into **supersteps**
	1. _compute_ something
	2. _communicate_ what you did
	3. _synchronize_ with other processors
- **parallel slackness:** number of virtual processors \(v\), physical processors \(p\)
	- \(v = 1\): not viable
	- \(v = p\): unpromising wrt. optimality
	- \(v \gg p\): leverages slack to schedule and pipeline computation

### Scaling rules

#### Moore's law
A law about the exponential increase of processing power, has many variants:
- 1965: **number of transistors will double each year**
- 1975: every two years
- CPU performance will double every 18 months,
- memory size four times every three years, etc.

#### Amdahl's law
We want to find the **maximum possible improvement**, when given
- \(P\) parallel time of the task, \(S\) serial time of the task, \(P + S = 1\)
- \(N\) parallel execution units
\[\mathrm{Speedup} = \frac{1}{S + \frac{P}{N}}\]

### CUDA programming
- compute kernel as C program
- explicit data and thread-level parallelism
- **computing**, not graphics processing

A program always consists of **CPU** (no/little parallelism) and **GPU** (high parallelism) part.
The **GPU** part is made up of **kernels**, which are C functions that are executed on the GPU:

```cuda
__global__ void matAdd (float A[N][N], float B[N][N], float C[N][N])
{
	// one thread computes one element
	int i = blockIdx.x * blockDim.x + threadIdx.x;
	int j = blockIdx.y * blockDim.y + threadIdx.y;
	
	// compute only if we're within bounds!
	if (i < N && j < N)
		C[i][j] = A[i][j] + B[i][j];
}

int main()
{
	// the thread grid and block structure is 2D, 2D
	dim3 dimGrid((N + dimBlock.x – 1) / dimBlock.x, (N + dimBlock.y – 1) / dimBlock.y);
	dim3 dimBlock(16, 16);
	matAdd <<<dimGrid, dimBlock>>> (A, B, C);
}
```

- general syntax is `kernel <<<blockCount, blockSize>>> (args)`
	- `blockCount` and `blockSize` can be 1D/2D/3D, depending on the type of problem
- each **thread** has a unique `threadIdx.{x,y,z}`
- each **block** has `blockIdx.{x,y,z}` (and `blockDim.{x,y,z}` for size)
	- will be assigned to **one streaming multiprocessor** (i.e. will have shared memory)
	- they are sometimes called _Cooperative Thread Arrays_ (CTAs)
- we have to make sure that the GPU has enough SMs and threads/block to start!

{: .no-invert}
![Thread and memory diagram for CUDA.](/assets/gpu-computing/grid-block-thread.webp)

#### Memory

##### Global memory
- accessible from all threads
- high latency
- lifetime exceeds thread lifetime
- **allocation:** `cudaMalloc(&dmem, size);`
- **deallocation:** `cudaFree(&dmem);`
- **transfer** (blocking): `cudaMemcpy(*dest, *src, size, transfer_type);`
	- the `transfer_type` here depends on what are we doing:
		- `cudaMemcpyHostToDevice`, `cudaMemcpyDeviceToHost`

##### Shared memory
- on-chip memory
- lifetime is same as thread block lifetime
- access costs is (in the best case) equal to register access
- can be around \(48 kB\)
- organized into \(n\) **banks:**
	- typically 16-32 banks with \(32b\) width
	- parallel access if no conflict (conflict results in serialization)

##### Registers
- are at thread level
- depend on run-time configuration
- max. 255 registers/thread
- we can't really specify what will become a register

##### Host memory
- **pinned** (i.e. can't be paged out by the system)
	- can be faster if we're doing a lot of computation on it
- **pageable** (unpinned)

#### Variable declaration

| Prefix         | Location                        | Access from | Lifetime     |
| ---            | ---                             | ---         | ---          |
| `__device__`   | global memory (device memory)   | device/host | program      |
| `__constant__` | constant memory (device memory) | device/host | program      |
| `__shared__`   | shared memory                   | device      | thread block |

#### Function declaration

| Prefix       | Executed on   | Callable from |
| ---          | ---           | ---           |
| `__device__` | device        | device        |
| `__global__` | device        | host          |
| `__host__`   | host          | host          |

- `__global__` defines a kernel, return type is `void`
- `__host__` is optional (implicit)
- `__host__` and `__device__` can be combined
- for functions executed on the GPU:
	- no recursion
	- only static variable declarations
	- no variable parameter count

#### Coalescing
Combining fine-grain access by multiple threads **into a single operation.**

The following two diagrams show data access bandwidths for two main types of access patterns:

{: .no-invert}
![Offset and stride access graph.](/assets/gpu-computing/offset-stride-access.webp)

- for shared memory, concurrent access by different threads is handled by the **memory banks**
	- for our cluster, there were \(32\), where successive \(4B\) mapped to successive banks (mod \(32\)), which made the stride pattern look like this:

{: .no-invert}
![Stride access for Shared memory graph.](/assets/gpu-computing/stride-shared-access.webp)

### Thread scheduling
- up to 1k threads per block
	- one block executes on one SM
- divided into **warps of 32 threads**
	- a scheduling unit of GPU
	- implementation decision, not CUDA
	- _example:_ 4 blocks being executed on one SM, each block 1k threads, 128 thread warps

The **scheduler** will act in the following way:
1. select one thread block to execute, allocate resources as required
2. select one of its warps (32 for block of size 1024), fetch its instruction and execute
3. repeat (for this warp) until all instructions are utilized
4. upon stalling, select another warp
5. deallocate resources after all warps have finished

This is called **fine-grained multi-threading** (FGMT)
- switch context when a long operation (like memory access) occurs
	- the context switch is very fast (as opposed to the CPU)
- **all threads in a warp execute the same instruction** (on their own data and registers)

![Fine-grained multi-threading example.](/assets/gpu-computing/fgmt.svg)

- _example:_ each memory access blocks execution for \(50\) cycles and occurs every \(20\) cycles: how many warps do we need to keep the GPU occupied?
	- answer is \(4\) (as one thread waits, we can execute and stall \(3\) more)

If the threads in a warp want to do something different, a **write mask** is used -- all of them still execute the same instruction, but only the result of those with the mask are written to the memory:

```cuda
__global__ badKernel (...)
{
	id = threadIdx.x;

	// not a great idea, use < instead!
	if ( id % 32 == 0 )
		out = complex_function_call();
	else
		out = 0;
}
```

### Optimizing Matrix Multiplication


#### Naive (CPU)
- nothing too interesting, just three loops
- can be further improved by changing the order we loop for better cache hits

```cuda
void MM_NAIVE (float* M, float* N, float* P, int Width)
{
	for (int i = 0; i < Width; ++i)
	{
		for (int j = 0; j < Width; ++j)
		{
			float sum = 0;
			for (int k = 0; k < Width; ++k)
			{
				float a = M[i * width + k];
				float b = N[k * width + j];
				sum += a * b;
			}
			P[i * Width + j] = sum;
		}
	}
}
```

#### Naive (GPU)
- looping handled by a 2D thread array (single block)
- per loop, we do 2 FLOPS and 4 memory accesses

```cuda
__global__ void MM_INIT (float* Md, float* Nd, float* Pd, int Width)
{
	float Pvalue = 0;
	float Melement, Nelement;

	for (int k = 0; k < Width; ++k)
	{
		Melement = Md[threadIdx.y * Width + k];
		Nelement = Nd[k * Width + threadIdx.x];
		Pvalue += Melement * Nelement;
	}

	Pd[threadIdx.y * Width + threadIdx.x] = Pvalue;
}
```

#### Multiple thread blocks (GPU)
- we can split the matrix by thread blocks so each thread block has a part of the array

```cuda
__global__ void MM_MTB (float* Md, float* Nd, float* Pd, int Width)
{
	float Pvalue = 0;
	float Melement, Nelement;

	// Calculate the row index of the Pd element
	int row = blockIdx.y * blockDim.y + threadIdx.y;
	// Calculate the column index of the Pd element
	int col = blockIdx.x * blockDim.x + threadIdx.x;

	for (int k = 0; k < Width; ++k)
	{
		Melement = Md[row * Width + k];
		Nelement = Nd[k * Width + col];
		Pvalue += Melement * Nelement;
	}

	Pd[row * Width + col] = Pvalue;
}
```

#### Using shared memory (GPU)
- we can utilize shared memory to greatly improve the FLOP/global memory access ratio
	- one FLOP here is a floating point operation
- **main trick:** copy the part of the matrix from global memory to shared memory!

```cuda
__global__ void MM_SM (float* Md, float* Nd, float* Pd, int Width)
{
	__shared__ float Mds [TILEWIDTH] [TILEWIDTH];
	__shared__ float Nds [TILEWIDTH] [TILEWIDTH];
	int bx = blockIdx.x; int by = blockIdx.y;
	int tx = threadIdx.x; int ty = threadIdx.y;
	int row = by * TILEWIDTH + ty;
	int col = bx * TILEWIDTH + tx;
	float Pvalue = 0
	
	if (Row > Width || Col > Width)
		return;

	// loop over tiles
	for (int m = 0; m < Width / TILEWIDTH; ++m)
	{
		// threads collectively load the part of the matrix to shared memory
		Mds [ty] [tx] = Md [ row * Width + ( m * TILEWIDTH + tx ) ];
		Nds [ty] [tx] = Nd [ col + ( m * TILEWIDTH + ty ) * Width ];
		
		// RAW dependency:
		// we must wait for all of them to finish!
		__syncthreads();
		
		for (int k = 0; k < TILEWIDTH; ++k)
			Pvalue += Mds[ty][k] * Nds[k][tx];
			
		// WAR dependency:
		// again wait or some threads will change Mds/Nds
		__syncthreads ();
	}
	Pd[row * Width + col] = Pvalue;
}
```

- the `__syncthreads();` calls synchronize all threads within a single block; solves dependencies:
	- RAW (true/data dependency): _don't read before you finish writing_
	- WAR (anti-dependency): _don't write before you finish reading_
	- WAW (output dependency): _if the last write is important, make sure it's the last_

### Parallelism
- **sequential program**
	- single thread of control
	- instructions executed sequentially
- **concurrent program**
	- several autonomous sequential threads
	- parallel execution possible
	- execution determined by implementation
	- **is not parallelism** -- we can implement concurrency by interleaving on a single CPU, it just indicates that the threads are independent

Various levels of parallelism:
- **Instruction Level Parallelism (ILP)** -- parallelism of one instruction stream
	- huge amount of dependencies and branches
	- limited parallelism
- **Thread Level Parallelism (TLP)** -- parallelism of multiple independent instruction streams
	- less amount of dependencies, no limitations due to branches
	- limited by the maximum number of concurrently executable streams
- **Data Level Parallelism (DLP)** -- applying one operation on multiple independent elements
	- parallelism depends on data structure
	- vectorization techniques (single instruction processing multiple values)
- **Request Level Parallelism (RLP)** -- datacenter and customers

_The lecture goes into theoretical parallel algorithm design._

#### Synchronization

{% math ENdefinition "synchronization" %}enforcement of a defined logical order between events. This establishes a defined time-relation between distinct places, thus defining their behavior in time.{% endmath %}
- SIMD (warps on GPU): one instruction, no synchronization necessary
- MIMD: synchronization necessary (shared variables, process synchronization, etc.)

### Profiling
{% math ENdefinition: "arithmetic density" %} \(r\) is the ration between floating point operations to data movements, i.e. \[r = \frac{\mathrm{FLOPs}}{\mathrm{Byte}}\]{% endmath %}

To evaluate a performance, we use the **roofline model:**
- the performance is limited by its weakest link -- either **memory-bound** or **compute-bound**
- obviously **depends on the hardware** (memory-bound program can become compute-bound when ran on a different machine)
- by optimizing performance, the line can be stretched in both directions

{: .no-invert}
![Roofline model illustration.](/assets/gpu-computing/roofline.webp)

_The lecture goes into CUDA profiling and I'm not writing that, feel free to watch the lecture._

### Scheduling optimizations
- common and important data parallel primitive (sum, histogram, etc.)
- easy to implement but hard to implement fast
- to process very large arrays, we will require more than one CTA -- synchronization problem
	- solution: _one reduction layer will be one kernel launch_
	- _the examples don't actually do this, but in practice this would be done_
- we're **assuming associativity** (so we can do shenaningans with the order of operations)

#### Naive implementation
- we're implementing a reduction **add**
- one kernel launch will **solve a reduction subtree of its block size**

```cuda
__global__ void Reduction(int *out, int *in, size_t N)
{
	extern __shared__ int sPartials[];
	const int tid = threadIdx.x;
	unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;

	// each thread loads one element from global to shared mem
	sPartials[tid] = in[i];
	__syncthreads();
	
	// do reduction in shared mem
	for (unsigned int s = 1; s < blockDim.x; s *= 2) {
		if (tid % ( 2 * s ) == 0) {
			sPartials[tid] += sPartials[tid + s];
		}
		__syncthreads();
	}

	if (tid == 0) {
		out[blockIdx.x] = sPartials[0];
	}
 }
```

{: .no-invert}
![Reduction: naive implementation diagram.](/assets/gpu-computing/reduction-naive.webp)

#### Interleaved address divergent
- remember that **all threads in a warp execute the same instructions**
- the previous code uses threads from all over the place -- **let's use the ones from the start**
- improves performance by almost \(50\%\)!

```cuda
for (unsigned int s = 1; s < blockDim.x; s *= 2) {
	int index = 2 * s * tid;
	if (index < blockDim.x) {
		sPartials[index] += sPartials[index + s];
	}
	__syncthreads();
}
```

{: .no-invert}
![Reduction: interleaved address divergent diagram.](/assets/gpu-computing/reduction-addresses.webp)

#### Resolving bank conflicts
- **consecutive threads should access consecutive memory addresses** (see memory bank stride access graph from a few sections ago)
- another large performance increase

```cuda
for (unsigned int s = blockDim.x / 2; s > 0; s >>= 1) {
	if (tid < 0) {
		sPartials[tid] += sPartials[tid + s];
	}
	__syncthreads();
}
```

{: .no-invert}
![Reduction: resolving bank conflicts diagram.](/assets/gpu-computing/reduction-bank.webp)

#### Making use of idle threads
- after the first iteration, **half of the blocks don't do anything** (they just load something to shared memory and are done)
- start with half of the blocks and **do the first operation while loading**
- almost double performance increase again!

```cuda
unsigned int i = blockIdx.x * (blockDim.x * 2) + threadIdx.x;

// each thread loads one element from global to shared mem
sPartials[tid] = in[i] + in[i + blockDim.x];
__syncthreads();
```

#### Manual unrolling
- when we have one warp left, we don't need any `__syncthreads()` calls
- a bit ugly but functional and further increases the speed

```cuda
for (unsigned int s = blockDim.x / 2; s > 32; s >>= 1) {
	if (tid < 0) {
		sPartials[tid] += sPartials[tid + s];
	}
	__syncthreads();
}

if (tid < 32 && blockDim.x >= 64) sPartials[tid] == sPartials[tid + 32];
if (tid < 16 && blockDim.x >= 32) sPartials[tid] == sPartials[tid + 16];
if (tid <  8 && blockDim.x >= 16) sPartials[tid] == sPartials[tid +  8];
if (tid <  4 && blockDim.x >=  8) sPartials[tid] == sPartials[tid +  4];
if (tid <  2 && blockDim.x >=  4) sPartials[tid] == sPartials[tid +  2];
if (tid <  1 && blockDim.x >=  2) sPartials[tid] == sPartials[tid +  1];
```

#### Overview

Here is an overview of the versions we have implemented so far (the values in the table are GB/s for the given version and TPB):

| Version \ TPB | \(32\)    | \(64\)    | \(128\)            | \(256\)   | \(512\)   | \(1024\)  |
| ---           | --:       | --:       | --:                | --:       | --:       | --:       |
| naive         | \(7.39\)  | \(12.57\) | \(\mathbf{16.77}\) | \(14.67\) | \(12.33\) | \(9.05\)  |
| addresses     | \(10.46\) | \(18.33\) | \(\mathbf{23.88}\) | \(18.96\) | \(14.5\)  | \(10.02\) |
| banks         | \(11.05\) | \(19.54\) | \(\mathbf{30.83}\) | \(27.51\) | \(23.67\) | \(17.99\) |
| first add     | \(21.68\) | \(37.15\) | \(\mathbf{58.03}\) | \(51.31\) | \(43.75\) | \(33.66\) |
| unrolling     | \(22.59\) | \(36.91\) | \(\mathbf{68.38}\) | \(62.35\) | \(53.06\) | \(43.78\) |

### \(n\)-body optimization
- we have \(n\) bodies and want to evaluete their movement
- uses Newton's second law of motion
- movement is approximated by temporal discretization (i.e. move by some small time)

_I'm not writing the formulas from the slides, this isn't a physics course._

#### AOS vs SOA
- AOS:  **Arrays of Structures**
	- data grouped per element _index,_ different element types next to each other
	- typical in most applications
	- _consecutive threads won't access consecutive places in memory_

```cuda
// AOS
struct {
	float x, y, z;
	float vx, vy, vz;
	float mass;
} p_t;

p_t particles [MAX_SIZE];
```

- SOA: **Structures of Arrays**
	- data grouped per element _type,_ elements distributed among different arrays
	- typical in GPU applications (where multiple threads are accessing memory concurrently)

```cuda
struct {
	float x    [MAX_SIZE],
	      y    [MAX_SIZE],
	      z    [MAX_SIZE];
	float vx   [MAX_SIZE],
	      vy   [MAX_SIZE],
	      vz   [MAX_SIZE];
	float mass [max_size];
} p_t;

p_t particles;
```

#### Naive implementation
- _single thread_ takes care of a _single body_
- we don't want to recalculate force between \(a, b\) and \(b, a\) -- reuse the data!
	- one thread per force could also be explored

```cuda
__host__ __device__ void bodyBodyInteraction(...)
{
	float dx = x1 - x0;
	float dy = y1 - y0;
	float dz = z1 - z0;

	float distSqr = dx*dx + dy*dy + dz*dz;
	distSqr += softeningSquared;

	float invDist = rsqrtf(distSqr);

	float invDistCube = invDist * invDist * invDist;
	float s = mass1 * invDistCube;

	*fx = dx * s;
	*fy = dy * s;
	*fz = dz * s;
}


__global__ void ComputeNBodyGravitation_Naive(...)
{
	for (int i = blockIdx.x * blockDim.x + threadIdx.x;
	     i < N;
	     i += blockDim.x * gridDim.x)
	{
		float acc[3] = {0};
		float4 me = ((float4 *) posMass)[i];
		float myX = me.x; float myY = me.y; float myZ = me.z;

		// also includes interaction between itself
		// is essentially zero and prevents needless branching
#pragma unroll 16
		for (int j = 0; j < N; j++) {
			float4 body = ((float4 *) posMass)[j];
			float fx, fy, fz;

			bodyBodyInteraction(
				&fx, &fy, &fz,
				myX, myY, myZ,
				body.x, body.y, body.z, body.w,
				softeningSquared
			);

			acc[0] += fx; acc[1] += fy; acc[2] += fz;
		}

		force[3*i+0] = acc[0];
		force[3*i+1] = acc[1];
		force[3*i+2] = acc[2];
	}
}
```

- `#pragma unroll` will reduce branch overhead
	- the factor has to be determined imperically
	- _be careful_ -- if \(N\) isn't a multiple, might not do some calculations/segfault

#### Shared memory
- tile into sub matrices that are loaded in to the shared memory
	- after \(p = \text{block size}\) steps, reload shared memory
- each thread still computes \(N\) interactions for one body

```cuda
__global__ void ComputeNBodyGravitation_Shared (...) {
	extern __shared__ float4 sharedPM[];
	for (int i = blockIdx.x * blockDim.x + threadIdx.x;
	     i < N;
	     i += blockDim.x * gridDim.x)
	{
		float acc[3] = {0};
		float4 myPM = ((float4 *) posMass)[i];
#pragma unroll 32
		for (int j = 0; j < N; j += blockDim.x) {
			// each thread loads its part
			sharedPM[threadIdx.x] = ((float4 *) posMass)[j+threadIdx.x];
			__syncthreads();

			for (size_t k = 0; k < blockDim.x; k++) {
				float fx, fy, fz;
				float4 otherMP = sharedPM[k];

				bodyBodyInteraction(
					&fx, &fy, &fz,
					myPM.x, myPM.y, myPM.z,
					otherMP.x, otherMP.y, otherMP.z, otherMP.w,
					softeningSquared
				);

				acc[0] += fx; acc[1] += fy; acc[2] += fz;
			}
			__syncthreads();
		}
		force[3*i+0] = acc[0]; force[3*i+1] = acc[1]; force[3*i+2] = acc[2];
	}
}
```
