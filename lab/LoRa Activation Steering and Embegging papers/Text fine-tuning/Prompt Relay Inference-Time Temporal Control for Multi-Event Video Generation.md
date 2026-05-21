## **Prompt Relay: Inference-Time Temporal Control for Multi-Event Video** **Generation**

Gordon Chen Ziqi Huang Ziwei Liu


S-Lab, Nanyang Technological University


[https://gordonchen19.github.io/Prompt-Relay/](https://gordonchen19.github.io/Prompt-Relay/)


**[0-2s]** The camera zooms toward the eagle’s eye as it flies. Inside the pupil, a cyberpunk city is already visible … **[2-4s]** … Cars
move close to the camera in layered traffic lanes ... **[4-6s]** The camera … starts to track and lock onto a car ... **[6-10s]** The camera
slowly zooms out … revealing that the cyberpunk scene is playing on a television screen … inside a 20th century living room …


**[0-2s]** A … rugged caveman walking … by the setting sun ... **[2-3s]** The camera whips downwards ... fills with a motion-blurred
grass texture. **[3-5s]** The camera whips rapidly upwards … revealing … a Spartan ... **[5-6s]** The camera whips rapidly downwards …

**[6-8s]** The camera whips rapidly upwards … tracks a majestic medieval knight in shining plate armor riding the horse ...


**[0-** **1s] …** A young boy is lying flat on his … staring up at the ceiling. **[1-3s]** After a brief moment, he rolls over, pushes himself up,
stands on the mattress, and starts jumping on the bed. He bounces up and down repeatedly ... **[3-6s]** The boy then runs toward a
pile of toys near the corner of the room, grabs a toy airplane, and pretends to fly it through the air …


Figure 1. **Prompt Relay** is an inference-time, training-free, plug-and-play method for enabling fine-grained temporal control by routing
each textual prompt to its intended time segment, allowing multiple events to occur in the correct order without semantic interference.



**Abstract**


_Video diffusion models have achieved remarkable progress_
_in_ _generating_ _high-quality_ _videos._ _However,_ _these_ _models_
_struggle_ _to_ _represent_ _the_ _temporal_ _succession_ _of_ _multiple_
_events_ _in_ _real-world_ _videos_ _and_ _lack_ _explicit_ _mechanisms_
_to_ _control_ _when_ _semantic_ _concepts_ _appear,_ _how_ _long_ _they_
_persist, and the order in which multiple events occur._ _Such_
_control_ _is_ _especially_ _important_ _for_ _movie-grade_ _video_ _syn-_
_thesis, where coherent storytelling depends on precise tim-_
_ing,_ _duration,_ _and_ _transitions_ _between_ _events._ _When_ _us-_
_ing a single paragraph-style prompt to describe a sequence_
_of complex events, models often exhibit semantic entangle-_



_ment, where concepts intended for different moments in the_
_video_ _bleed_ _into_ _one_ _another,_ _resulting_ _in_ _poor_ _text-video_
_alignment. To address these limitations, we propose Prompt_
_Relay,_ _an_ _inference-time,_ _plug-and-play_ _method_ _to_ _enable_
_fine-grained_ _temporal_ _control_ _in_ _multi-event_ _video_ _genera-_
_tion, requiring no architectural modifications and no addi-_
_tional_ _computational_ _overhead._ _Prompt_ _Relay_ _introduces_
_a_ _penalty_ _into_ _the_ _cross-attention_ _mechanism,_ _so_ _that_ _each_
_temporal_ _segment_ _attends_ _only_ _to_ _its_ _assigned_ _prompt,_ _al-_
_lowing_ _the_ _model_ _to_ _represent_ _one_ _semantic_ _concept_ _at_ _a_
_time and thereby improving temporal prompt alignment, re-_
_ducing semantic interference, and enhancing visual quality._


… pours milk …


… pours cereal …



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||
|||||||||||||
||||||~~**Penalty**~~|~~** Strength**~~||||||


Q (Video Tokens)



Figure 2. **Temporal** **Cross-Attention** **Routing.** Each textual prompt is associated with a specific temporal segment of the video. The
attention penalty varies smoothly across time, allowing video tokens to attend strongly to their corresponding prompt within the assigned
interval while suppressing attention to temporally irrelevant prompts. This enables multiple events (e.g., pouring cereal followed by pouring
milk) to occur in the correct order without semantic interference.



**1. Introduction**


Recent advances in video diffusion models have enabled
the generation of high-quality videos conditioned on textual prompts, achieving impressive visual fidelity and motion coherence [2–4, 23, 30]. Despite this progress, existing
models are optimized for single-event generation and offer no mechanism for explicit temporal control - users cannot specify when an event occurs, how long it persists for
and how multiple events are ordered. As a result, modeling
movie-grade videos composed of a succession of events, actions, or camera motions, each occurring within a specific
segment of the video and in a specific order, remains challenging. This limitation stems from the lack of temporal
awareness in the cross-attention mechanism: by conditioning every frame of the video on the entire prompt simultaneously, the model treats a multi-event prompt as global context rather than a temporally structured sequence, causing
semantic concepts intended for different moments to bleed
into one another, degrading text-video alignment.

Recent works have begun to address temporal controllability in video generation [10, 21, 27–29, 31]. One line
of work [27, 29] finetunes the backbone model with temporally grounded supervision. However, these methods require large amounts of annotated data, training and shifts
the pre-trained model’s distribution. Inference-time attention control methods [10, 28, 31] avoid training altogether,
but impose structural constraints on the attention mechanism that limit their generality and can introduce visual artifacts at segment boundaries.

In this paper, we propose Prompt Relay, a simple and
elegant attention-level routing mechanism for fine-grained
temporal control and multi-event video generation. Prompt
Relay operates entirely at inference time and is plug-andplay compatible with existing video diffusion backbones.



Prompt Relay requires no computational overhead and no
architectural modifications. Our main contributions are as
follows:

- We propose Prompt Relay, a test-time, plug-and-play
method for fine-grained temporal control in video generation with no computational overhead.

- We propose a Boundary-Attention decay mechanism,
a soft Gaussian penalty on cross-attention logits that
smoothly suppressess semantic interference across segment boundaries.

- We demonstrate that Prompt Relay substantially improves
temporal prompt alignment, reduces semantic interference and enhances visual quality.


**2. Related Works**


**2.1. Controllable Video Generation**


Video generation has seen rapid progress in recent years,
with applications spanning motion control [6, 9, 24–26],
viewpoint control [7, 15, 22], identity control [17, 18, 33]
and editing [8, 19]. However, most models remain limited
in the ability to generate coherent multi-event videos. Because the attention mechanism allows every pixel to attend
to every prompt token, models struggle to associate semantic concepts with their intended temporal intervals, leading
to temporal misalignment and semantic entanglement. This
challenge motivates us to provide explicit temporal control
at inference time.


**2.2. Attention-Based Control in Diffusion Models**


Attention manipulation has emerged as a key mechanism
for controllable diffusion generation. Prior work has explored attention for spatial [12–14, 16, 32], identity [11, 34]
and motion control [19, 20, 24]. In contrast, attention-based
temporal control remains largely underexplored.


**2.3. Multi-Event Video Generation**


A notable approach to temporal modeling for multi-event
video generation is MinT [27], which introduces a trainable
temporal cross-attention module that binds event descriptions to predefined time intervals, but requires additional
training, architectural modifications, and temporally annotated data. MEVG [21] generates each event clip sequentially, conditioning on the last frame of the previous clip
via latent inversion to maintain visual continuity. However,
this autoregressive design causes error accumulation across
segments and produces abrupt transitions when consecutive events are semantically dissimilar. DiTCtrl [10] proposes mask-guided KV-sharing within MM-DiT’s 3D fullattention, enabling prompt-specific semantic control without training. However, the binary attention masks derived
from the attention map introduce hard boundaries that can
cause background inconsistencies and unnatural transitions.
TS-Attn [31] and SwitchCraft [28] instead modulate crossattention by identifying motion-relevant tokens, TS-Attn
via a subject semantic layout, and SwitchCraft via eventspecific anchor tokens. Both methods therefore assume the
presence of a dominant foreground subject in each event and
struggle with scene-level changes or events where no single
entity dominates the frame.


**3. Prompt Relay**


Given a sequence of temporally-constrained text prompts
_{_ ( _ps, t_ [start] _s_ _, t_ [end] _s_ [)] _[}]_ _s_ _[N]_ =1 [,] [our] [goal] [is] [to] [generate] [a] [video] [such]
that each arbitrary prompt _ps_ is realized within its designated temporal interval [ _t_ [start] _s_ _, t_ [end] _s_ []][.] The generated video
should preserve global coherence while ensuring that each
prompt influences only its assigned temporal region.


**3.1. Preliminaries**


Cross-attention is a mechanism that enables a diffusion
model to incorporate external conditioning information,
such as text prompts, into the generation process. Given
a latent representation at diffusion step _t_, denoted as _ϕ_ ( _zt_ ),
and a set of conditioning embeddings _ψ_ ( _P_ ) derived from
an input prompt _P_, cross-attention computes interactions
between the two through learned projections.




         - _QK_ _⊤_
Attn( _ϕ_ ( _zt_ ) _, ψ_ ( _P_ )) = Softmax ~~_√_~~

_d_




_V,_ (1)



Figure 3. **Ablation** **Study** **of** **the** **Temporal** **Penalty** **Function.**
The curves show the attention fraction retained between a query
token and the prompt tokens of a given segment, as a function of
the query’s latent frame offset from that segment’s midpoint _ms_,
after applying the penalty exp( _−C_ ( _i, j_ )). (Top) Effect of the window parameter _w_ . _w_ = _L −_ 2 preserves full attention within the
segment and only suppresses attention near the segment boundaries. (Bottom) Effect of the decay threshold _ϵ_ . Smaller values
enforce stronger attenuation outside the ’free-attention’ window;
however, we find that the choice among small values has negligible perceptual impact. We adopt _ϵ_ = 0 _._ 1 as our default.


queries to respond to different aspects of the prompt. However, because attention is computed globally over all conditioning tokens, multiple semantic concepts may compete
for influence over the same latent queries. When these concepts correspond to different temporal regions, unrestricted
attention can lead to interference between instructions.


**3.2. Temporal Prompt Routing**


In order to enforce the association between each prompt _ps_
and its assigned temporal interval [ _t_ [start] _s_ _, t_ [end] _s_ []][,] [we introduce]
a penalty term _C_ ( _Q, K_ ) into the cross-attention logits:


         - _QK_ _⊤_          Attn( _ϕ_ ( _zt_ ) _, ψ_ ( _P_ )) = softmax ~~_√_~~ _−_ _C_ ( _Q, K_ ) _V._

_d_

(2)
The role of _C_ ( _Q, K_ ) is to suppress the attention between
key and query tokens whenever they do not belong to the
same interval [ _t_ [start] _s_ _, t_ [end] _s_ []][.] [This allows each prompt to guide]
generation only within its intended segment, without leak


where _Q_ = _ℓQϕ_ ( _zt_ ) are query vectors derived from latent
features, _K_ = _ℓKψ_ ( _P_ ) and _V_ = _ℓV ψ_ ( _P_ ) are key and
value vectors projected from the conditioning embeddings,
and _d_ denotes the projection dimensionality. Each attention
weight reflects how strongly a latent query attends to a particular conditioning token. Through this operation, semantic information from the conditioning input is selectively
injected into the latent representation, allowing different


A man eats pasta at a restaurant table → A woman in a red dress and sunglasses walks past


Hard Masking


Boundary-Attention

Decay (Ours)


Figure 4. **Hard Masking vs Boundary-Attention Decay.** Hard masking enforces an abrupt semantic switch in cross-attention at segment
boundaries while self-attention remains continuous across the segments. This creates a discontinuity at the boundary, forcing the model
to reconcile conflicting signals (Woman eats the pasta instead of the man). Boundary-attention decay avoids this conflict by smoothly coactivating both neighboring prompts near the boundary, giving the model a gradual handoff region in which the transition can be planned
jointly before being committed to in the visual representation.



ing semantic concepts into other parts of the video. For any
arbitrary query token indexed by _i_ and any key token j belonging to _ps_, the penalty is defined as:


_C_ ( _i, j_ ) = [ReLU(] _[|][f]_ [(] _[i]_ [)] _[ −]_ _[m][s][| −]_ _[w]_ [)][2] _,_

2 _σ_ [2]

_ms_ = _[t]_ _s_ [start] + _t_ [end] _s_ _._ (3)
2


Here, _f_ ( _i_ ) denotes the latent frame index associated with
query token i, and _ms_ denotes the midpoint of the corresponding temporal segment. The parameter _w_ defines a local window around the segment midpoint within which no
penalty is applied, while _σ_ controls the rate at which attention decays outside this window. Query tokens within
the window incur zero penalty and can attend freely to their
associated prompt tokens. Beyond this region, attention is
smoothly attenuated as a function of the temporal distance
between the query and the segment midpoint. We demonstrate in Fig. 3, that _w_ = _L −_ 2 achieves the best balance
between temporal isolation and intra-segment fidelity.
We compare our approach to hard masking in Fig. 4.
Hard masking sets _C_ ( _i, j_ ) = _−∞_ for all query-key pairs
where _f_ ( _i_ ) _∈/_ [ _t_ [start] _s_ _, t_ [end] _s_ []] [and] _[j]_ [belongs] [to] [prompt] _[p][s]_
(i.e. a query either attends fully to a prompt or is completely blocked from it). This enforces a sudden switch
between prompts at segment boundaries. While hard
masking eliminates cross-segment semantic interference,
it creates a discontinuity at the boundary: cross-attention
switches abruptly to the new prompt while self-attention
remains anchored to the previous segment’s visual structure, forcing the model to reconcile conflicting signals.
Boundary-attention decay avoids this conflict by smoothly
co-activating both neighboring prompts near the boundary,
giving the model a gradual handoff region in which the transition can be planned jointly before being committed to in
the visual representation.



**3.3. Boundary-Attention Decay**


To suppress semantic interference across temporal segments, attention between queries near segment boundaries
and prompt tokens from neighboring segments should be
negligible. We therefore choose the decay parameter _σ_ so
that the attention prior sufficiently decreases near segment
endpoints. Since our penalty subtracts _C_ ( _i, j_ ) from the logits, it applies a multiplicative factor exp� _−_ _C_ ( _i, j_ )� to the
unnormalized attention scores before softmax. This prior
is 1 inside the “free-attention” window and decays toward
the segment boundaries. Let the endpoint distance from the
segment midpoint be _L_ = _|f_ ( _i_ ) _−_ _ms|_ . We choose _σ_ such
that the prior reaches a small value _ϵ_ at the endpoints:



This formulation ensures smooth transitions between neighboring prompts while preventing destructive interference
across segments. As a result, each textual instruction primarily influences its intended temporal region, allowing the
model to focus on one semantic concept at a time while
maintaining global temporal coherence.


**4. Experiments**


**4.1. Experimental Setup**


We apply Prompt Relay on top of the state-of-the-art pretrained video generation model Wan2.2-T2V-A14B. To
demonstrate the limitations of existing video generators in
handling multi-event prompts, we test several other models,
including Sora Storyboard [3], Veo 3.1[4], Wan 2.2[5], and
Kling 2.6[2]. We set _ϵ_ = 0 _._ 1 across all experiments. Setting
_w_ = _L−_ 2 reduces _σ_ to a constant. In addition to selectively
routing local prompts to their assigned temporal segments,
we include a global prompt that conditions the entire video
and provides persistent context.




 exp _−_ [(] _[L][ −]_ _[w]_ [)][2]

2 _σ_ [2]




- _L −_ _w_
= _ϵ_ _⇒_ _σ_ = _._ (4)
�2 ln(1 _/ϵ_ )


Sora
(Storyboard)


Kling 2.6


Veo 3.1


Wan 2.2


Wan 2.2 +
Prompt Relay

(Ours)


**Prompt** : A handheld, front-facing, selfie perspective of a man filming himself at arm ’ s length ... The man … standing on a
busy street in Hong Kong. Neon signs glow behind him, skyscrapers loom overhead, and crowds move in the background ...
The man raises his hand toward the camera. His palm moves closer until his hand completely fills the frame … The hand
pulls away from the lens, revealing the man in the same framing but now is filming himself in the grand canyons.


Figure 5. **Qualitative Comparison.** Given a multi-event prompt describing a deliberate scene transition, Prompt Relay preserves correct
temporal structure, ensuring that each semantic instruction influences only its intended segment while maintaining global visual coherence.



**4.2. Evaluation Metrics**


Existing quantitative metrics test visual fidelity or global
text-video alignment, but fail to capture temporal semantics
or transition quality, properties that are inherently perceptual. Hence, we conduct a human preference study to evaluate multi-event video generation along three dimensions:

- **Temporal Prompt Alignment:** Whether each prompt is
realized in its intended temporal interval.

- **Transition** **Naturalness:** The perceptual smoothness of
transitions between consecutive events, including the absence of abrupt cuts, flickering, or unnatural morphing at
segment boundaries.

- **Visual** **Quality:** Overall perceptual fidelity of the generated video, including sharpness, temporal consistency,
and absence of visual artifacts.

We construct 20 diverse multi-event test scenarios, covering a wide range of settings including explicit scene tran


sitions, multi-character interactions, and complex camera
trajectories, randomly generated with ChatGPT [1]. These
scenarios each contain 3-6 temporal events. Participants
were shown videos alongside their corresponding prompt,
with model identity withheld, and asked to rank each video
on a scale of 1–5 per criterion. Final scores are computed as
the average rank across all participants (30) and scenarios.


**4.3. Results**


As shown in Table. 1, Prompt Relay consistently outperforms baseline approaches in temporal alignment and transition naturalness. Notably Wan 2.2 with Prompt Relay consistently exhibits stronger visual quality compared to the
baseline Wan 2.2. This is likely because Prompt Relay’s
attention routing mechanism suppresses attention between
queries in a particular temporal segment and prompts belonging to other segments. By reducing unnecessary com

**Metric** **Storyboard** **Kling 2.6** **Veo 3.1** **Wan 2.2** **Wan 2.2 + Prompt Relay**


Temporal Prompt Alignment ( _↓_ ) 4.67 1.30 3.93 4.00 **1.10**
Transition Naturalness ( _↓_ ) 4.60 4.43 1.30 3.50 **1.17**
Visual Quality ( _↓_ ) 3.67 2.50 **2.0** 4.00 2.83


Table 1. Human preference scores for multi-event video generation. (lower values indicate better rankings)



petition in the cross-attention space, the model can allocate attention more effectively to the active semantic concepts, resulting in clearer visual structure, improved temporal alignment, and more stable generation. However, Kling
2.6 and Veo 3.1 still achieve higher visual quality overall,
indicating that visual fidelity remains partially bounded by
the capacity of the underlying backbone model.


**5. Limitations**


Since each temporal segment attends primarily to its corresponding local prompt, persistent visual elements such as
characters, objects, or scene style are not explicitly shared
across segments. If these elements are described inconsistently across local prompts, their appearance may drift over
time. We found that we can fully mitigate this by incorporating a global prompt that provides shared context and
anchors persistent elements across multiple segments.


**6. Conclusion**


We present Prompt Relay, an inference-time, plug-and-play
method for multi-event video generation with fine-grained
temporal control. We also show that our method improves
visual quality over the backbone model. We view our work
as a pivotal step towards movie-grade, controllable video
synthesis.


**Acknowledgments**


This research is supported by cash and in-kind funding
from NTU S-Lab and industry partner(s). This study
is also supported by the Ministry of Education, Singapore, under its MOE AcRF Tier 2 (MOE-T2EP202230002).


**References**


[1] Chatgpt 5.2. Accessed January 15, 2026 [Online], 2025. 5

[2] Kling 2.6. Accessed January 15, 2026 [Online], 2025. 2, 4

[3] Sora. Accessed January 15, 2026 [Online] [https://](https://sora.chatgpt.com/explore)
[sora.chatgpt.com/explore, 2025.](https://sora.chatgpt.com/explore) 4

[4] Veo 3.1. Accessed January 15, 2026 [Online], 2025. 2, 4

[5] Wan 2.2. Accessed January 15, 2026 [Online], 2025. 4

[6] Rameen Abdal, Or Patashnik, Ivan Skorokhodov, Willi
Menapace, Aliaksandr Siarohin, Sergey Tulyakov, Daniel
Cohen-Or, and Kfir Aberman. Dynamic concepts personalization from single videos. In _Proceedings_ _of_ _the_ _Special_



_Interest Group on Computer Graphics and Interactive Tech-_
_niques Conference Conference Papers_, 2025. 2

[7] Jianhong Bai, Menghan Xia, Xiao Fu, Xintao Wang, Lianrui Mu, Jinwen Cao, Zuozhu Liu, Haoji Hu, Xiang Bai,
Pengfei Wan, et al. Recammaster: Camera-controlled
generative rendering from a single video. _arXiv_ _preprint_
_arXiv:2503.11647_, 2025. 2

[8] Yuxuan Bian, Zhaoyang Zhang, Xuan Ju, Mingdeng Cao,
Liangbin Xie, Ying Shan, and Qiang Xu. Videopainter: Anylength video inpainting and editing with plug-and-play context control. In _Proceedings of the Special Interest Group on_
_Computer_ _Graphics_ _and_ _Interactive_ _Techniques_ _Conference_
_Conference Papers_, 2025. 2

[9] Ryan Burgert, Yuancheng Xu, Wenqi Xian, Oliver Pilarski,
Pascal Clausen, Mingming He, Li Ma, Yitong Deng, Lingxiao Li, Mohsen Mousavi, et al. Go-with-the-flow: Motioncontrollable video diffusion models using real-time warped
noise. In _Proceedings_ _of_ _the_ _Computer_ _Vision_ _and_ _Pattern_
_Recognition Conference_, 2025. 2

[10] Minghong Cai, Xiaodong Cun, Xiaoyu Li, Wenze Liu,
Zhaoyang Zhang, Yong Zhang, Ying Shan, and Xiangyu
Yue. Ditctrl: Exploring attention control in multi-modal diffusion transformer for tuning-free multi-prompt longer video
generation. In _Proceedings of the Computer Vision and Pat-_
_tern Recognition Conference_, 2025. 2, 3

[11] Shengqu Cai, Ceyuan Yang, Lvmin Zhang, Yuwei Guo, Junfei Xiao, Ziyan Yang, Yinghao Xu, Zhenheng Yang, Alan
Yuille, Leonidas Guibas, et al. Mixture of contexts for long
video generation. _arXiv preprint arXiv:2508.21058_, 2025. 2

[12] Mingdeng Cao, Xintao Wang, Zhongang Qi, Ying Shan, Xiaohu Qie, and Yinqiang Zheng. Masactrl: Tuning-free mutual self-attention control for consistent image synthesis and
editing. In _Proceedings of the IEEE/CVF international con-_
_ference on computer vision_, 2023. 2

[13] Hila Chefer, Yuval Alaluf, Yael Vinker, Lior Wolf, and
Daniel Cohen-Or. Attend-and-excite: Attention-based semantic guidance for text-to-image diffusion models. _ACM_
_transactions on Graphics (TOG)_, 2023.

[14] Gordon Chen, Ziqi Huang, Cheston Tan, and Ziwei Liu.
Stencil: Subject-driven generation with context guidance. In
_2025_ _IEEE_ _International_ _Conference_ _on_ _Image_ _Processing_
_(ICIP)_ . IEEE, 2025. 2

[15] Hao He, Yinghao Xu, Yuwei Guo, Gordon Wetzstein, Bo
Dai, Hongsheng Li, and Ceyuan Yang. Cameractrl: Enabling
camera control for text-to-video generation. _arXiv_ _preprint_
_arXiv:2404.02101_, 2024. 2

[16] Amir Hertz, Ron Mokady, Jay Tenenbaum, Kfir Aberman,
Yael Pritch, and Daniel Cohen-Or. Prompt-to-prompt im

age editing with cross attention control. _arXiv_ _preprint_
_arXiv:2208.01626_, 2022. 2

[17] Teng Hu, Zhentao Yu, Zhengguang Zhou, Sen Liang, Yuan
Zhou, Qin Lin, and Qinglin Lu. Hunyuancustom: A
multimodal-driven architecture for customized video generation. _arXiv preprint arXiv:2505.04512_, 2025. 2

[18] Lijie Liu, Tianxiang Ma, Bingchuan Li, Zhuowei Chen, Jiawei Liu, Gen Li, Siyu Zhou, Qian He, and Xinglong Wu.
Phantom: Subject-consistent video generation via crossmodal alignment. _arXiv_ _preprint_ _arXiv:2502.11079_, 2025.
2

[19] Shaoteng Liu, Yuechen Zhang, Wenbo Li, Zhe Lin, and Jiaya
Jia. Video-p2p: Video editing with cross-attention control.
In _Proceedings_ _of_ _the_ _IEEE/CVF_ _Conference_ _on_ _Computer_
_Vision and Pattern Recognition_, 2024. 2

[20] Tuna Han Salih Meral, Hidir Yesiltepe, Connor Dunlop,
and Pinar Yanardag. Motionflow: Attention-driven motion transfer in video diffusion models. _arXiv_ _preprint_
_arXiv:2412.05275_, 2024. 2

[21] Gyeongrok Oh, Jaehwan Jeong, Sieun Kim, Wonmin Byeon,
Jinkyu Kim, Sungwoong Kim, and Sangpil Kim. Mevg:
Multi-event video generation with text-to-video models. In
_European_ _Conference_ _on_ _Computer_ _Vision_ . Springer, 2024.
2, 3

[22] Xuanchi Ren, Tianchang Shen, Jiahui Huang, Huan Ling,
Yifan Lu, Merlin Nimier-David, Thomas M¨uller, Alexander Keller, Sanja Fidler, and Jun Gao. Gen3c: 3d-informed
world-consistent video generation with precise camera control. In _Proceedings_ _of_ _the_ _Computer_ _Vision_ _and_ _Pattern_
_Recognition Conference_, 2025. 2

[23] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao,
Chen-Wei Xie, Di Chen, Feiwu Yu, Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video
generative models. _arXiv preprint arXiv:2503.20314_, 2025.
2

[24] Luozhou Wang, Ziyang Mai, Guibao Shen, Yixun Liang, Xin
Tao, Pengfei Wan, Di Zhang, Yijun Li, and Ying-Cong Chen.
Motion inversion for video customization. In _Proceedings of_
_the Special Interest Group on Computer Graphics and Inter-_
_active Techniques Conference Conference Papers_, 2025. 2

[25] Xiang Wang, Hangjie Yuan, Shiwei Zhang, Dayou Chen, Jiuniu Wang, Yingya Zhang, Yujun Shen, Deli Zhao, and Jingren Zhou. Videocomposer: Compositional video synthesis
with motion controllability. _Advances in Neural Information_
_Processing Systems_, 2023.

[26] Zhouxia Wang, Ziyang Yuan, Xintao Wang, Yaowei Li,
Tianshui Chen, Menghan Xia, Ping Luo, and Ying Shan.
Motionctrl: A unified and flexible motion controller for
video generation. In _ACM SIGGRAPH 2024 Conference Pa-_
_pers_, 2024. 2

[27] Ziyi Wu, Aliaksandr Siarohin, Willi Menapace, Ivan Skorokhodov, Yuwei Fang, Varnith Chordia, Igor Gilitschenski,
and Sergey Tulyakov. Mind the time: Temporally-controlled
multi-event video generation. In _Proceedings_ _of_ _the_ _Com-_
_puter_ _Vision_ _and_ _Pattern_ _Recognition_ _Conference_, 2025. 2,
3

[28] Qianxun Xu, Chenxi Song, Yujun Cai, and Chi Zhang.
Switchcraft: Training-free multi-event video generation with



attention controls. _arXiv_ _preprint_ _arXiv:2602.23956_, 2026.
2, 3

[29] Shuai Yang, Wei Huang, Ruihang Chu, Yicheng Xiao,
Yuyang Zhao, Xianbang Wang, Muyang Li, Enze Xie, Yingcong Chen, Yao Lu, et al. Longlive: Real-time interactive
long video generation. _arXiv_ _preprint_ _arXiv:2509.22622_,
2025. 2

[30] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu
Huang, Jiazheng Xu, Yuanming Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. Cogvideox: Text-to-video
diffusion models with an expert transformer. _arXiv preprint_
_arXiv:2408.06072_, 2024. 2

[31] Hongyu Zhang, Yufan Deng, Zilin Pan, Peng-Tao Jiang, Bo
Li, Qibin Hou, Zhiyang Dou, Zhen Dong, and Daquan Zhou.
TS-attn: Temporal-wise separable attention for multi-event
video generation. In _The_ _Fourteenth_ _International_ _Confer-_
_ence on Learning Representations_, 2026. 2, 3

[32] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala. Adding
conditional control to text-to-image diffusion models. In
_Proceedings_ _of_ _the_ _IEEE/CVF_ _international_ _conference_ _on_
_computer vision_, 2023. 2

[33] Yong Zhong, Zhuoyi Yang, Jiayan Teng, Xiaotao Gu,
and Chongxuan Li. Concat-id: Towards universal identity-preserving video synthesis. _arXiv_ _preprint_
_arXiv:2503.14151_, 2025. 2

[34] Yupeng Zhou, Daquan Zhou, Ming-Ming Cheng, Jiashi
Feng, and Qibin Hou. Storydiffusion: Consistent selfattention for long-range image and video generation. _Ad-_
_vances in Neural Information Processing Systems_, 2024. 2


