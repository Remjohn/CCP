# **Residual Stream Duality in Modern** **Transformer Architectures**

**Yifan** **Zhang**

```
            yifanzhangresearch@gmail.com

```

March 16, 2026


**Abstract**


Recent work has made clear that the residual pathway is not mere optimization plumbing; it
is part of the model’s representational machinery. We agree, but argue that the cleanest way
to organize this design space is through a two-axis view of the Transformer. A decoder evolves
information along two ordered dimensions: sequence position and layer depth. Self-attention
already provides adaptive mixing along the sequence axis, whereas the residual stream usually
performs fixed addition along the depth axis. If we fix a token position and treat layer index as
the ordered variable, then a causal depth-wise residual attention read is exactly the same local
operator as causal short sliding-window attention (ShortSWA), except written over depth rather
than over sequence. This is the core residual stream duality behind Transformer [2] .
This perspective also clarifies the recent literature. ELC-BERT and DenseFormer already
show that learned aggregation over depth can outperform uniform residual accumulation, while
Vertical Attention, DeepCrossAttention (DCA), MUDDFormer, and Attention Residuals move
further toward explicit attention-based routing over earlier layers. The key point, however, is
that operator-level duality does not imply systems-level symmetry. For large-scale autoregressive
models, sequence-axis ShortSWA is usually the more hardware-friendly placement because it
reuses token-side sliding-window kernels, KV-cache layouts, and chunked execution. If the goal
is instead to change the shortcut itself, Deep Delta Learning (DDL) is the cleaner intervention
because it modifies the residual operator directly rather than adding a separate cross-layer
retrieval path. Our recommendation is therefore simple: use DDL when the shortcut is the
object of interest, and use sequence-axis ShortSWA when the goal is local adaptive mixing.


`Project` `Page` : `[https://github.com/yifanzhang-pro/residual-stream-duality](https://github.com/yifanzhang-pro/residual-stream-duality)`

#### **1 Introduction**


A modern Transformer evolves information along two ordered axes: sequence position and layer
depth. Along the sequence axis, self-attention performs learned, content-dependent mixing. Along
the depth axis, the residual stream usually performs uniform addition. The title Transformer [2] is
meant literally: modern Transformer architectures have two ordered directions of information flow,
but only one of them is usually equipped with an adaptive attention operator. The main theme of
this note is that this asymmetry is conceptually revealing and practically consequential.
That asymmetry has already motivated a broad family of proposals that replace or augment
uniform depth aggregation. Earlier examples include ELC-BERT, which feeds each layer a convex


1


Layer Depth ( _ℓ_ )





Sequence Position ( _t_ )


**Figure** **1** **Overview** **of** **Residual** **Stream** **Duality.** A modern Transformer evolves information along two
ordered dimensions: sequence position and layer depth. Computing the target state _h_ [(] _t_ _[ℓ]_ [)] via explicit depth-wise
residual attention operates identically to causal short sliding-window attention (ShortSWA) on the sequence
axis, effectively bridging the representation mechanisms of the two pathways.


combination of earlier layer outputs, and DenseFormer, which inserts a depth-weighted average
after each block (Charpentier and Samuel, 2023; Pagliardini et al., 2024). More recent work makes
the cross-depth routing explicitly attention-based, including Vertical Attention, DeepCrossAttention
(DCA), MUDDFormer, and Attention Residuals (Kojima et al., 2026; Heddes et al., 2025; Xiao
et al., 2025; Chen et al., 2026). Related interventions such as Hyper-Connections and Deep Delta
Learning (DDL) further underscore that shortcut design remains an active architectural degree
of freedom (Zhu et al., 2024; Zhang et al., 2026). The shared lesson is that the residual pathway
participates in representation, not merely optimization.
Our claim is not that all of these proposals are identical. ELC-BERT and DenseFormer sit on
the learned-static end of the spectrum; Vertical Attention, DCA, MUDDFormer, and Attention
Residuals use more expressive routing modules. But the common object is learned aggregation
over the ordered depth axis. The cleanest exact statement applies to explicit depth-wise attention
reads: once a token position is fixed and layer index is treated as a one-dimensional ordered axis, a
truncated residual attention read is precisely causal ShortSWA written over depth. The full-memory
variant is simply the full-window limit of the same operator family.
That duality is mathematical, not systems-symmetric. Sequence-axis ShortSWA reuses existing
sliding-window attention kernels, token-side KV-cache layouts, and chunked execution strategies.
Depth-axis aggregation, by contrast, requires an additional layer-indexed state path: each block


2


needs online access to earlier layer states or block summaries for the same token, and under pipeline
parallelism those states may need to be forwarded, stored, or recomputed. The practical question is
therefore not whether attention can be applied over depth, but whether depth is the right axis on
which to place a short adaptive mixer.
The thesis of this note is therefore:

- A depth-wise residual attention read is not a new local operator; it is ShortSWA written on the
depth axis rather than the sequence axis.


- Learned cross-depth aggregation spans a continuum from static depth weighting (ELC-BERT,
DenseFormer) to attention-based routing (Vertical Attention, DCA, MUDDFormer, Attention
Residuals). These systems are not identical end-to-end, but they occupy the same design space.


- Once that distinction is explicit, the natural design choice is either to use Deep Delta Learning (Zhang et al., 2026) to improve the shortcut itself or to place ShortSWA directly on the
sequence axis, which is usually more hardware-efficient for current training and inference stacks.


- Following Zhang (2025), we view ShortSWA as the successor to ShortConv and, in spirit, the
attention-form successor to Canon layers (Allen-Zhu, 2025).


**Relation to prior depth-aggregation work.** ELC-BERT and DenseFormer are important precursors
because they already replace uniform depth accumulation with learned aggregation. ELC-BERT
feeds each layer a convex combination of previous layer outputs, while DenseFormer adds a depthweighted average of current and past representations after each block (Charpentier and Samuel, 2023;
Pagliardini et al., 2024). Vertical Attention, DCA, MUDDFormer, and Attention Residuals move
further toward attention-based routing over earlier layers (Kojima et al., 2026; Heddes et al., 2025;
Xiao et al., 2025; Chen et al., 2026). Our claim is therefore not that these methods are end-to-end
identical. It is that, once depth is treated as an ordered axis, they are best compared inside one
common design space of learned cross-depth aggregation. DDL, by contrast, attacks a different
target: it changes the shortcut update itself rather than adding a separate retrieval path over stored
earlier states (Zhang et al., 2026). Hyper-Connections make a related point, that residual design is
itself a meaningful architectural degree of freedom, but they do not remove the systems asymmetry
between token-side local mixing and layer-side state management (Zhu et al., 2024).


**Relation** **to** **ShortConv** **and** **Canon** **layers.** ShortConv, Canon layers, and ShortSWA all occupy
the same architectural slot: they are local mixers that operate before or alongside a broader global
mechanism. ShortConv uses a fixed, small kernel. Canon layers compute learned weighted sums
over nearby tokens (Allen-Zhu, 2025). As argued in Zhang (2025), once chunked computation is
already part of the implementation, the natural upgrade is ShortSWA: the same local role, but with
content-adaptive mixing and a chunk-aligned receptive field. In that sense, ShortSWA is the natural
successor to ShortConv and the attention-form successor to Canon layers.

#### **2 Residual Stream Duality**


**2.1** **Preliminaries**


Let _H_ = [ _H_ [(0)] _, . . ., H_ [(] _[L]_ [)] ] _∈_ R [(] _[L]_ [+1)] _[×][T]_ _[×][d]_ denote the hidden-state stack of an _L_ -block decoder, where
_H_ [(0)] is the input stream, _T_ is the sequence length, and _d_ is the model width. We write _H_ [(] _[ℓ]_ [)] _∈_ R _[T]_ _[×][d]_


3


for the hidden states at depth _ℓ_ . A standard pre-norm Transformer block, for _ℓ_ = 0 _, . . ., L −_ 1, is


                     -                     _U_ [(] _[ℓ]_ [)] = _H_ [(] _[ℓ]_ [)] + Attn Norm _H_ [(] _[ℓ]_ [)][��] _,_


                     -                      _H_ [(] _[ℓ]_ [+1)] = _U_ [(] _[ℓ]_ [)] + MLP Norm _U_ [(] _[ℓ]_ [)][��] _._


The sequence axis is mixed adaptively by attention, while the depth axis is mixed by fixed addition.


**2.2** **Depth-wise** **residual** **attention** **is** **ShortSWA** **on** **the** **depth** **axis**


Fix a token position _t_ and collect its trajectory through depth:


_Xt_ = [ _h_ [(0)] _t_ [;] _[ h]_ _t_ [(1)][;] _[ · · ·]_ [;] _[ h]_ [(] _t_ _[L]_ [)] ] _∈_ R [(] _[L]_ [+1)] _[×][d]_ _._


Now consider a causal depth window of size _K_ . Define


_Wt,ℓ_ [(] _[K]_ [)] = [ _h_ [(max(0] _t_ _[,ℓ][−][K]_ [+1))] ; _. . ._ ; _h_ [(] _t_ _[ℓ]_ [)][]] _[ ∈]_ [R] _[K][ℓ][×][d][,]_ _Kℓ_ = min( _K, ℓ_ + 1) _._


A depth-wise residual attention read at layer _ℓ_ can be written as


_qt,ℓ_ = _WQh_ [(] _t_ _[ℓ]_ [)] _[,]_ **K** _t,ℓ_ = _Wt,ℓ_ [(] _[K]_ [)] _[W][K][,]_ **V** _t,ℓ_ = _Wt,ℓ_ [(] _[K]_ [)] _[W][V][,]_







_zt_ [(] _[ℓ]_ [)] = softmax




- _qt,ℓ_ ~~_√_~~ **K** _⊤t,ℓ_
_dk_



**V** _t,ℓ._



This is exactly causal ShortSWA applied to the one-dimensional sequence _Xt_ whose index is the
layer number:
_zt_ [(] _[ℓ]_ [)] = ShortSWA� _Xt_ ; _K_                      - _ℓ_ _[.]_


Hence, after transposing the hidden-state tensor so that depth becomes the ordered axis, truncated
depth-wise residual attention and ShortSWA belong to the same operator family. The full-memory
residual attention variant is simply the full-window limit _K_ = _ℓ_ + 1.
This exact equivalence applies whenever the cross-depth retrieval is implemented as an explicit
attention read. Simpler learned-weight schemes such as ELC-BERT or DenseFormer belong to the
same broader design space but are not literally instances of the QKV operator above (Charpentier
and Samuel, 2023; Pagliardini et al., 2024).


**2.3** **A** **unified** **view** **of** **learned** **depth** **aggregation**


The exact equivalence above applies to the explicit depth-wise residual attention read written here.
It also suggests a useful taxonomy of nearby methods. ELC-BERT and DenseFormer are learned
depth aggregators with parameterized weights over earlier layers, but without a full depth-wise QK
attention read (Charpentier and Samuel, 2023; Pagliardini et al., 2024). Vertical Attention, DCA,
MUDDFormer, and Attention Residuals are closer to the explicit attention end of the spectrum:
Vertical Attention learns inter-layer paths through routing modules, DCA computes attention
inputs from mixtures of previous layer outputs, MUDDFormer introduces separate dynamic dense
modules for query, key, value, and residual streams, and Attention Residuals presents the read most
directly as attention over depth (Kojima et al., 2026; Heddes et al., 2025; Xiao et al., 2025; Chen
et al., 2026). These systems are not identical end-to-end architectures; they differ in factorization,


4


parameter sharing, gating, and injection point. What the duality statement contributes is a common
coordinate system: once depth is treated as an ordered axis, explicit cross-depth attention is simply
local causal attention on that axis, and the broader family can be read as increasingly expressive
parameterizations of learned depth aggregation.


**2.4** **Why** **the** **sequence** **axis** **is** **the** **better** **placement**


Once the equivalence above is explicit, the main design question becomes where to place the short
attention primitive when the goal is local adaptive mixing. Our view is that the sequence axis is
the better answer:
_S_ [(] _[ℓ]_ [)] = _H_ [(] _[ℓ]_ [)] + ShortSWA�Norm( _H_ ( _ℓ_ )); _w_           - _,_


                     -                     _A_ [(] _[ℓ]_ [)] = _S_ [(] _[ℓ]_ [)] + Attn Norm _S_ [(] _[ℓ]_ [)][��] _,_


                     -                      _H_ [(] _[ℓ]_ [+1)] = _A_ [(] _[ℓ]_ [)] + MLP Norm _A_ [(] _[ℓ]_ [)][��] _._


This preserves the same local-to-global story but places the adaptive local mixer on the axis that
modern kernels and inference stacks already optimize.
At autoregressive inference time, sequence-axis ShortSWA can reuse the usual token-side cache
layout over the most recent _w_ tokens. In chunked training or inference, the local window can be
aligned to the chunk already loaded into SRAM. Under pipeline parallelism, the implementation
preserves the standard forward flow of activations between layer partitions rather than introducing
an additional layer-indexed state path. Depth-axis attention-style aggregation faces the opposite
incentives: each block needs online access to earlier layer states or block summaries for the same
token. Methods such as Vertical Attention, DCA, MUDDFormer, and blockwise Attention Residuals
differ in how they parameterize or compress this access, but they all live with the same underlying
pressure: depth-side routing must manage cross-layer state explicitly (Kojima et al., 2026; Heddes
et al., 2025; Xiao et al., 2025; Chen et al., 2026). If the target is instead the shortcut operator itself,
we would choose Deep Delta Learning rather than add another cross-depth read, because DDL
changes the residual update directly and does not require an explicit stack of earlier layer states
(Zhang et al., 2026).


**2.5** **Recommended** **block**


The resulting recommendation is therefore a clean two-way design fork:

- If the goal is a better shortcut, use Deep Delta Learning (Zhang et al., 2026).


- If the goal is a local content-adaptive mixer, use ShortSWA directly on the sequence axis.

For current large-scale training and inference stacks, we do not see a general systems case for a third
option that repackages sequence-local attention as a depth-axis residual mechanism. The second
choice yields the following block.


**2.6** **Complexity** **and** **systems** **notes**


Ignoring head-wise constants, ShortSWA adds a local attention term of roughly _O_ ( _Twd_ ) per layer,
where _w_ _≪_ _T_ . If a block still includes full self-attention, the asymptotic sequence-mixing cost
remains _O_ ( _T_ [2] _d_ ) up to constant factors. The important point is not a new asymptotic regime, but


5


**Algorithm** **1** Recommended local-to-global block when the goal is sequence-side local mixing



**Require:** hidden states _H_ [(] _[ℓ]_ [)], local window _w_



1: _S_ [(] _[ℓ]_ [)] _←_ _H_ [(] _[ℓ]_ [)] + ShortSWA(Norm( _H_ [(] _[ℓ]_ [)] ); _w_ )



2: _A_ [(] _[ℓ]_ [)] _←_ _S_ [(] _[ℓ]_ [)] + Attn(Norm( _S_ [(] _[ℓ]_ [)] ))



3: _H_ [(] _[ℓ]_ [+1)] _←_ _A_ [(] _[ℓ]_ [)] + MLP(Norm( _A_ [(] _[ℓ]_ [)] ))



a better hardware placement: the local operation lives on the token axis and can reuse standard
sliding-window kernels and KV-cache layouts.
The next estimates apply to explicit attention-style reads over depth, not to lighter learnedweight schemes such as ELC-BERT or DenseFormer. Depth-wise residual attention with a depth
window _K_ adds _O_ ( _TKd_ ) work per block, hence _O_ ( _TKLd_ ) across an _L_ -block network, together
with additional online access to earlier layer states or block summaries. The full-depth variant
grows to _O_ ( _TL_ [2] _d_ ) for the score/value interactions. These formulas make the compute overhead
visible, but the more consequential issue in practice is systems complexity: one now needs extra
layer-indexed state that must be retained, forwarded, or recomputed, especially when depth windows
cross pipeline-stage boundaries. In some deployments this behaves like a second cache over depth.
DDL avoids this depth-axis state-management overhead because it modifies the per-block shortcut
rather than attending over stored earlier layer states (Zhang et al., 2026).

#### **3 Conclusion**


The central claim of this note is a duality statement. Once sequence position and layer depth are both
treated as ordered axes, an explicit depth-wise residual attention read is simply ShortSWA written
on the transposed axis: tokens are fixed, layers become the ordered dimension, and the practically
relevant truncated variants are short causal attention over depth. Seen from this angle, learned
depth aggregation forms a continuum. ELC-BERT and DenseFormer occupy the learned-static end;
Vertical Attention, DCA, MUDDFormer, and Attention Residuals occupy the attention-based end
(Charpentier and Samuel, 2023; Pagliardini et al., 2024; Kojima et al., 2026; Heddes et al., 2025;

Xiao et al., 2025; Chen et al., 2026). These are not identical primitive families, but neither are they
conceptually unrelated.
Once stated this way, the design choice becomes cleaner. If the aim is to improve the residual
pathway itself, DDL is the more direct architectural intervention. If the aim is adaptive local mixing,
sequence-axis ShortSWA is the better system’s choice, because it aligns with existing sliding-window
kernels, token-side KV caches, and chunked execution. Following Zhang (2025), we still view
ShortSWA as the successor to ShortConv. Relative to Canon layers (Allen-Zhu, 2025), it is the
content-adaptive local-mixing upgrade. Our recommendation is therefore two-pronged: DDL for
better shortcuts, or ShortSWA on the sequence axis for local routing, not residual attention over
depth by default.
Transformer [2] is therefore not a claim that every model should attend to both axes. It is a way
to organize the design space: one operator family, two possible ordered axes, and a clear systems
preference for sequence placement unless learned cross-depth retrieval is itself the object of interest.


6


#### **References**

Zeyuan Allen-Zhu. Physics of language models: Part 4.1, architecture design and the magic of
canon layers. _arXiv_ _preprint_ _arXiv:2512.17351_, 2025.


Lucas Georges Gabriel Charpentier and David Samuel. Not all layers are equally as important:
Every layer counts bert. In _Proceedings_ _of_ _the_ _BabyLM_ _Challenge_ _at_ _the_ _27th_ _Conference_ _on_
_Computational_ _Natural_ _Language_ _Learning_, pages 238–252, 2023.


Guangyu Chen, Yu Zhang, Jianlin Su, Weixin Xu, Siyuan Pan, Yaoyu Wang, Yucheng Wang,
Guanduo Chen, Bohong Yin, Yutian Chen, Junjie Yan, Ming Wei, Y. Zhang, Fanqing Meng,
Chao Hong, Xiaotong Xie, Shaowei Liu, Enzhe Lu, Yunpeng Tai, Yanru Chen, Xin Men, Haiqing
Guo, Y. Charles, Haoyu Lu, Lin Sui, Jinguo Zhu, Zaida Zhou, Weiran He, Weixiao Huang, Xinran
Xu, Yuzhi Wang, Guokun Lai, Yulun Du, Yuxin Wu, Zhilin Yang, and Xinyu Zhou. Attention
residuals. _Github_, 2026. URL `[https://github.com/MoonshotAI/Attention-Residuals](https://github.com/MoonshotAI/Attention-Residuals)` .


Mike Heddes, Adel Javanmard, Kyriakos Axiotis, Gang Fu, MohammadHossein Bateni, and Vahab
Mirrokni. Deepcrossattention: Supercharging transformer residual connections. _arXiv_ _preprint_
_arXiv:2502.06785_, 2025.


Takeshi Kojima, Yusuke Iwasawa, Rio Yokota, Yusuke Miyao, Jun Suzuki, and Yutaka Matsuo.
Vertical attention: Automatic exploration of inter-layer connections in transformer-based language
models. _Openreview_, 2026.


Matteo Pagliardini, Amirkeivan Mohtashami, Francois Fleuret, and Martin Jaggi. Denseformer:
Enhancing information flow in transformers via depth weighted averaging. _Advances_ _in_ _neural_
_information_ _processing_ _systems_, 37:136479–136508, 2024.


Da Xiao, Qingye Meng, Shengping Li, and Xingyuan Yuan. Muddformer: Breaking residual bottlenecks in transformers via multiway dynamic dense connections. _arXiv_ _preprint_ _arXiv:2502.12170_,
2025.


Yifan Zhang. Rethinking swa: Why short sliding window attention will replace shortconv in modern
architectures. `[https://github.com/yifanzhang-pro/Rethinking-SWA](https://github.com/yifanzhang-pro/Rethinking-SWA)`, December 2025. Blog
post and project page.


Yifan Zhang, Yifeng Liu, Mengdi Wang, and Quanquan Gu. Deep delta learning. _arXiv_ _preprint_
_arXiv:2601.00417_, 2026.


Defa Zhu, Hongzhi Huang, Zihao Huang, Yutao Zeng, Yunyao Mao, Banggu Wu, Qiyang Min, and
Xun Zhou. Hyper-connections. _arXiv_ _preprint_ _arXiv:2409.19606_, 2024.

#### **Acknowledgement**


We sincerely thank Xinyu Yang for helpful discussions. We used large language models to assist in
polishing the writing of this work.


7


## **Appendix**

8


