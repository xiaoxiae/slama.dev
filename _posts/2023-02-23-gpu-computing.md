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
6. TODO [[slides](/assets/gpu-computing/06.pdf)]
7. TODO [[slides](/assets/gpu-computing/07.pdf)]
8. TODO [[slides](/assets/gpu-computing/08.pdf)]
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
- each thread has a unique `threadIdx.{x,y,z}`
- each block has `blockIdx.{x,y,z}` (and `blockDim.{x,y,z}` for size)
	- will be assigned to **one streaming multiprocessor** (i.e. will have shared memory)
- we have to make sure that the GPU has enough SMs and threads/block to start!

{: .no-invert}
![Thread and memory diagram for CUDA.](/assets/gpu-computing/grid-block-thread.png)

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
- combining fine-grain access by multiple threads into a single operation
- should match a multiple of L1/L2 cache sizes!

The following two diagrams show data access bandwidths for two main types of access patterns:

{: .no-invert}
![Offset and stride access graph.](/assets/gpu-computing/offset-stride-access.png)

- for shared memory, this is handled by the **memory banks**
	- for our cluster, there were \(32\), where successive \(4B\) mapped to successive banks (mod \(32\)), which made the stride pattern look like this:

{: .no-invert}
![Stride access for Shared memory graph.](/assets/gpu-computing/stride-shared-access.png)

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
- all threads in a warp execute the same instruction

![Fine-grained multi-threading example.](/assets/gpu-computing/fgmt.svg)

- _example:_ each memory access blocks execution for \(50\) cycles and occurs every \(20\) cycles: how many warps do we need to keep the GPU occupied?
	- answer is \(4\) (as one thread waits, we can execute and stall \(3\) more)

If the threads in a warp want to do something different, a **write-mask** is used -- all of them still execute the same instruction, but only the result of those with the mask are written to the memory:

```cuda
__global__ badKernel (...)
{
	id = threadIdx.x;

	// not a great idea, do < instead!
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

#### Initial (GPU)
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
- we can utilize shared memory to greatly improve the FLOPS/global memory access ratio
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
		__syncthreads();  // we must wait for all of them to finish!
		
		for (int k = 0; k < TILEWIDTH; ++k)
			Pvalue += Mds[ty][k] * Nds[k][tx];
		__syncthreads ();  // again wait or some threads will change Mds/Nds
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

#### Synchronization

{% math ENdefinition "synchronization" %}enforcement of a defined logical order between events. This establishes a defined time-relation between distinct places, thus defining their behavior in time.{% endmath %}
- SIMD (warps on GPU): one instruction, no synchronization necessary
- MIMD: synchronization necessary (shared variables, process synchronization, etc.)
