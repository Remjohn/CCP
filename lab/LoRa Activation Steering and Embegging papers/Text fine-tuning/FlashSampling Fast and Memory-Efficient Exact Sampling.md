# **FlashSampling: Fast and Memory-Efficient** **Exact Sampling**

**Tomas** **Ruiz** [1∗] **Zhen** **Qin** [3∗] **Yifan** **Zhang** [2†] **Xuyang** **Shen** [3]

**Yiran** **Zhong** [3] **Mengdi** **Wang** [2] _[†]_

1LMU Munich 2Princeton University 3FlashSampling


February 28, 2026 [‡]


**Abstract**


Sampling from a categorical distribution is mathematically simple, but in large-vocabulary
decoding, it often triggers extra memory traffic and extra kernels after the LM head. We
present **FlashSampling**, an exact sampling primitive that fuses sampling into the LM-head
matmul and never materializes the logits tensor in HBM. The method is simple: compute logits
tile-by-tile on chip, add Gumbel noise, keep only one maximizer per row and per vocabulary
tile, and finish with a small reduction over tiles. The fused tiled kernel is exact because argmax
decomposes over a partition; grouped variants for online and tensor-parallel settings are exact
by hierarchical factorization of the categorical distribution. Across H100, H200, B200, and
B300 GPUs, FlashSampling speeds up kernel-level decode workloads, and in end-to-end vLLM
experiments, it reduces time per output token by up to 19% on the models we test. These results
show that exact sampling, with no approximation, can be integrated into the matmul itself,
turning a bandwidth-bound postprocessing step into a lightweight epilogue.


`Project` `Page` : `[https://github.com/FlashSampling/FlashSampling](https://github.com/FlashSampling/FlashSampling)`

### **1 Introduction**


Sampling from a categorical distribution is a small mathematical operation, but in large-categorical
systems, it can become an expensive inner-loop primitive. Modern LLM serving stacks invoke
sampling repeatedly during autoregressive decoding, often on outputs with tens or hundreds of
thousands of categories (Kwon et al., 2023; Ye et al., 2025; Maddison et al., 2014; Huijben et al.,
2022). Recent measurements confirm the cost: sampling can account for over 10% of token generation
time even on a single GPU (Key et al., 2024), and 20–38% in tensor-parallel settings where logits
must be gathered across ranks (Zhao et al., 2025). The bottleneck is usually not arithmetic, but the
chain of separate kernels that materialize, normalize, and scan the logits tensor.
At decode time, the LM-head projection already streams a large [ _V, D_ ] weight matrix from HBM.
When the active batch is small, this projection is typically memory-bandwidth bound. Materializing
the resulting [ _B, V_ ] logits tensor, launching extra kernels to normalize and sample from it, and
then discarding it adds extra memory traffic and synchronization but no useful model computation.


∗Equal contribution; _†_ Corresponding authors. _‡_ Revised: March 16, 2026.


1


In this regime, the separate sampler is pure overhead (Dao et al., 2022; Wijmans et al., 2025).
Throughout, _B_ denotes batch size and _V_ denotes the number of categories, such as vocabulary size.



**Multinomial Sampling**



**FlashSampling**

























**Figure** **1** Conventional multinomial sampling (left) materializes the full [ _B, V_ ] logits tensor in HBM between
the matmul and the sampler. FlashSampling (right) fuses sampling into the matmul epilogue, followed by a
lightweight reduction over vocabulary tiles. Logits are computed tile-by-tile in on-chip memory, perturbed
with Gumbel noise, and reduced without ever writing the full logits tensor to HBM. Red arrows denote HBM
traffic; green arrows denote on-chip data movement.


Standard pipelines write logits to HBM and read them back for sampling, even though logits are
immediately discarded after one sample is drawn. Exact sampling is often described as “compute
softmax, then sample”, which obscures the fact that exact sampling does not require forming
probabilities at all. For large vocabularies, streaming and tensor-parallel settings turn sampling into
a memory and communication problem if full logits must be materialized or gathered.
In this work, we introduce FlashSampling, which computes logits tile-by-tile on chip and writes
only one candidate per row and per vocabulary tile, followed by a lightweight reduction. Exact
sampling needs only the index of the largest perturbed logit, so there is no need to form a softmax,
a prefix sum, or normalized probabilities; the method introduces no approximation. A simple
hierarchical factorization yields exact online and distributed variants that keep only small summaries


2


in flight and communicate only small summaries across ranks.
Our contributions can be summarized as follows:
1. **FlashSampling,** **a** **simple** **fused** **exact** **sampler.** We introduce a two-stage design that computes
logits tile-by-tile in the LM-head epilogue, adds Gumbel noise on chip, and stores only one
candidate per row and per vocabulary tile instead of materializing the full [ _B, V_ ] logits tensor.


2. **A** **clean** **exactness** **argument.** We separate the two ingredients used in the paper: the fused tiled
kernel is exact pathwise by argmax decomposition over vocabulary tiles, while grouped, online,
and distributed variants are exact in distribution by hierarchical factorization through group
log-masses.


3. **A** **systems** **analysis** **and** **evaluation.** We show why raw logits-byte savings alone are too small to
explain the measured speedups, and we demonstrate consistent gains in the memory-bandwidthbound decode regime across four NVIDIA GPUs and in end-to-end vLLM evaluation.

### **2 Background**


**Notation.** Let [ _V_ ] := _{_ 1 _, . . ., V }_ . Let _**ℓ**_ _∈_ (R _∪{−∞}_ ) _[V]_ denote _transformed_ _logits_ after any

[�]
deterministic operations such as additive bias, temperature scaling, or masking. We assume that
each row has at least one finite entry; otherwise, the target categorical distribution is undefined.
The target distribution is

exp( _ℓ_ [�] _i_ )
_p_ ( _i_ ) = _._

           - _V_
_j_ =1 [exp(] _[ℓ]_ [�] _[j]_ [)]


Raw logits _**ℓ**_ are the special case _**ℓ**_ [�] = _**ℓ**_ . We denote i.i.d. standard Gumbel variables by _gi_ _∼_
Gumbel(0 _,_ 1). Because the Gumbel law is continuous, ties occur with probability zero, so argmax is
unique almost surely.


**2.1** **Why** **Sampling** **Is** **Expensive** **at** **Scale**


A common materialized-logits pipeline first computes transformed logits, then forms probabilities,
and finally samples from those probabilities. One representative example is softmax followed by
prefix-sum sampling:


GEMM(produce logits) _→_ write logits to HBM _→_ read logits for sampling _._


Algorithm 1 summarizes this pattern.
Not every implementation uses exactly these kernels, but any materialized-logits baseline pays
the same structural costs: at least one logits write, at least one logits reread, and extra sampling
work after the GEMM.


**Decode** **regime.** In autoregressive decoding, _B_ is typically small. The LM-head projection is then
often memory-bandwidth bound because it repeatedly streams the large [ _V, D_ ] weight matrix from
HBM. Materializing [ _B, V_ ] logits and reading them back for sampling adds multiple avoidable HBM
round-trips in the most latency-sensitive part of the decode loop (Kwon et al., 2023; Ye et al., 2025).


3


**Algorithm** **1** One common materialized-logits sampling pipeline

**Require:** Hidden state _**h**_ _∈_ R _[D]_, LM-head weights _**W**_ _∈_ R _[V][ ×][D]_, optional deterministic transforms
**Ensure:** Sampled index _i_ _[⋆]_ _∈{_ 1 _, . . ., V }_

1: _**ℓ**_ _←_ _**W h**_ _▷_ GEMM: compute logits and write to HBM



2: _**ℓ**_ _←_ transform( _**ℓ**_ ) _▷_ temperature, bias, mask; read/write HBM

[�]

3: _m ←_ max _i_ _ℓ_ [�] _i_ _▷_ pass 1 over transformed logits

4: _Z_ _←_ [�] _[V]_ _i_ =1 [exp(] _[ℓ]_ [�] _[i][ −]_ _[m]_ [)] _▷_ pass 2 over transformed logits

5: _pi_ _←_ exp( _ℓ_ [�] _i −_ _m_ ) _/Z_ for all _i_ _▷_ write probabilities

6: _ci_ _←_ [�] _[i]_ _j_ =1 _[p][j]_ [for] [all] _[i]_ _▷_ prefix sum

7: Draw _u ∼_ Unif(0 _,_ 1)



8: _i_ _[⋆]_ _←_ min _{i_ : _ci_ _≥_ _u}_ _▷_ search

9: **return** _i_ _[⋆]_


**2.2** **GPU** **Memory** **Hierarchy**


Table 1 summarizes the GPU memory hierarchy. On-chip memory (registers, SRAM) is orders of
magnitude faster than HBM but far smaller. FlashSampling exploits this gap by keeping logits in
registers/SRAM and never writing the full logits tensor to HBM.


**Table** **1** GPU memory hierarchy (H100 SXM) (NVIDIA, 2022, 2024).


**Level** **Capacity** **Bandwidth**


Registers/SRAM 256 KB / SM _>_ 100 TB/s
L2 cache 50 MB _∼_ 12 TB/s
HBM3 80 GB 3.35 TB/s


**2.3** **The** **Gumbel-Max** **Trick**


The classical Gumbel-Max trick states that exact categorical sampling can be performed by adding
i.i.d. Gumbel noise and taking an argmax:


**Theorem** **2.1** (Gumbel-Max) **.** Let _**ℓ**_ [�] _∈_ (R _∪{−∞}_ ) _[V]_ have at least one finite entry, and let _{gi}_ _[V]_ _i_ =1
be i.i.d. Gumbel(0 _,_ 1). Then



_i_ _[⋆]_ = argmax
_i∈_ [ _V_ ]




- - _e_ [�] _[ℓ][i]_
_ℓ_ - _i_ + _gi_ = _⇒_ P( _i_ _[⋆]_ = _i_ ) =

       - _V_ _[.]_
_j_ =1 _[e]_ [�] _[ℓ][j]_



This classical result goes back to Gumbel (1954) and is widely used in machine learning (Maddison
et al., 2014; Huijben et al., 2022). The trick extends to sampling without replacement via the
Gumbel-Top- _k_ method (Kool et al., 2019). The key point for this paper is simple: _exact_ _sampling_
_does_ _not_ _require_ _an_ _explicit_ _softmax_ . It only requires the index of the largest perturbed logit.


4


### **3 FlashSampling**

We now describe FlashSampling from simplest to most practical form. The core algorithm is
intentionally simple and introduces no approximation: maintain the largest perturbed score seen so
far and its index.


**3.1** **Exact** **Sampling** **via** **Online** **Gumbel-Max**


Given transformed logits _**ℓ**_ _∈_ (R _∪{−∞}_ ) _[V]_, exact sampling from Cat(softmax( _**ℓ**_ [�] )) is:

[�]



_i_ _[⋆]_ = argmax
_i∈_ [ _V_ ]




- _ℓ_ - _i_ + _gi_ _,_ _gi_ _∼_ Gumbel(0 _,_ 1) i.i.d.



**Algorithm.** Generate i.i.d. Gumbels, compute _si_ = _ℓ_ [�] _i_ + _gi_, and return _i_ _[⋆]_ = argmax _i si_ . The
computation can be performed online in a single pass that maintains only the current best score
and its index, analogous to the online normalizer calculation for softmax (Milakov and Gimelshein,
2018). No softmax, no normalization constant, and no prefix sum are required (see Algorithm B.1
in the Appendix).


**Systems** **implication.** Sampling reduces to a single reduction over perturbed logits. This naturally
fits GPU reductions and removes the extra normalization and prefix-sum work used by common
softmax-based pipelines.


**Simplicity.** The online algorithm keeps only two running state variables per row: the current
best perturbed score and the corresponding index. This simplicity is what makes fusion with the
LM-head epilogue practical.


**GPU** **parallelization.** Each threadblock can process one contiguous vocabulary chunk, or _vocabulary_
_tile_ . The block computes perturbed scores for that chunk, keeps only the tile-local maximizer, and a
small second-stage reduction selects the global maximizer across vocabulary tiles.


**3.2** **FlashSampling** **for** **LM-Head** **Sampling**


We now consider the common case where logits are produced by GEMM:


_**Y**_ = _**HW**_ _[⊤]_ _∈_ R _[B][×][V]_ _,_


where _**H**_ _∈_ R _[B][×][D]_ are hidden states and _**W**_ _∈_ R _[V][ ×][D]_ are LM-head weights. We wish to sample one
index per row from Cat(softmax( _**Y**_ _b,_ :)), possibly after deterministic transforms such as temperature
scaling, additive bias, or masking.


**Goal:** **avoid** **materializing** _**Y**_ **.** FlashSampling performs sampling inside the matmul kernel and
writes only one candidate per row and per vocabulary tile, never the full [ _B, V_ ] logits tensor:

- **Stage** **1** **(fused** **kernel):** compute one batch tile and one vocabulary tile on chip, apply deterministic transforms, add Gumbel noise, and keep the tile-local maximizer for each row.


- **Stage** **2** **(reduction):** reduce over vocabulary-tile candidates to obtain one global sample per
row.


5


**Algorithm** **2** FlashSampling fused matmul-sample (two-stage): one candidate per row and per
vocabulary tile, followed by reduction

**Require:** Hidden states _**H**_ _∈_ R _[B][×][D]_, LM-head weights _**W**_ _∈_ R _[V][ ×][D]_, temperature _τ_ _>_ 0, optional
mask/bias, RNG key
**Ensure:** Samples _**i**_ _[⋆]_ _∈{_ 1 _, . . ., V }_ _[B]_

**Stage** **1** **(fused** **kernel):** for each batch tile _B_ and vocabulary tile _Tt_ in parallel

1: Initialize accumulator _**A**_ [(] _[t]_ [)] _∈_ R _[|B|×|T][t][|]_ _←_ 0

2: **for** _d_ 0 = 1 _,_ 1 + _K_ tile _, . . ., D_ **do**

3: Load _**H**_ _B, d_ 0: _d_ 0+ _K_ tile _−_ 1 and _**W**_ _Tt, d_ 0: _d_ 0+ _K_ tile _−_ 1 into on-chip memory

4: _**A**_ [(] _[t]_ [)] _←_ _**A**_ [(] _[t]_ [)] + _**H**_ _B, d_ 0: _d_ 0+ _K_ tile _−_ 1� _**W**_ _Tt, d_ 0: _d_ 0+ _K_ tile _−_ 1� _⊤_

5: **end** **for**

6: **for** each output element ( _b, i_ ) _∈B × Tt_ **do**

          -          7: _y_  - _b,i_ _←_ transform _A_ [(] _b,i_ _[t]_ [)] _▷_ temperature, bias, mask

8: Draw _ub,i_ _∈_ (0 _,_ 1) and set _gb,i_ _←−_ log� _−_ log _ub,i_  
9: _sb,i_ _←_ _y_  - _b,i_ + _gb,i_
10: **end** **for**

11: **for** each row _b ∈B_ **do**

12: ( _m_ [(] _b_ _[t]_ [)] _[, j]_ _b_ [(] _[t]_ [)][)] _[ ←]_ [argmax] _i∈Tt_ _[s][b,i]_

13: idx [(] _b_ _[t]_ [)] _←_ global vocabulary index corresponding to _jb_ [(] _[t]_ [)]
14: Write ( _m_ [(] _b_ _[t]_ [)] _[,]_ [ idx] _b_ [(] _[t]_ [)][)] [to] [HBM]

15: **end** **for**


**Stage** **2** **(reduction):** for each row _b_

16: _t_ _[⋆]_ _←_ argmax _t m_ [(] _b_ _[t]_ [)]
17: _i_ _[⋆]_ _b_ _[←]_ [idx] _b_ [(] _[t][⋆]_ [)]
18: **return** _**i**_ _[⋆]_


**Why** **the** **two-stage** **design** **is** **simple.** The fused stage does all expensive work in the matmul
epilogue. The second stage is only an argmax over a small candidate buffer of shape roughly

[ _B,_ #vocab tiles]. This design is easy to implement and already captures most of the benefit in the
decode regime.


**Why** **this** **avoids** **softmax.** The algorithm never forms probabilities and never computes an explicit
softmax. Exactness follows because it computes the same maximizer of the perturbed logits that a
full Gumbel-Max pass would compute.


**Tensor-parallel** **fusion.** When the vocabulary is sharded across ranks, each rank can run the fused
kernel on its local shard and return only small summaries rather than all local logits. In the grouped
formulation below, these summaries are a local sample and a local log-mass. No _O_ ( _V_ ) all-gather of
logits is required.


**RNG** **determinism.** For reproducibility, RNG streams are indexed by the logical output position
( _b, i_ ) using a counter-based RNG (e.g. Philox), so each random number is a deterministic function


6


of a key and a counter. Uniform variates are mapped to the open interval (0 _,_ 1) to avoid infinities in
the Gumbel transform _g_ = _−_ log( _−_ log _u_ ).


**Numerical** **precision.** GEMM accumulation and perturbed scores are computed in FP32 for
stability, even when inputs are FP16 or BF16. Gumbel noise is likewise generated in FP32 to avoid
numerical error in the logarithms. The overhead is minor compared with the GEMM itself.

### **4 Theoretical Analysis of FlashSampling**


This section separates the two exactness arguments used in the paper. The fused tiled kernel is
exact _pathwise_ : once perturbed scores are formed, the global maximizer is exactly the maximizer of
the tile-local maxima. Grouped, online, and distributed variants are exact _in_ _distribution_ : they rely
on hierarchical factorization through group log-masses.


**4.1** **Group-Gumbel-Max:** **Hierarchical** **Exact** **Sampling**


Partition [ _V_ ] into _m_ disjoint groups _{Gk}_ _[m]_ _k_ =0 _[−]_ [1][;] [the] [groups] [need] [not] [have] [equal] [size.] [For] [any] [group]
with at least one finite transformed logit, define


_Lk_ = log            - exp( _ℓ_ [�] _i_ ) = logsumexp( _**ℓ**_ [�] _Gk_ ) _._

_i∈Gk_


If a group contains no finite transformed logit, then _Lk_ = _−∞_, the group has zero probability mass,
and it can be skipped.
After discarding zero-mass groups, the categorical distribution factorizes as



P( _K_ = _k_ )

- �� choose group



_∝_ exp( _Lk_ ) _,_ P( _I_ = _i | K_ = _k_ )

         - ��         choose within group



_∝_ exp( _ℓ_ [�] _i_ ) for _i ∈Gk._



Thus exact sampling from the full categorical can be implemented by first choosing a group using
the logits _{Lk}_ and then sampling within the chosen group.


**Parallel** **FlashSampling.** Suppose logits arise from a linear projection _**y**_ = _**W x**_, where _**W**_ _∈_ R _[V][ ×][D]_

and _**x**_ _∈_ R _[D]_ . Let _**W**_ _Gk_ _∈_ R _[|G][k][|×][D]_ be the block of rows indexed by group _Gk_, so _**y**_ _k_ = _**W**_ _Gk_ _**x**_ _∈_ R _[|G][k][|]_

are the group logits. Parallel FlashSampling computes groups independently: each group with
nonzero mass computes (i) an exact local sample _zk_ _∼_ Cat(softmax( _**y**_ _k_ )) and (ii) its group log-mass
_Lk_ = logsumexp( _**y**_ _k_ ). The algorithm then samples _K_ _∼_ Cat(softmax( _**L**_ )) and returns _zK_ mapped
to its global index. This is exact by direct factorization.


**Online** **FlashSampling.** When memory is the primary constraint, FlashSampling can stream groups
one at a time and maintain only a running log-mass and a running sample. Suppose the current
running state is ( _L_ run _, z_ ) and the next nonzero-mass group has log-mass _Lk_ and exact local sample
_zk_ . Define
_L_ new = log             - _eL_ run + _eLk_             - _._


Then replace _z_ by _zk_ with probability


_e_ _[L][k]_ 1

_e_ _[L]_ [run] + _e_ _[L][k]_ [=] _[ e][L][k][−][L]_ [new] [=] 1 + _e_ _[L]_ [run] _[−][L][k]_ _[,]_


7


and otherwise keep _z_ . Section 4.4 proves that this binary merge rule preserves exactness by induction.


**4.2** **Distributed** **FlashSampling** **for** **Tensor-Parallel** **Vocabularies**


In tensor-parallel LM heads, the vocabulary dimension is sharded across _n_ GPUs. Naively, each
GPU computes local logits and then an all-gather concatenates the full _V_ logits before sampling,
incurring communication proportional to the vocabulary size per row. FlashSampling treats shards
as groups: each rank returns (i) a local exact sample from its shard, if its shard has nonzero mass for
that row, and (ii) the shard log-mass _Lk_ . A final exact categorical sample over the shard log-masses
chooses which rank provides the global sample. Communication therefore scales with the number of
shards, not the number of vocabulary entries.


**4.3** **A** **Unifying** **View:** **Max-Stability** **of** **Grouped** **Gumbel** **Perturbations**


Group-Gumbel-Max and FlashSampling both rely on the same structural fact: _max_ decomposes
over partitions. For grouped variants we additionally use the max-stability of Gumbel perturbations.


**Lemma** **4.1** (Gumbel max-stability under grouping) **.** Let _{gi}_ _[V]_ _i_ =1 [be] [i.i.d.] [Gumbel][(0] _[,]_ [ 1)] [and] [let]
_{Gk}_ _[m]_ _k_ =0 _[−]_ [1] [be] [a] [partition] [of] [[] _[V]_ [ ].] [Assume] [each] [group] [under] [discussion] [contains] [at] [least] [one] [finite]
transformed logit. Define


_Mk_ = max _Ik_ = argmax( _ℓ_ [�] _i_ + _gi_ ) _,_ _Lk_ = log     - _e_ [�] _[ℓ][i]_ _._
_i∈Gk_ [(] _[ℓ]_ [�] _[i]_ [ +] _[ g][i]_ [)] _[,]_ _i∈Gk_ _i∈Gk_


Then:
1. _Mk_ _∼_ Gumbel( _Lk,_ 1),


2. _{Mk}_ are independent across disjoint groups,


3. P( _Ik_ = _i_ ) = _e_ [�] _[ℓ][i]_ _/_ [�] _j∈Gk_ _[e]_ [�] _[ℓ][j]_ [for] _[i][ ∈G][k]_ [.]


_Proof._ For any real _t_,




   P( _Mk_ _≤_ _t_ ) =




- 
P( _gi_ _≤_ _t −_ _ℓ_ [�] _i_ ) =
_i∈Gk_ _i∈G_




- exp - _−_ _e−_ ( _t−_ - _ℓi_ )� = exp - _−_ _e_ _[−]_ [(] _[t][−][L][k]_ [)][�] _,_

_i∈Gk_



which is the CDF of Gumbel( _Lk,_ 1). Independence follows because the groups are disjoint and
the underlying Gumbels are independent. The within-group argmax probabilities are exactly the
Gumbel-Max trick applied to the restricted transformed logits.


**Consequence.** For grouped variants, selecting a group by argmax _k Mk_ is equivalent in distribution
to applying Gumbel-Max directly to the group logits _{Lk}_ . The outer group sample may therefore
use fresh independent Gumbels, or it may reuse explicitly computed group maxima. For the fused
two-stage kernel in Algorithm 2, exactness does _not_ rely on max-stability: once the perturbed scores
_xi_ = _ℓ_ [�] _i_ + _gi_ have been formed, exactness is simply the deterministic identity


max _xi_ = max max
_i_ _t_ _i∈Tt_ _[x][i][.]_


8


**4.4** **Exactness** **of** **Group-Gumbel-Max**


The correctness of grouped FlashSampling rests on two facts: exact group factorization, and the
binary merge rule used by the online variant.


**Lemma** **4.2** (Exact group factorization) **.** Let [ _V_ ] be partitioned into groups _{Gk}_ _[m]_ _k_ =0 _[−]_ [1][,] [and] [discard]
any zero-mass groups. Define _Lk_ = log [�] _i∈Gk_ [exp][(] _[ℓ]_ [�] _[i]_ [).] [If] [we] [sample] _[K]_ _[∼]_ [Cat][(][softmax][(] _**[L]**_ [))] [and] [then]
sample _I_ _|_ ( _K_ = _k_ ) _∼_ Cat(softmax( _**ℓ**_ [�] _Gk_ )), the marginal distribution of _I_ equals Cat(softmax( _**ℓ**_ [�] )).


_Proof._ For any _i ∈Gk_,


_e_ _[L][k]_ _e_ [�] _[ℓ][i]_ _e_ [�] _[ℓ][i]_
P( _I_ = _i_ ) = P( _K_ = _k_ ) P( _I_ = _i | K_ = _k_ ) =

             - _s_ _[e][L][s]_ _[·]_             - _j∈Gk_ _[e]_ [�] _[ℓ][j]_ [=]             - _Vj_ =1 _[e]_ [�] _[ℓ][j]_ _[.]_



**Lemma** **4.3** (Binary merge rule) **.** Let _A, B_ _⊆_ [ _V_ ] be disjoint and suppose both have nonzero mass.
Define
_LA_ = log           - _e_ [�] _[ℓ][i]_ _,_ _LB_ = log           - _e_ [�] _[ℓ][i]_ _._




- _e_ [�] _[ℓ][i]_ _,_ _LB_ = log 
_i∈A_ _i∈B_




- _e_ [�] _[ℓ][i]_ _._


_i∈B_



Suppose _ZA_ _∼_ Cat(softmax( _**ℓ**_ [�] _A_ )), _ZB_ _∼_ Cat(softmax( _**ℓ**_ [�] _B_ )), and an independent Bernoulli choice
selects _B_ with probability _e_ _[L][B]_ _/_ ( _e_ _[L][A]_ + _e_ _[L][B]_ ). Returning _ZB_ when _B_ is selected and _ZA_ otherwise
yields an exact sample from Cat(softmax( _**ℓ**_ [�] _A∪B_ )).


_Proof._ For any _i ∈_ _A_,


_e_ _[L][A]_ _e_ [�] _[ℓ][i]_ _e_ [�] _[ℓ][i]_
P( _Z_ = _i_ ) = P(choose _A_ ) P( _ZA_ = _i_ ) =

_e_ _[L][A]_ + _e_ _[L][B]_ _[·]_                        - [=]                        - _[.]_
_j∈A_ _[e]_ [�] _[ℓ][j]_ _j∈A∪B_ _[e]_ [�] _[ℓ][j]_


The same calculation for _i ∈_ _B_ gives


_e_ _[L][B]_ _e_ [�] _[ℓ][i]_ _e_ [�] _[ℓ][i]_
P( _Z_ = _i_ ) = _e_ _[L][A]_ + _e_ _[L][B]_ _[·]_            - [=]            - _[.]_

_j∈B_ _[e]_ [�] _[ℓ][j]_ _j∈A∪B_ _[e]_ [�] _[ℓ][j]_


Hence _Z_ _∼_ Cat(softmax( _**ℓ**_ [�] _A∪B_ )).


**Theorem** **4.4** (Exactness of hierarchical FlashSampling) **.** Algorithms B.2, B.3, and B.4 return an
exact sample from Cat(softmax( _**ℓ**_ [�] )).


_Proof._ For the parallel and distributed variants, Lemma 4.2 shows that it suffices to sample the
group or shard index from logits _{Lk}_ and then sample within the chosen group; both steps are
exact.
For the online variant, initialize with an exact sample from the first nonzero-mass group. Each
subsequent update merges the current union with the next nonzero-mass group using Lemma 4.3.
An induction over the streamed groups therefore yields an exact sample from the full categorical
distribution.


9


**4.5** **Exactness** **of** **Tile-Wise** **FlashSampling** **Reduction**


FlashSampling also relies on a simpler structural lemma: the global maximum equals the maximum
of the tile-local maxima.


**Lemma** **4.5** (Max over vocabulary tiles) **.** Let _{xi}_ _[V]_ _i_ =1 [be] [real] [numbers] [and] [let] _[{T][s][}][n]_ _s_ =0 [tile] _[−]_ [1] be a
partition of [ _V_ ] into vocabulary tiles. For each tile, define


_ms_ = max _i∈Ts_ _[x][i][,]_            - _ıs_ _∈_ argmax _i∈Ts_ _xi,_


where � _ıs_ is a global index in _Ts_ . Then


max [= max] _ms._
_i∈_ [ _V_ ] _[x][i]_ _s_


Moreover, for any _s_ _[⋆]_ _∈_ argmax _s ms_, the chosen index � _ıs_ _[⋆]_ is a global maximizer. Conversely, every
global maximizer lies in some tile _s_ _[⋆]_ _∈_ argmax _s ms_ .


_Proof._ The identity for the maximum value is immediate:


max [= max] max [= max] _ms._
_i∈_ [ _V_ ] _[x][i]_ _s_ _i∈Ts_ _[x][i]_ _s_


If _s_ _[⋆]_ _∈_ argmax _s ms_, then _xıs⋆_ = _ms_ _[⋆]_ = max _i xi_, so � _ıs_ _[⋆]_ is a global maximizer. Conversely, if _i_ _[⋆]_ is any
global maximizer, then its�tile _s_ _[⋆]_ satisfies _ms_ _[⋆]_ = _xi_ _[⋆]_ = max _i xi_, hence _s_ _[⋆]_ _∈_ argmax _s ms_ .


Applying Lemma 4.5 to _xi_ = _ℓ_ [�] _i_ + _gi_ justifies the two-stage fused design in Algorithm 2. Because
the Gumbel variables are continuous, the global maximizer is unique almost surely, so the tile-wise
reduction returns exactly the same index as a full row-wise argmax with probability one.


**4.6** **Top-** _k_ **,** **Nucleus** **Sampling,** **and** **Masking**


Practical decoding often uses truncated supports, and the tiled structure of FlashSampling naturally
accommodates most of them.


- **Top-** _k_ **:** The Group-Gumbel-Max decomposition extends directly to top- _k_ via the Gumbel-Top- _k_
trick (Kool et al., 2019). Each tile computes top- _k_ candidates locally (logits and indices), and
a second stage reduces all per-tile candidates into a global top- _k_ . Sampling from the final _k_
candidates can be done with multinomial or Gumbel-Max sampling.


- **Top-** _p_ **(nucleus):** Unlike top- _k_, nucleus sampling (Holtzman et al., 2020) requires a global
softmax followed by a sorted cumulative sum, neither of which decomposes into independent
tile-local work. However, top- _p_ can be applied _after_ top- _k_ on the reduced candidate set of only
_k_ elements, where softmax, sorting, and cumulative summation are negligible. This sequential
top- _k_ -then-top- _p_ strategy is used in practice by vLLM [∗][,][†], FlashInfer [‡], and other SOTA top- _k_
top- _p_ algorithms (Park et al., 2026).


∗ `[https://github.com/vllm-project/vllm/blob/v0.16.0/vllm/v1/sample/ops/topk_topp_sampler.py#](https://github.com/vllm-project/vllm/blob/v0.16.0/vllm/v1/sample/ops/topk_topp_sampler.py#L264-L279)`
```
L264-L279
```

  - `[https://github.com/vllm-project/vllm/blob/v0.16.1rc0/vllm/v1/sample/ops/topk_topp_triton.py#](https://github.com/vllm-project/vllm/blob/v0.16.1rc0/vllm/v1/sample/ops/topk_topp_triton.py#L956)`
```
L956
```

  - `[https://github.com/flashinfer-ai/flashinfer/blob/v0.6.3/flashinfer/sampling.py#L1069-L1072](https://github.com/flashinfer-ai/flashinfer/blob/v0.6.3/flashinfer/sampling.py#L1069-L1072)`


10


- **Masking:** Forbidden indices (e.g. banned tokens, grammar constraints) are supported by setting
their logits to _−∞_ before perturbation, which preserves exactness over the restricted support.


While the FlashSampling theory allows integrating these sampling strategies, we leave the implementation to future work.


**4.7** **Cost** **Model:** **Bandwidth,** **Kernels,** **and** **Overhead**


We outline a simple model to reason about speedups.


**Materialized** **baseline** **(lower** **bound).** For a BF16 baseline that materializes logits, the GEMM
must at least read _**W**_ and _**H**_ and write _**Y**_ once; sampling must then read _**Y**_ at least once again.
An optimistic lower bound on arithmetic intensity is therefore


2 _BV D_ _BV D_
_I_ mat( _B_ ) _≈_ FLOP/byte _,_
2( _V D_ + _BD_ + 2 _BV_ ) [=] _V D_ + _BD_ + 2 _BV_


where the denominator counts mandatory BF16 traffic only. Real softmax-based samplers usually
make more than one pass over the materialized logits, so the true baseline intensity is lower.


**Fused** **matmul** **+** **sampling.** If sampling is fused into the GEMM epilogue so that the logits write
and reread are removed, then, up to lower-order terms from the small candidate buffer,


2 _BV D_ _BV_
_I_ fused( _B_ ) _≈_ FLOP/byte _._
2( _V D_ + _BD_ ) [=] _V_ + _B_


Thus fusion raises the effective arithmetic intensity.


**Incremental** **traffic** **saved** **by** **fusion.** Relative to a fused kernel, any materialized baseline incurs at
least one write and one reread of the [ _B, V_ ] logits tensor. In BF16 this minimal extra traffic is 4 _BV_
bytes. Compared with the mandatory LM-head weight read of 2 _V D_ bytes, the extra fraction is


4 _BV_ [2] _[B]_
2 _V D_ [=] _D_ _[.]_


For the small configuration ( _D_ = 4096), this ratio is 0 _._ 049% at _B_ = 1, 3 _._ 125% at _B_ = 64, and
6 _._ 25% at _B_ = 128. Thus raw logits-byte savings alone are too small to explain the largest measured
speedups. The main gains come from eliminating extra sampling kernels, global-memory round-trips
through those kernels, and their launch and synchronization overhead. In the memory-bandwidthbound decode regime, these extra kernels are pure overhead.
At _B_ = 1 on the small configuration, the minimal avoided logits round-trip is


4 _BV_ = 4 _·_ 1 _·_ 151 _,_ 936 = 607 _,_ 744 bytes _≈_ 0 _._ 608 MB _._


At 8 TB/s, this corresponds to only 7 _._ 6 _×_ 10 _[−]_ [5] ms. The observed latency gap therefore cannot be
explained by raw HBM bandwidth alone.


11


### **5 Experiments**

We evaluate FlashSampling at two levels: kernel-level microbenchmarks that isolate fused matmulplus-sample across four GPU architectures, and end-to-end vLLM integration that measures autoregressive decode latency. All benchmarks use the open-source FlashSampling Triton implementation (Ruiz, 2026).


**5.1** **Setup**


**Hardware.** Kernel microbenchmarks are run on four NVIDIA GPUs spanning two architecture
generations. Table 2 summarizes their specifications. All GPUs are provisioned via Modal cloud.


**Table 2** GPU specifications. Peak BF16 TFLOP/s are dense (without structured sparsity), since the LM-head
matmul is a dense GEMM. The ops:byte ratio (peak compute / bandwidth) contextualizes the crossover
between bandwidth- and compute-limited regimes, although the exact crossover is kernel-dependent.


**H100** **H200** **B200** **B300**


Architecture Hopper Hopper Blackwell Blackwell
HBM capacity (GB) 80 141 192 288
HBM bandwidth (TB/s) 3.35 4.8 8.0 8.0
Peak BF16 dense (TFLOP/s) 989 989 2,250 2,250
Ops:byte ratio 295 206 281 281


**Software.** PyTorch 2.10.0, CUDA 13.0, Triton 3.6, and FlashInfer 0.6.3. All kernels are warmed
up for 25 iterations before timing.


**Workload** **configuration.** The main text focuses on the decode-centric configuration


_D_ = 4 _,_ 096 _,_ _V_ = 151 _,_ 936 _,_


which matches models such as Qwen3-8B and Qwen3-235B-A22B MoE. We sweep batch sizes
_B_ _∈{_ 1 _,_ 2 _,_ 4 _,_ 8 _,_ 16 _,_ 32 _,_ 64 _,_ 128 _,_ 256 _}_ . Additional results for a larger configuration show the same
qualitative trends (Appendix A).


**Baselines.**
1. **Multinomial** **Sampling.** This baseline materializes the logits using a matmul (cuBLAS), followed
by sampling with softmax and multinomial. We apply `torch.compile` to it, which improves
speed by 14% on average over PyTorch eager (range: 7–30% across GPUs and batch sizes).
Unless explicitly stated, all references to Multinomial Sampling refer to the compiled version.


2. **FI1** **(FlashInfer** **top-** _k_ **/top-** _p_ **).** `top_k_top_p_sampling_from_logits` [§], a sampling kernel used
by vLLM for top- _k_ /top- _p_ decode. Logits are also materialized using cuBLAS.


3. **FI2** **(FlashInfer** **Gumbel-Max).** `sampling_from_logits` [§], FlashInfer’s exact Gumbel-Max sampler on pre-materialized logits. Logits materialized using cuBLAS.


§ `[https://docs.flashinfer.ai/api/sampling.html](https://docs.flashinfer.ai/api/sampling.html)`


12


**5.2** **Standalone** **Logits** **Sampling**


Standalone FlashSampling applies Gumbel-Max to pre-materialized logits. This is algorithmically
close to FI2, which also uses Gumbel-Max on materialized logits. We therefore focus on the
fused setting, which is the primary systems contribution: FlashSampling’s advantage comes from
eliminating the logits materialization and the sampling pass.


**5.3** **Fused** **Matmul** **and** **Sampling**


Table 3 reports FlashSampling speedups relative to the three baselines ( _D_ =4096, _V_ =151k). All
numbers are median latency over 100 timed iterations.


**Table** **3** FlashSampling speedup vs. three baselines ( _D_ =4096, _V_ =151k). Values _>_ 1 indicate FlashSampling
is faster; bold marks the peak per GPU within each baseline. FI1: FlashInfer top- _k_ /top- _p_ kernel. FI2:
FlashInfer Gumbel-Max kernel.


_vs._ _Multinomial_ _Sampling_ _vs._ _FI1_ (top- _k_ /top- _p_ ) _vs._ _FI2_ (Gumbel-Max)


_B_ H100 H200 B200 B300 H100 H200 B200 B300 H100 H200 B200 B300


1 1.25 1.28 1.46 1.46 1.30 1.35 1.51 2.45 1.18 1.20 1.32 1.31
2 1.24 1.26 1.46 1.43 1.30 1.38 1.56 2.18 1.16 1.17 1.30 1.28
4 1.24 1.27 1.47 1.44 1.32 1.41 1.61 2.37 1.16 1.18 1.32 1.30
8 1.27 1.31 1.53 1.50 1.33 1.44 1.61 2.46 1.17 1.19 1.33 1.30
16 1.30 1.37 1.57 1.54 1.35 1.45 1.65 2.47 1.18 1.21 1.36 1.33
32 1.38 1.47 1.68 1.64 1.37 **1.47** **1.68** 2.47 1.20 **1.22** 1.38 1.34
64 1.60 **1.60** 1.84 1.81 **1.46** 1.47 1.67 **2.52** **1.26** 1.21 **1.39** **1.37**





1 2 4 8 16 32 64 128 256
Batch Size





1 2 4 8 16 32 64 128 256
Batch Size



**Figure** **2** Relative performance on B300. Left: FlashSampling vs. the Multinomial Sampling (baseline
= 1). Right: FlashSampling vs. FlashInfer FI1 and FI2 (baseline = 1). FlashSampling is faster than the
Multinomial Sampling across all shown batch sizes, faster than FI1 throughout, and faster than FI2 in the
decode regime.


13


**Key** **observations.**
1. **FlashSampling** **is** **consistently** **faster** **in** **the** **decode** **regime.** For _B_ _≤_ 64, FlashSampling is faster
than all three baselines on all four GPUs. In this regime, the peak speedup vs. Multinomial
Sampling is 1 _._ 84 _×_ and the peak speedup vs. FI1 is 2 _._ 52 _×_ .


2. **The gain** **is primarily from fusion.** Speedups over FI2 are smaller than speedups over Multinomial
Sampling or FI1 because FI2 already uses Gumbel-Max. The remaining gain therefore comes
mainly from eliminating logits materialization and sampling overhead (Section 5.4).


3. **The** **advantage** **narrows** **at** **larger** **batch** **sizes.** As batch size grows, GEMM efficiency matters
more and the workload becomes less dominated by memory-bandwidth-bound postprocessing.
The larger-configuration appendix shows the same qualitative trend, with the crossover occurring
earlier.


**5.4** **Interpreting** **the** **Batch-Size** **Trend**


The cost model in Section 4.7 showed that HBM savings from avoiding the logits write and reread
alone are small ( _≤_ 6% of traffic). Figure 3 reveals a larger effect: the baselines’ separate sampling
kernels are expensive, and their runtime grows steeply with batch size, while FlashSampling absorbs
sampling into the matmul at negligible cost (Table 4: 2–6% of kernel time). Eliminating these
separate kernels is the primary source of speedup. The advantage narrows at large batch sizes
because FlashSampling’s Triton matmul becomes less efficient than cuBLAS (right panel), partially
offsetting the sampling savings. Note that Triton is platform-agnostic (AMD, Intel GPUs, etc.),
so the cuBLAS gap is a trade-off for portability. Profiling was performed on an RTX 3090 using
Nsight Compute and Proton.


**Table** **4** Sampling as a percentage of total kernel time. A high fraction spent on sampling rather than
matmul is an indicator of inefficient sampling implementation. FlashSampling’s sampling fraction stays low
because it is fused into the matmul epilogue; the baselines’ fraction grows with batch size _B_ . Bold marks the
highest sampling fraction for each method.


_FlashSampling_ _Multinomial_ _Sampling_ _FI2_ (Gumbel-Max)


_B_ matmul (%) sampl. (%) matmul (%) sampl. (%) matmul (%) sampl. (%)


1 97.7 2.3 93.7 6.3 94.7 5.3
16 97.7 2.3 87.1 12.9 93.4 6.6
64 93.6 6.0 71.3 **28.7** 88.6 11.4
256 93.4 **6.2** 73.1 26.9 88.2 **11.8**


14


800


700


600


500


400


300


200


100


0



1 2 4 8 16 32 64 128 256
Batch Size





Batch Size





**Figure** **3** Sampling runtime (left) and matmul runtime (right) in _µ_ s vs. batch size. Lower is better.


**5.5** **Roofline** **Analysis** **and** **Bandwidth** **Utilization**


The LM-head projection is memory-bandwidth-bound at small batch sizes because arithmetic
intensity equals _B_ (the weight matrix dominates traffic). Figure 4 confirms this on H100.



10 [3]


10 [2]


10 [1]





Method
FlashSampling flashinfer:top_k_top_p_sampling_from_logits
Multinomial Sampling (Compiled) flashinfer:sampling_from_logits



100


80


60


40


20


0



3500


3000


2500


2000


1500


1000


500


0



|Pe|ak Mem|ory Band|width|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||


1 2 4 8 16 32 64 128 256
Batch Size










|Col1|Col2|Col3|b<br>bsz=12|Ridge: A<br>sz=256<br>8|
|---|---|---|---|---|
|||bsz=16<br>bsz=32<br>~~bsz~~|~~=64~~||
||bsz=1<br>bsz=2<br>bsz=4<br>|bsz=8<br>~~Roofline~~<br>FlashSampling<br>Multinomial Sampling<br>flashinfer:top_k_top_<br>flashinfer:sampling_f|(Compiled)<br>p_sampling_f<br>rom_logits|rom_logits|



10 [0] 10 [1] 10 [2]

Arithmetic Intensity (FLOP/byte)



**Figure** **4** Roofline (left) and HBM bandwidth utilization (right) on H100. Left: all methods track the
memory-bound slope for _B_ _≤_ 64; FlashSampling sits slightly above baselines because it avoids the logits
round-trip. Close to the ridge point (AI _≈_ 295), performance flattens below the compute ceiling, where
cuBLAS outperforms Triton. Right: FlashSampling achieves higher bandwidth utilization than all baselines
in the decode regime, confirming that fusion removes overhead rather than shifting it. Appendix D shows the
same pattern on B200.


**5.6** **End-to-End** **vLLM** **Evaluation**


In this section, we demonstrate the end-to-end speedups achieved by FlashSampling on LLM inference.
We integrate FlashSampling into vLLM (Kwon et al., 2023) by replacing the LM-head projection
and the sampling step. We benchmark TPOT using problems from the AIME22-24 dataset [¶] .
vLLM uses continuous batching, so the effective batch size varies dynamically during serving. We
use `vllm` `bench` `sweep` `serve` with `–max-concurrency` = _B_ to implement the batch size, and set


  - `[https://huggingface.co/datasets/AI-MO/aimo-validation-aime](https://huggingface.co/datasets/AI-MO/aimo-validation-aime)`


15


`–request-rate` = _B_ for requests to follow a Poisson process at _B_ requests per second. We rerun the
benchmark 5 times for each batch size, compare TPOT between baseline and FlashSampling, and
report the median TPOT reduction across the 5 runs. Experiments run on a single B200 GPU with
four models spanning a range of sizes and architectures.


**Key** **observation:** The speedups are proportional to the decoding time spent on the LM head
compared to attention and FFN. This explains the highest speedups on Qwen3-1.7B, which sees up
to 19% TPOT reduction. For Qwen3-32B and gpt-oss-120b, attention and FFN layers dominate
decode time, so the speedups are smaller.


**Table** **5** TPOT speedup (%) computed as (1 _−_ FlashSampling _/_ baseline), and standard deviation across 5
runs. _B_ is the maximum number of concurrent requests. Bold marks the peak per model.


_B_ Qwen3-1.7B Qwen3-8B Qwen3-32B gpt-oss-120b


1 10 _._ 8 _±_ 0 _._ 3 % 2 _._ 8 _±_ 0 _._ 9 % **1** _._ **9** _±_ 1 _._ 4 % 0 _._ 3 _±_ 0 _._ 8 %
2 12 _._ 8 _±_ 0 _._ 6 % **6** _._ **9** _±_ 1 _._ 7 % _−_ 1 _._ 8 _±_ 0 _._ 5 % 1 _._ 7 _±_ 0 _._ 5 %
4 14 _._ 5 _±_ 0 _._ 4 % 3 _._ 7 _±_ 0 _._ 1 % 1 _._ 6 _±_ 0 _._ 0 % **2** _._ **4** _±_ 0 _._ 3 %
8 15 _._ 2 _±_ 0 _._ 4 % 3 _._ 6 _±_ 0 _._ 4 % 1 _._ 1 _±_ 0 _._ 1 % 2 _._ 1 _±_ 0 _._ 1 %
16 17 _._ 7 _±_ 9 _._ 0 % 3 _._ 0 _±_ 0 _._ 4 % 1 _._ 1 _±_ 0 _._ 1 % 1 _._ 8 _±_ 0 _._ 4 %
32 9 _._ 7 _±_ 5 _._ 1 % 4 _._ 4 _±_ 1 _._ 7 % 1 _._ 3 _±_ 0 _._ 3 % 1 _._ 5 _±_ 2 _._ 0 %
64 **18** _._ **7** _±_ 6 _._ 8 % 5 _._ 2 _±_ 2 _._ 2 % 1 _._ 2 _±_ 0 _._ 3 % 1 _._ 6 _±_ 0 _._ 8 %


**5.7** **Empirical** **Correctness** **Verification**


**Kernel** **Level:** To verify sampling correctness, we compare samples from FlashSampling to the
reference PyTorch implementation using a chi-squared goodness-of-fit test on 5,000 samples, and
find no statistically significant difference.


**End-to-end** **Level:** We run FlashSampling on 1,319 questions from the GSM8K dataset using
Qwen3-1.7B and check the answers with a LLM judge. FlashSampling achieves 89 _._ 4% accuracy
versus 89 _._ 6% for the baseline. This difference is not statistically significant (p=0.776), according to
a paired bootstrap test. This is consistent with exact sampling. One cannot use greedy sampling
here, since it would disable FlashSampling.

### **6 Related Work**


**Gumbel-Max** **and** **Extensions.** The Gumbel-Max trick for exact categorical sampling dates to
Gumbel (1954) and was formalized by Maddison et al. (2014). Jang et al. (2017) introduced the
Gumbel-Softmax relaxation for differentiable discrete sampling, which complements our focus on
exact sampling. Huijben et al. (2022) surveys the broader Gumbel-Max literature. Kool et al. (2019)
extend the trick to top- _k_ sampling without replacement, and Qi et al. (2020) study fast Gumbel
variate generation. Ahmed and Singh (2026) modify the sampling distribution via entropy-aware
reweighting and use Gumbel-Max as a subroutine. FlashSampling contributes a systems-oriented


16


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||vL<br>|~~Me~~<br>LM Ba<br>|~~hod~~<br> seline<br>||||||
|||v|LM +|FlashS|amplin|g|g|||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||


Batch Size

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||<br>|~~M~~<br>vLLM B<br>|~~thod~~<br> aselin<br>|e<br>|||||
||<br>|<br>vLLM +|<br> Flash|<br> Sampli|ng|ng|||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||



Batch Size



4.0


3.5


3.0


2.5


2.0

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
||||Met<br>|hod<br>||||||
|||v<br>v|LM Ba<br>LM +|seline<br> FlashS|amplin|g||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||
|||||||||||



15.0


14.5


14.0


13.5


13.0


12.5



Batch Size

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
|||M<br>~~LLM~~|thod<br>~~ aselin~~||||||
||<br>|<br>vLLM +|<br> Flash|<br> Sampli|ng||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||



Batch Size



6.5


6.0


5.5


5.0


4.5


4.0


17.5

15.0

12.5

10.0

7.5

5.0



**Figure** **5** TPOT vs. concurrency on B200 for all four models. Top row: Qwen3-1.7B (up to 19% reduction)
and Qwen3-8B (roughly 3–7%). Bottom row: Qwen3-32B and gpt-oss-120b, where gains are smaller because
attention and FFN dominate decode time.


17


hierarchical decomposition for exact online and distributed sampling in LLM inference, preserving
the original distribution exactly.


**IO-Aware** **Kernel** **Fusion.** FlashAttention (Dao et al., 2022) showed that avoiding materialization
of the attention matrix can substantially reduce HBM traffic, with subsequent work improving
parallelism (Dao, 2024) and exploiting hardware asynchrony (Shah et al., 2024). Cut Your Losses
(Wijmans et al., 2025), Liger Kernel (Hsu et al., 2025), and Dong and Chang (2025) apply the
same idea to training-time cross-entropy by fusing the LM-head matmul with the loss computation.
The same matmul-plus-epilogue fusion pattern appears in MLP layers (Zhang et al., 2026), RNNs
(Pöppel et al., 2025), and whole-model inference (Nrusimha et al., 2025). At the compiler level,
EVT (Chen et al., 2024) auto-generates fused GEMM epilogues via CUTLASS, and Samaga et al.
(2025) fuse approximate top- _k_ selection into the matmul on TPUs. FlashSampling applies this
methodology to a different domain: inference-time sampling, exploiting domain-specific structure
(Gumbel-Max decomposability), and achieving exactness (no approximations).


**Efficient** **LLM** **Sampling** FlashInfer (Ye et al., 2025) provides optimized GPU kernels for attention
and sampling in LLM serving, including sorting-free rejection sampling for top- _k_ /top- _p_ . Qrita
(Park et al., 2026) achieves 2 _×_ throughput over prior sampling kernels via pivot-based selection.
Min- _p_ sampling (Minh et al., 2025) proposes a dynamic truncation method that, like top- _p_, requires
probability computation before truncation. SIMPLE (Zhao et al., 2025) offloads sampling to
the CPU, motivated by the same bottleneck FlashSampling addresses. Sampled softmax (Rawat
et al., 2019) reduces large-vocabulary cost by computing the loss over a random subset, trading
exactness for speed. All these methods operate on pre-materialized logits, while FlashSampling
avoids materializing them entirely and introduces no approximation.

### **7 Conclusion**


We presented **FlashSampling**, a simple fused design for exact categorical sampling that avoids
materializing the [ _B, V_ ] logits tensor in HBM. The key ideas are straightforward: exact sampling
does not require an explicit softmax, the fused tiled kernel is exact by argmax decomposition over
vocabulary tiles, and grouped log-masses yield exact online and distributed variants. The method
introduces no approximation: it produces exact samples from the target categorical distribution.
Empirically, FlashSampling is most effective in the memory-bandwidth-bound decode regime, where
it removes pure sampling overhead and turns sampling into a lightweight epilogue.

### **Acknowledgement**


We sincerely thank Yongye Zhu, Zhuoqing Song, and Mayank Mishra for their helpful discussions
and constructive feedback. We used large language models to assist in polishing the writing of this
work.


18


### **References**

Kareem Ahmed and Sameer Singh. Entropy-aligned decoding of lms for better writing and reasoning,
2026. URL `[https://arxiv.org/abs/2601.01714](https://arxiv.org/abs/2601.01714)` .


Zhaodong Chen, Andrew Kerr, Richard Cai, Jack Kosaian, Haicheng Wu, Yufei Ding, and Yuan
Xie. Evt: Accelerating deep learning training with epilogue visitor tree. In _Proceedings_ _of_
_the_ _29th_ _ACM_ _International_ _Conference_ _on_ _Architectural_ _Support_ _for_ _Programming_ _Languages_
_and_ _Operating_ _Systems,_ _Volume_ _3_, ASPLOS ’24, page 301–316, New York, NY, USA, 2024.
Association for Computing Machinery. ISBN 9798400703867. doi: 10.1145/3620666.3651369.
URL `[https://doi.org/10.1145/3620666.3651369](https://doi.org/10.1145/3620666.3651369)` .


Tri Dao. Flashattention-2: Faster attention with better parallelism and work partitioning. In _The_
_Twelfth_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2024. URL `[https://openreview.](https://openreview.net/forum?id=mZn2Xyh9Ec)`
`[net/forum?id=mZn2Xyh9Ec](https://openreview.net/forum?id=mZn2Xyh9Ec)` .


Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. FlashAttention: Fast
and memory-efficient exact attention with IO-awareness. In _Advances_ _in_ _Neural_ _Information_
_Processing_ _Systems_, volume 35, 2022.


Jianbing Dong and Jianbin Chang. From projection to prediction: Beyond logits for scalable
language models, 2025. URL `[https://arxiv.org/abs/2511.17599](https://arxiv.org/abs/2511.17599)` .


Emil Julius Gumbel. Statistical theory of extreme values and some practical applications. _National_
_Bureau_ _of_ _Standards_ _Applied_ _Mathematics_ _Series_, 33, 1954.


Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. The curious case of neural
text degeneration. In _International_ _Conference_ _on_ _Learning_ _Representations_, 2020. URL `[https:](https://openreview.net/forum?id=rygGQyrFvH)`
`[//openreview.net/forum?id=rygGQyrFvH](https://openreview.net/forum?id=rygGQyrFvH)` .


Pin-Lun Hsu, Yun Dai, Vignesh Kothapalli, Qingquan Song, Shao Tang, Siyu Zhu, Steven Shimizu,
Shivam Sahni, Haowen Ning, Yanning Chen, and Zhipeng Wang. Liger-kernel: Efficient triton
kernels for LLM training. In _Championing_ _Open-source_ _DEvelopment_ _in_ _ML_ _Workshop_ _@_ _ICML25_,
2025. URL `[https://openreview.net/forum?id=36SjAIT42G](https://openreview.net/forum?id=36SjAIT42G)` .


Iris AM Huijben, Wouter Kool, Max B Paulus, and Ruud JG Van Sloun. A review of the gumbel-max
trick and its extensions for discrete stochasticity in machine learning. _IEEE_ _transactions_ _on_
_pattern_ _analysis_ _and_ _machine_ _intelligence_, 45(2):1353–1371, 2022.


Eric Jang, Shixiang Gu, and Ben Poole. Categorical reparameterization with Gumbel-softmax. In
_International_ _Conference_ _on_ _Learning_ _Representations_, 2017.


Oscar Key, Luka Ribar, Alberto Cattaneo, Luke Hudlass-Galley, and Douglas Orr. Approximate
top-k for increased parallelism. In _Adaptive_ _Foundation_ _Models:_ _Evolving_ _AI_ _for_ _Personalized_
_and_ _Efficient_ _Learning_, 2024. URL `[https://openreview.net/forum?id=UonuElM9kV](https://openreview.net/forum?id=UonuElM9kV)` .


Wouter Kool, Herke Van Hoof, and Max Welling. Stochastic beams and where to find them: The
Gumbel-top-k trick for sampling sequences without replacement. In Kamalika Chaudhuri and
Ruslan Salakhutdinov, editors, _Proceedings_ _of_ _the_ _36th_ _International_ _Conference_ _on_ _Machine_


19


_Learning_, volume 97 of _Proceedings_ _of_ _Machine_ _Learning_ _Research_, pages 3499–3508. PMLR,
09–15 Jun 2019. URL `[https://proceedings.mlr.press/v97/kool19a.html](https://proceedings.mlr.press/v97/kool19a.html)` .


Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph
Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model
serving with pagedattention. In _Proceedings_ _of_ _the_ _29th_ _Symposium_ _on_ _Operating_ _Systems_
_Principles_, pages 611–626, 2023.


Chris J. Maddison, Daniel Tarlow, and Tom Minka. A* sampling. In _Advances in Neural Information_
_Processing_ _Systems_, volume 27, 2014.


Maxim Milakov and Natalia Gimelshein. Online normalizer calculation for softmax. _arXiv_ _preprint_
_arXiv:1805.02867_, 2018.


Nguyen Nhat Minh, Andrew Baker, Clement Neo, Allen G Roush, Andreas Kirsch, and Ravid
Shwartz-Ziv. Turning up the heat: Min-p sampling for creative and coherent LLM outputs.
In _The_ _Thirteenth_ _International_ _Conference_ _on_ _Learning_ _Representations_, 2025. URL `[https:](https://openreview.net/forum?id=FBkpCyujtS)`
`[//openreview.net/forum?id=FBkpCyujtS](https://openreview.net/forum?id=FBkpCyujtS)` .


Aniruddha Nrusimha, William Brandon, Mayank Mishra, Yikang Shen, Rameswar Panda, Jonathan
Ragan-Kelley, and Yoon Kim. Flashformer: Whole-model kernels for efficient low-batch inference,
2025. URL `[https://arxiv.org/abs/2505.22758](https://arxiv.org/abs/2505.22758)` .


NVIDIA. NVIDIA H100 tensor core GPU architecture. Technical report, 2022. URL `[https://](https://resources.nvidia.com/en-us-data-center-overview-mc/en-us-data-center-overview/gtc22-whitepaper-hopper)`

```
 resources.nvidia.com/en-us-data-center-overview-mc/en-us-data-center-overview/
```

`[gtc22-whitepaper-hopper](https://resources.nvidia.com/en-us-data-center-overview-mc/en-us-data-center-overview/gtc22-whitepaper-hopper)` . Accessed: 2026-03-04.


NVIDIA. NVIDIA H100 tensor core GPU datasheet. Technical report, 2024.
URL `[https://www.megware.com/fileadmin/user_upload/LandingPage%20NVIDIA/](https://www.megware.com/fileadmin/user_upload/LandingPage%20NVIDIA/nvidia-h100-datasheet.pdf)`
`[nvidia-h100-datasheet.pdf](https://www.megware.com/fileadmin/user_upload/LandingPage%20NVIDIA/nvidia-h100-datasheet.pdf)` . Accessed: 2026-03-04.


Jongseok Park, Sunga Kim, Alvin Cheung, and Ion Stoica. Qrita: High-performance top-k and
top-p algorithm for gpus using pivot-based truncation and selection, 2026. URL `[https://arxiv.](https://arxiv.org/abs/2602.01518)`
`[org/abs/2602.01518](https://arxiv.org/abs/2602.01518)` .


Korbinian Pöppel, Maximilian Beck, and Sepp Hochreiter. FlashRNN: I/o-aware optimization of
traditional RNNs on modern hardware. In _The_ _Thirteenth_ _International_ _Conference_ _on_ _Learning_
_Representations_, 2025. URL `[https://openreview.net/forum?id=l0ZzTvPfTw](https://openreview.net/forum?id=l0ZzTvPfTw)` .


Yiyan Qi, Pinghui Wang, Yuanming Zhang, Junzhou Zhao, Guangjian Tian, and Xiaohong Guan.
Fast generating a large number of Gumbel-max variables. In _Proceedings_ _of_ _The_ _Web_ _Conference_,
pages 2006–2012, 2020.


Ankit Singh Rawat, Jiecao Chen, Felix Xinnan X. Yu, Ananda Theertha Suresh, and Sanjiv Kumar.
Sampled softmax with random Fourier features. In _Advances_ _in_ _Neural_ _Information_ _Processing_
_Systems_, volume 32, 2019.


Tomas Ruiz. fmms-kernel: FMMS kernel: Fused matrix-multiplication + sampling. GitHub
repository, 2026. URL `[https://github.com/tomasruizt/fmms-kernel](https://github.com/tomasruizt/fmms-kernel)` . Triton implementation
of fused matmul + Gumbel-Max sampling.


20


Yashas Samaga, Varun Yerram, Spandana Raj Babbula, Prateek Jain, and Praneeth Netrapalli.
Faster approx. top-k: Harnessing the full power of two stages, 2025. URL `[https://arxiv.org/](https://arxiv.org/abs/2506.04165)`
`[abs/2506.04165](https://arxiv.org/abs/2506.04165)` .


Jay Shah, Ganesh Bikshandi, Ying Zhang, Vijay Thakkar, Pradeep Ramani, and Tri Dao.
Flashattention-3: Fast and accurate attention with asynchrony and low-precision. In _The_
_Thirty-eighth_ _Annual_ _Conference_ _on_ _Neural_ _Information_ _Processing_ _Systems_, 2024. URL
`[https://openreview.net/forum?id=tVConYid20](https://openreview.net/forum?id=tVConYid20)` .


Erik Wijmans, Brody Koh, Roei Herzig, Jitendra Jain, Jianwei Zhu, Saurabh Kapoor, and Ross
Girshick. Cut your losses in large-vocabulary language models. _arXiv_ _preprint_ _arXiv:2411.09009_,
2025.


Zihao Ye, Lequn Chen, Ruihang Lai, Wuwei Lin, Yineng Zhang, Stephanie Wang, Tianqi Chen,
Baris Kasikci, Vinod Grover, Arvind Krishnamurthy, et al. Flashinfer: Efficient and customizable
attention engine for llm inference serving. _Proceedings_ _of_ _Machine_ _Learning_ _and_ _Systems_, 7, 2025.


Zixi Zhang, Zhiwen Mo, Yiren Zhao, and Robert Mullins. Deep kernel fusion for transformers, 2026.
URL `[https://arxiv.org/abs/2602.11808](https://arxiv.org/abs/2602.11808)` .


Bohan Zhao, Zane Cao, and Yongchao He. Simple: Disaggregating sampling from gpu inference into
a decision plane for faster distributed llm serving, 2025. URL `[https://arxiv.org/abs/2512.](https://arxiv.org/abs/2512.00719)`
`[00719](https://arxiv.org/abs/2512.00719)` .


21


# **Appendix**

**A** **Additional** **Kernel** **Results** **for** **the** **Large** **Configuration** **23**


**B** **FlashSampling** **Algorithm** **Pseudocode** **23**


**C** **Numerically** **Stable** **and** **Fast** **Gumbel** **Generation** **25**


**D** **Roofline** **and** **Bandwidth** **Utilization** **on** **B200** **26**


**E** **Returning** **Log-Normalizers** **or** **Max** **Values** **26**


22


### **A Additional Kernel Results for the Large Configuration**

For completeness, Table 6 reports the larger-configuration kernel results deferred from the main
text. The same qualitative pattern appears: FlashSampling is strongest in the small-batch decode
regime, while the advantage narrows once the workload becomes more GEMM-efficiency dominated.


**Table** **6** FlashSampling speedup vs. three baselines on the larger configuration ( _D_ =8192, _V_ =128k). Values

_>_ 1 indicate FlashSampling is faster; bold marks the peak per GPU within each baseline. At _B≥_ 128 the
advantage narrows and cuBLAS GEMM efficiency becomes increasingly important.


_vs._ _Multinomial_ _Sampling_ _vs._ _FI1_ (top- _k_ /top- _p_ ) _vs._ _FI2_ (Gumbel-Max)


_B_ H100 H200 B200 B300 H100 H200 B200 B300 H100 H200 B200 B300


1 1.22 1.22 1.43 1.39 1.21 1.17 1.31 1.51 1.13 1.09 1.20 1.18
2 1.20 1.19 1.38 1.35 1.18 1.19 1.32 1.77 1.12 1.08 1.20 1.17
4 1.20 1.19 1.34 1.33 1.18 1.20 1.23 1.75 1.12 1.09 1.13 1.13
8 1.21 1.21 1.32 1.30 1.21 1.22 1.27 1.72 1.13 1.09 1.13 1.12
16 1.23 1.24 1.35 1.34 1.22 1.23 1.30 1.77 1.14 1.11 1.13 1.13
32 1.25 1.31 1.42 1.39 1.22 1.28 1.34 1.79 1.14 1.16 1.18 1.16
64 **1.36** **1.39** **1.54** **1.52** **1.28** **1.30** **1.42** **1.88** **1.18** **1.17** **1.26** **1.25**


128 1.29 0.99 1.44 1.49 1.14 0.86 1.26 1.64 1.03 0.76 1.12 1.14
256 0.88 0.76 1.15 1.17 0.80 0.72 1.08 1.44 0.70 0.64 0.92 0.90

### **B FlashSampling Algorithm Pseudocode**


This appendix collects detailed pseudocode for the FlashSampling variants described in the main
text.


**Streaming** **Gumbel-Max** **(standalone** **logits).** Algorithm B.1 presents the basic one-pass streaming
Gumbel-Max sampler over pre-materialized logits.


**Algorithm** **B.1** Gumbel-Max sampling (standalone logits): streaming argmax over perturbed logits


**Require:** Logits _**ℓ**_ _∈_ R _[V]_, RNG state
**Ensure:** Sample index _i_ _[⋆]_ _∈{_ 1 _, . . ., V }_

1: _m ←−∞_, _i_ _[⋆]_ _←_ 1

2: **for** _i_ = 1 **to** _V_ **do**

3: _g_ _←_ Gumbel(0 _,_ 1) _▷_ via _g_ = _−_ log( _−_ log _u_ ), _u ∼_ Unif(0 _,_ 1)

4: _s ←_ _ℓi_ + _g_

5: **if** _s > m_ **then**

6: _m ←_ _s_, _i_ _[⋆]_ _←_ _i_

7: **end** **if**

8: **end** **for**

9: **return** _i_ _[⋆]_


23


**Parallel** **Group-Gumbel-Max.** Algorithm B.2 extends streaming Gumbel-Max to a group-parallel
setting where each group is processed by an independent threadblock.


**Algorithm** **B.2** FlashSampling (parallel): Group-Gumbel-Max over groups


**Require:** Input _**x**_ _∈_ R _[d]_, weight matrix _**W**_ _∈_ R _[d][×][V]_, group size _g_ (so _V_ = _mg_ ), RNG state
**Ensure:** Sample index _z_ _∈{_ 1 _, . . ., V }_ and optional log-normalizer _ℓZ_ = logsumexp( _**y**_ )

1: **for** _k_ = 0 **to** _m −_ 1 **in** **parallel** **do**

2: _**y**_ _k_ _←_ _**W**_ _k_ _[⊤]_ _**[x]**_ _[ ∈]_ [R] _[g]_

3: _zk_ _←_ argmax _j∈_ [ _g_ ]  - _yk,j_ _−_ log( _−_ log _uk,j_ )� _▷uk,j ∼_ Unif(0 _,_ 1)

4: _Lk_ _←_ logsumexp( _**y**_ _k_ )

5: **end** **for**

6: _k_ _[⋆]_ _←_ argmax _k∈_ [ _m_ ]  - _Lk −_ log( _−_ log ¯ _uk_ )� _▷_ _u_ ¯ _k ∼_ Unif(0 _,_ 1)

7: _z_ _←_ _k_ _[⋆]_ _g_ + _zk⋆_ _▷_ map group-local index to global vocabulary index

8: _ℓZ_ _←_ logsumexp([ _L_ 0 _, . . ., Lm−_ 1]) _▷_ optional

9: **return** ( _z, ℓZ_ )


**Sequential/online** **Group-Gumbel-Max.** Algorithm B.3 provides a memory-efficient variant that
streams groups one at a time.


**Algorithm** **B.3** FlashSampling (sequential/online): streaming Group-Gumbel-Max with _O_ ( _g_ )
working memory


**Require:** Input _**x**_ _∈_ R _[d]_, weight matrix _**W**_ _∈_ R _[d][×][V]_, group size _g_ (so _V_ = _mg_ ), RNG state
**Ensure:** Sample index _z_ _∈{_ 1 _, . . ., V }_ and optional log-normalizer _ℓZ_

**Initialize** **with** **the** **first** **group.**

1: _**y**_ 0 _←_ _**W**_ 0 _[⊤]_ _**[x]**_ _[ ∈]_ [R] _[g]_

2: _L_ 0 _←_ logsumexp( _**y**_ 0)

3: _z_ 0 _←_ argmax _j∈_ [ _g_ ]  - _y_ 0 _,j_ _−_ log( _−_ log _u_ 0 _,j_ )� _▷u_ 0 _,j ∼_ Unif(0 _,_ 1)

4: _z_ _←_ _z_ 0, _ℓ_ _←_ _L_ 0
5: **for** _k_ = 1 **to** _m −_ 1 **do**

6: _**y**_ _k_ _←_ _**W**_ _k_ _[⊤]_ _**[x]**_ _[ ∈]_ [R] _[g]_

7: _Lk_ _←_ logsumexp( _**y**_ _k_ )

8: _ℓ_ new _←_ logsumexp([ _ℓ,_ _Lk_ ])

_e_ _[L][k]_
9: _p_ replace _←_ exp( _Lk −_ _ℓ_ new) _▷_ = _e_ _[ℓ]_ + _e_ _[Lk]_
10: Draw _u ∼_ Unif(0 _,_ 1)

11: **if** _u < p_ replace **then**

12: _zk_ _←_ argmax _j∈_ [ _g_ ] - _yk,j_ _−_ log( _−_ log _uk,j_ )� _▷_ sample within selected group

13: _z_ _←_ _kg_ + _zk_
14: **end** **if**

15: _ℓ_ _←_ _ℓ_ new
16: **end** **for**

17: _ℓZ_ _←_ _ℓ_ _▷_ optional

18: **return** ( _z, ℓZ_ )


24


**Distributed** **Group-Gumbel-Max.** Algorithm B.4 extends FlashSampling to tensor-parallel vocabularies sharded across multiple GPUs.


**Algorithm** **B.4** FlashSampling (distributed, tensor-parallel vocab): communicate _O_ (1) scalars per
rank

**Require:** World size _n_ . Rank _k_ _∈{_ 0 _, . . ., n_ _−_ 1 _}_ holds shard _**W**_ [(] _[k]_ [)] _∈_ R _[d][×]_ [(] _[V/n]_ [)] covering vocab indices
_{k · V/n_ + 1 _, . . .,_ ( _k_ + 1) _· V/n}_ . Input _**x**_ _∈_ R _[d]_, RNG state.
**Ensure:** Global sample index _z_ _∈{_ 1 _, . . ., V }_ (and optional _ℓZ_ )

1: On each rank _k_ :

compute local logits _**y**_ [(] _[k]_ [)] _←_ ( _**W**_ [(] _[k]_ [)] ) _[⊤]_ _**x**_ _∈_ R _[V/n]_

compute local log-mass _Lk_ _←_ logsumexp( _**y**_ [(] _[k]_ [)] )
sample local index _z_    - _k_ _∼_ Cat(softmax( _**y**_ [(] _[k]_ [)] )) _▷_ e.g., via Gumbel-Max / Group-Gumbel-Max /
fused kernel



2: All-gather _{_ ( _Lk,_ - _zk_ ) _}_ _[n]_ _k_ =0 _[−]_ [1] [to] [a] [coordinator] [(or] [perform] [an] [equivalent] [reduction)]



3: Sample winning rank _k_ _[⋆]_ _←_ argmax _k∈_ [ _n_ ] - _Lk −_ log( _−_ log ¯ _uk_ )� _▷_ _u_ ¯ _k ∼_ Unif(0 _,_ 1)

4: _z_ _←_ _k_ _[⋆]_ _·_ ( _V/n_ ) + _z_ - _k⋆_ _▷_ convert rank-local index to global



5: Optionally _ℓZ_ _←_ logsumexp([ _L_ 0 _, . . ., Ln−_ 1])



6: **return** _z_ (and _ℓZ_ )

### **C Numerically Stable and Fast Gumbel Generation**


Gumbel noise can be generated as _g_ = _−_ log( _−_ log _u_ ) with _u_ _∼_ Unif(0 _,_ 1). In GPU kernels, two
issues matter:

- **Numerical** **stability:** avoid _u_ = 0 or _u_ = 1 which lead to infinities.


- **Throughput:** the cost of generating random numbers and computing logs should not dominate.


**Practical** **recipe.** Given a 32-bit RNG output _r_ _∈{_ 0 _, . . .,_ 2 [32] _−_ 1 _}_, map to


_r_ + 1
_u_ = 2 [32] + 1 _[∈]_ [(0] _[,]_ [ 1)] _[,]_


then compute _g_ = _−_ log( _−_ log _u_ ). Many GPU RNG libraries (e.g. Philox, XORWOW) support
generating floats in (0 _,_ 1) directly; the above mapping is a safe fallback.


**Approximate** **log** **options.** If exactness in the distribution is required, the Gumbel generation must
be statistically correct. However, using fast approximate log implementations can introduce small
distortions. FlashSampling supports two modes:

- **Exact-math** **mode:** use standard log for high fidelity.


- **Fast-math** **mode:** use approximate logs for speed, with empirical validation that sampling bias
remains negligible for target applications.
The sampling remains _algorithmically_ _exact_ with respect to the generated Gumbels; any bias comes
from numeric approximations.


25


### **D Roofline and Bandwidth Utilization on B200**

Figure 6 shows the roofline and bandwidth utilization on B200. The same pattern holds: FlashSampling tracks the memory-bound slope more closely and achieves higher bandwidth utilization than
all baselines in the decode regime.


Method
FlashSampling flashinfer:top_k_top_p_sampling_from_logits
Multinomial Sampling (Compiled) flashinfer:sampling_from_logits



10 [3]


10 [2]


10 [1]





|Pe|ak Mem|ory Band|width|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||||||||||
|||||||||||


1 2 4 8 16 32 64 128 256
Batch Size



8000

7000

6000

5000

4000

3000

2000

1000

0



100


80


60


40


20


0










|Col1|Col2|Col3|Col4|Ridge: A|
|---|---|---|---|---|
||||bsz=1|28<br>bsz=256|
||b|sz=8<br>bsz=16<br>~~bsz=32~~<br>bsz<br>Roofline<br>|64||
||bsz=1<br>bsz=2<br>bsz=4|FlashSampling<br>Multinomial Sampling<br>flashinfer:top_k_top_p<br>flashinfer:sampling_fr|(Compiled)<br>_sampling_<br>om_logits|<br>from_logits|



10 [0] 10 [1] 10 [2]

Arithmetic Intensity (FLOP/byte)



**Figure** **6** Roofline (left) and HBM bandwidth utilization (right) on B200 ( _D_ =4096, _V_ =151k). The pattern
matches H100 (Figure 4): FlashSampling uses bandwidth more efficiently in the memory-bound decode
regime and narrows at large batch sizes where cuBLAS GEMM efficiency dominates.

### **E Returning Log-Normalizers or Max Values**


Some applications need log _Z_ = log [�] _j_ _[e]_ [�] _[ℓ][j]_ [,] [for] [example] [to] [compute] [log-probabilities.] [The] [core]
FlashSampling sampler does not need log _Z_, but it can be added as an optional mode by accumulating
a numerically stable log-sum-exp alongside sampling. In fused settings, this requires extra work in
the epilogue, so we treat it as an optional feature rather than part of the core design.


26


