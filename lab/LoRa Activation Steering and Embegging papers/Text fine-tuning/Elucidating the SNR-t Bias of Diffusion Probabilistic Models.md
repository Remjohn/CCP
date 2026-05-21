## **Elucidating the SNR-t Bias of Diffusion Probabilistic Models**

Meng Yu [1] _[,]_ [2][*], Lei Sun [2][†], Jianhao Zeng [2], Xiangxiang Chu [2], Kun Zhan [1][‡]

1Lanzhou University, 2AMAP Alibaba Group



**Abstract**


_Diffusion Probabilistic Models have demonstrated remark-_
_able performance across a wide range of generative tasks._
_However, we have observed that these models often suffer_
_from_ _a_ _Signal-to-Noise_ _Ratio-timestep_ _(SNR-t)_ _bias._ _This_
_bias refers to the misalignment between the SNR of the de-_
_noising sample and its corresponding timestep during the_
_inference phase._ _Specifically, during training, the SNR of a_
_sample is strictly coupled with its timestep._ _However, this_
_correspondence_ _is_ _disrupted_ _during_ _inference,_ _leading_ _to_
_error_ _accumulation_ _and_ _impairing_ _the_ _generation_ _quality._
_We provide comprehensive empirical evidence and theoreti-_
_cal analysis to substantiate this phenomenon and propose a_
_simple yet effective differential correction method to mitigate_
_the SNR-t bias._ _Recognizing that diffusion models typically_
_reconstruct low-frequency components before focusing on_
_high-frequency details during the reverse denoising process,_
_we decompose samples into various frequency components_
_and_ _apply_ _differential_ _correction_ _to_ _each_ _component_ _indi-_
_vidually._ _Extensive_ _experiments_ _show_ _that_ _our_ _approach_
_significantly improves the generation quality of various dif-_
_fusion models (IDDPM, ADM, DDIM, A-DPM, EA-DPM,_
_EDM, PFGM++, and FLUX) on datasets of various resolu-_
_tions with negligible computational overhead._ _The code is_
_at https://github.com/AMAP-ML/DCW._


**1. Introduction**


Due to their outstanding performance, Diffusion Probabilistic Models (DPMs) [17, 48, 51] have achieved remarkable
success in various generative tasks, including image [11, 45],
audio [6, 21], and video [4, 19, 68] generation. DPMs typically consist of two processes. In the forward process, a
data sample is progressively perturbed by Gaussian noise
until it becomes the standard Gaussian noise. In the reverse
process, DPMs iteratively denoise from the standard Gaussian noise to generate the clean data sample. Despite their
significant success, we identify that DPMs suffer severely


*Work done during the internship at AMAP Alibaba Group.
†Project leader.
‡Corresponding author. Email: kzhan@lzu.edu.cn



from a Signal-to-Noise Ratio–timestep (SNR-t) bias.


The SNR-t bias refers to the misalignment between the
SNR of predicted samples and their assigned timesteps during inference. Specifically, during training, the neural network is conditioned on both the perturbed sample and the
corresponding timestep, establishing a deterministic correspondence between the SNR of the sample and the timestep.
However, during inference, due to cumulative errors arising
from both the model’s predictions [20] and the numerical
solvers [31, 51], the denoising trajectory inevitably deviates
from the ideal path, causing a misalignment between the
SNR of the predicted sample and its designated timestep,
as shown in Fig. 1a. Unlike previously studied exposure
bias [38], which focuses on inter-sample discrepancies, the
SNR-t bias emphasizes the misalignment between the predicted sample and its corresponding timestep. We argue that
the SNR-t bias is a more fundamental bias that can induce
exposure bias and is prevalent in current DPMs.


We provide a comprehensive experimental analysis and
theoretical justification for SNR-t bias. Our experiments
reveal two key findings: (1) the network demonstrates significantly inaccurate predictions when processing samples with
mismatched SNR and timesteps. Specifically, as illustrated
in Fig. 1b, samples with lower SNR tend to make the network
produce larger noise predictions, while those with higher
SNR yield smaller noise predictions. (2) Reverse denoising
samples often exhibit lower SNR compared to their corresponding forward samples at the same timestep, as shown
in Fig. 1c. These findings lead to a notable conclusion: the
SNR-t bias severely degrades the model performance and
often manifests as lower SNR for the corresponding timestep
during the denoising process. To investigate the underlying
mechanisms, we analyze the reverse process of DPMs and
provide a theoretical proof of this bias, thereby offering a
robust theoretical justification for our findings.


To mitigate the SNR-t bias, a natural solution is to align
the distribution of reverse samples, which tends to have
lower SNR, with the corresponding distribution of forward
samples. Given the complexity of existing DPM frameworks,
training or fine-tuning approaches would incur significant
costs. Instead, we propose a dynamic differential correction
method in the wavelet domain, which leverages the model’s


60

50

40

30

20

10



|Col1|||ϵ<br>ϵ|θ(x10,<br>(x,|10)||2<br>16)|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**||**|**θ16**|**||2**||||||||||
||**||**|**θ16**|**||2**||||||||||
|||||||||||~~s =~~<br>s =|~~ 0 ~~<br> 16||
||||||||||||||
||||||||||||||
||||||||||||||


0 2 4 6 8 10 12 14 16 18
t



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||~~orw~~<br>ever|~~rd~~<br>e||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||


0 2 4 6 8 10 12 14 16 18
t



54
51
48
45
42
39
36



Train Inference

(a) Schematic of SNR-t bias in DPMs.



(b) SNR-t bias causes inaccurate predictions.



(c) The reverse process exhibits lower SNR.



Figure 1. (a) During training, the SNR of perturbed sample _**x**_ _t_ is strictly tied to timestep _t_ . However, during inference, due to network
prediction errors and discretization errors in numerical solvers, the SNR of predicted sample _**x**_ **ˆ** _t_ no longer matches the preset timestep _t_ . (b)
shows the network output _||_ _**ϵθ**_ ( _**x**_ _t, s_ ) _||_ 2 when a trained network _**ϵθ**_ ( _·, s_ ) with fixed timestep _s_ receives samples _**x**_ _t_ with mismatched SNR
(samples are generated via forward process using Eq. 2 with different _t_ ). (c) shows the network output _||_ _**ϵθ**_ ( _·, t_ ) _||_ 2 using forward samples
and reverse predicted samples, respectively. _||_ _**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ) _||_ 2 is always larger than _||_ _**ϵθ**_ ( _**x**_ _t, t_ ) _||_ 2, which indicates that predicted samples exhibit
lower SNR compared to forward samples at the same timestep. See the experiment details of (b) and (c) in Sec. 4.



inherent capabilities to alleviate the bias without additional
training. Specifically, at each denoising step, we obtain
the reconstruction sample, which directly predicts the clean
sample from the current predicted sample. By analytically
modeling the prediction distribution and the reconstruction
distribution, we find that their difference signal contains
gradient information that can guide the biased predicted
sample toward the ideal perturbed sample. We incorporate
this differential signal into each denoising step to ensure the
predicted distribution aligns more closely with the perturbed
distribution, thereby effectively mitigating the bias.
Additionally, to improve the correction effect, we introduce the method into the wavelet domain, allowing it to
correct different frequency components of samples separately. This approach leverages the unique denoising characteristics [42, 61] of DPMs, which initially emphasize the
reconstruction of low-frequency contours during the reverse
process before focusing on restoring high-frequency details.
Meanwhile, we assign dynamic weight coefficients to the
correction operations for different components. By applying
targeted corrections for varying frequency components at
different stages of the denoising process, we achieve significant improvements in corrections and overall performance.
Notably, our method can further enhance the performance
of improved models [38, 39, 64] for exposure bias, which
highlights the significance and superiority of our proposed
problem and method. In summary, our contributions are:


- We identify the SNR-t bias in DPMs and provide comprehensive experimental analysis and theoretical proof.

- We propose a dynamic differential correction method in
wavelet domain to effectively alleviate the SNR-t bias.

- Our method is training-free and plug-and-play, effectively
improving the generation quality of various DPMs. It
can also be extended to other bias-correction models with
significant gains and negligible computation.



**2. Related Work**


This section first reviews the development of DPMs, followed by some recent works on bias analysis in DPMs.


The foundational theory of DPMs is introduced by
DPM [48], with major advances brought by DDPM [17].
ADM [11] employs classifier guidance to make DPMs outperform GANs [13], while EDM [18] systematically explores the training and inference design space to further
boost generation quality and efficiency of DPMs. Notably, ODE-based DPMs [12, 31, 67, 69], knowledge
distillation-based DPMs [28, 32, 34, 47], and consistency
models [24, 30, 50, 52] are widely studied. Meanwhile,
DPMs have advanced downstream tasks like text-to-image
models [3, 7, 23, 45], image editing [10, 33, 40], and superresolution generation [15, 25, 46]. Furthermore, USP [9],
SY-TDM [35], FE2E [56], S [2] -Guidance [5], and ADECOT [43] improve DPMs from different perspectives.


Research on exposure bias is closely related to our work.
Exposure bias in DPMs refers to the sample mismatch between training and sampling. ADM-IP [38] re-perturbs training data to imitate the discrepancies in inference, exposing
the model to possible prediction errors. MDSS [44] interprets exposure bias as deviations between predicted samples
and network outputs and adopts a multi-step denoising schedule to reduce it. EP-DDPM [27] derives an upper bound on
accumulated errors and incorporates it as a retraining regularizer to lessen the bias. While these models require retraining,
TS-DPM [26] and ADM-ES [39] offer training-free, plugand-play alternatives. In addition, MCDO [60], DPM-AT

[66], DPM-AE [57], BMGDM [63], and DPM-FR [64] also
analyze and mitigate this bias from different perspectives.


Exposure bias acts across samples, whereas SNR-t bias
arises between samples and timesteps.


**3. Background**


In this section, we review the preliminaries of DPMs.
DPMs generally comprise a forward process and a reverse
process, with both formulated as Markov chains. Given a
target data distribution _q_ ( _**x**_ 0) and a variance schedule _βt_, the
forward process is defined as



_**q**_ (\ _x_ _**_**_ {1 :



_T_
} _ _**0**_ _)=_ _**\**_ _pr_ od (1)


_|_ \x



where _q_ ( _**x**_ _t|_ _**x**_ _t−_ 1) = _N_ ( _**x**_ _t_ ; _[√]_ 1 _−_ _βt_ _**x**_ _t−_ 1 _, βt_ _**I**_ ). Utilizing
the attributes of the Gaussian distribution, the perturbed
sample _**x**_ _t_ is directly expressed in a closed form as the conditional distribution _q_ ( _**x**_ _t|_ _**x**_ 0):



_q_
\ _[x]_ __t_ _**=**_ \ s



r _t_ _{\_ _**b**_ _ar_ (2)



where _αt_ = 1 _−βt_, _α_ ¯ _t_ = [�] _i_ _[t]_ =1 _[α][i]_ [, and] _**[ ϵ]**_ _[t]_ _[∼N]_ [(] **[0]** _[,]_ _**[ I]**_ [)][. Then,]
by applying Bayes’ theorem, the corresponding posterior
distribution can be expressed as:


_**q**_ _(\_ x _**_**_ _{t_ _**-**_ 1} | _\_ x _**_**_ _t_, _**\**_ _x_ _**_**_ 0) _=_ _m_ [\] _a_ _**t**_ h _c_ (3)


where



_f_

_d_ l _e_ { _\m_ _ra_ c _{_ _s_ \ _qr_ t

_}_ _{_ _ _t_ _**}**_ =\ { _\_ _a_ b _r_



_eta_
1 _}_ _\_ } _b_



_i_
_d_ l _e_ { _\m_
_\_ t



c _{_ _s_ \ _qr_ t _{\_ _l_ a _p_ h [a] _[_]_ [}] _[{][t]_ [-]

{ _\_ _a_ b _r_ 1 _}_ _\_ } _b_



**4. SNR-t Bias**


In this section, we present the specific definition of SNR-t
bias and elaborate on two key findings.
The DPM takes the perturbed sample _**x**_ _t_ and the timestep
_t_ as input during training, as shown in Fig. 1a, and the SNR
of _**x**_ _t_ is directly determined by the timestep _t_ :


\t _e_ x t _{SN_ R} _(_ _)_ t = (7)


Due to the forced binding between the SNR of samples
and timesteps during the training phase, the network _**ϵθ**_ ( _·, t_ )
is proficient in accurately predicting samples with a corresponding SNR( _t_ ). But what happens if the network _**ϵθ**_ ( _·, s_ )
receives a sample _**x**_ _t_ with a mismatched SNR( _t_ )?
To validate this, we design and conduct an experiment to
assess the network predictions using samples with the mismatched SNR. Specifically, we select the ADM [11] model
as our baseline model and utilize 2,000 samples from the
CIFAR-10 [22] dataset. We first fix the timestep as _s_ for
the network _**ϵθ**_ ( _·, s_ ) and then generate a series of forward
perturbed samples _{_ _**x**_ 0 _,_ _**x**_ 1 _, · · ·_ _,_ _**x**_ _t, · · ·_ _,_ _**x**_ _T }_ using Eq. 2.
These perturbed samples are subsequently fed into the network _**ϵθ**_ ( _·, s_ ), after which we compute their mean squared
norm and present the results in Fig. 1b.


**Key Finding 1.** _The network produces significantly inaccu-_
_rate predictions when processing samples with mismatched_
_SNR and timesteps._ As illustrated in Fig. 1b, this bias exhibits a specific pattern: for the fixed timestep _s_, when handling the input sample _**x**_ _t_ with a lower SNR, where _t_ _>_ _s_,
the network tends to overestimate the predicted output. In
contrast, when dealing with the sample _**x**_ _t_ with a higher
SNR, the predicted output is typically underestimated. In
summary, samples with lower SNR lead the network to produce larger noise predictions, while those with higher SNR
result in smaller noise predictions.
With the Key Finding 1 highlighting the significant performance degradation caused by SNR-t bias in DPMs, a natural
subsequent question arises: how does SNR-t bias exactly
manifest during the actual denoising process?
The inference process in DPMs can be understood as
a numerical solution to a Stochastic Differential Equation
(SDE) or an Ordinary Differential Equation (ODE), which
inevitably introduces discretization errors during numerical computations. Additionally, the neural network within
DPMs is subject to inherent prediction errors. Consequently,
these two types of errors can cause the reverse denoising trajectory to deviate from the ideal path, resulting in a mismatch
between the actual SNR of the reverse predicted samples
_**x**_ ˆ _t_ and the designated timestep _t_ . Thus, the actual reverse
denoising process can be expressed as:



A neural network _p_ _**θ**_ ( _**x**_ _t−_ 1 _|_ _**x**_ _t_ ) = _N_ ( _**x**_ _t−_ 1; _µ_ _**θ**_ ( _**x**_ _t, t_ ) _, σt_ _**I**_ )
is employed to approximate _q_ ( _**x**_ _t−_ 1 _|_ _**x**_ _t,_ _**x**_ 0), which aims
to minimize _D_ KL( _q_ ( _**x**_ _t−_ 1 _|_ _**x**_ _t,_ _**x**_ 0) _∥p_ _**θ**_ ( _**x**_ _t−_ 1 _|_ _**x**_ _t_ )). Through
reparameterization, we are able to obtain:



_x_

_l_ a _ig_ n _ed_ ___ t, _t_ ) _&=_ \

_**_**_ [{] _**\**_ [T] _**[h]**_ _[e][ }]_ [( \]
} _m_ \ f _r_ _c_ a



_{_
_l_ a _ig_ n _ed_
\ _**b**_ _eg i_ n



_**{**_ _\_
f _r_ _c_ a



q
s ~~_r_~~
_t_



{ _**\**_ _b a_ ~~_a_~~ [r] _[{][\]_ _**}_**_ { _**t**_ _-1 }_ }\ _b_
l _p_ _a_ h



(4)
where _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ represents the reconstruction of] _**[ x]**_ [0][ given] _**[ x]**_ _[t]_ [,]
and _**ϵθ**_ ( _·_ ) denotes the noise prediction network. Specifically,
the relationship between the two is:

_[(]_ [\] _[ x]_ _[_][t]_ _**[,][t]**_ [)] _**[=]**_ _[\][f r]_ [a]
_**\**_ [x] _[^][0 _]_ [\ T] _**[h]**_ _[e]_ ~~_c_~~ _x_ (5)
_{\_


Finally, we obtain the concise training objective:


\math c a _l_ _**{**_ L _}_ _**_**_ _{\m_ a **t** _h_ _**r**_ m _{_ _**si**_ m _**p**_ _le }_ } _**=**_ _\m_ [a] th _b_ (6)


Once the noise prediction network is trained to convergence,
we can start from a standard Gaussian noise, perform stepby-step iterative denoising via _p_ _**θ**_ ( _**x**_ _t−_ 1 _|_ _**x**_ _t_ ), and ultimately
generate the clean data sample.



_\h_ a t ~~_{_~~
_\x_



r
_**_**_ } _{ t_ ~~_=_~~ [-] _[ 1][ }]_ _**c**_ {1 _**}**_ _{\ s_ q t _{_ _**\**_ _a_ (8)
_\_ _r_ f _a_


To further investigate the manifestations of SNR-t bias,
we adopt the same experimental setup as in Fig. 1b and
conduct the following comparative experiment. (1) We generate perturbed samples _{_ _**x**_ 1 _,_ _**x**_ 2 _, . . .,_ _**x**_ _T }_ via Eq. 2, and
feed _**x**_ _t_ and timestep _t_ into the network to obtain _**ϵθ**_ ( _**x**_ _t, t_ ).
(2) Then, we initialize 2,000 samples of standard Gaussian
noise and perform iterative denoising via Eq. 8 to obtain samples _{_ _**x**_ **ˆ** 1 _,_ **ˆ** _**x**_ 2 _, . . .,_ **ˆ** _**x**_ _T }_ and corresponding network outputs
_**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ). (3) Finally, we compute and plot the expectation of _ℓ_ 2 norms _||_ _**ϵθ**_ ( _**x**_ _t, t_ ) _||_ [2] 2 [and] _[ ||]_ _**[ϵ][θ]**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] _[||]_ 2 [2][, as shown]
in Fig. 1c. Particularly, similar experiments were also conducted in ADM-ES [39], and we provide the evidence of
the differences, together with more robust analyses in Appendix A. Building on this, we derive the second key finding:


**Key Finding 2.** _Reverse denoising samples often exhibit_
_lower SNR compared to their corresponding forward sam-_
_ples at the same timestep._ Fig. 1c shows that for any timestep
_t_, the mean _ℓ_ 2 norm of reverse predictions _**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ) consistently exceeds that of forward predictions _**ϵθ**_ ( _**x**_ _t, t_ ). The
Key Finding 1 shows that the network tends to produce an
overestimated output when processing samples with lower
SNR. Therefore, we have reason to conclude that the denoising sample _**x**_ **ˆ** _t_ generally maintains a lower SNR than the
forward perturbed sample _**x**_ _t_ at the same timestep, leading
to overestimated predictions at each denoising step.


**5. Method**


In this section, we first analytically model the reverse process
of DPMs and derive the analytical form of the SNR-t bias,
providing a comprehensive theoretical basis for this bias.
Then, based on the theoretical analysis, we propose a simple yet effective differential correction method to mitigate
the SNR-t bias, thereby improving the generation quality
of DPMs. Finally, by incorporating the denoising laws of
DPMs, we introduce differential correction into the wavelet
domain and design a specialized weighting strategy to further
enhance the correction effect.


**5.1. Theoretical Proof**


For the theoretical analysis of bias in DPMs, prior works
have proposed two distinct assumptions. ADM-ES [39] and
TS-DPM [26] propose the following formulation:


_**\**_ [x] _[^][0 _]_ [\ T] _**[ h]**_ [e] _[(][\]_ _**[x]**_ _[_]_ (9)


where _**ϵ**_ _t_ _∼N_ ( **0** _,_ _**I**_ ), with _ϕt_ a scalar coefficient. LADPM [65] and DPM-FR [64] propose another formulation:
_**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] [=] _[γ][t]_ _**[x]**_ [0][ +] _[ ϕ][t]_ _**[ϵ]**_ _[t]_ [, with] _[ γ][t]_ [also a scalar coefficient.]
Unfortunately, these prior assumptions are overly strong and
lack sufficient theoretical grounding and empirical validation.
Furthermore, there is a clear discrepancy in the coefficient
of _**x**_ 0 between the two hypotheses. To address this issue,



we conduct extensive theoretical and experimental analyses in this work, and ultimately decide to adopt the second
hypothesis for our subsequent analysis.


**Assumption 5.1.** _During both the forward and reverse pro-_
_cesses, the reconstruction sample_ _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] _[ can be expressed]_
_in terms of the original data_ _**x**_ 0 _as follows:_


_**\**_ [x ] _**[^]**_ _[0][_ \]_ [T h] _[ e]_ _**[(]**_ [\] [h] _[ a][t]_ _[{][\]_ (10)


_where_ 0 _<_ _γt_ ⩽ 1 _,_ _ϕt_ _<_ _M_ _,_ _and_ _M_ _denotes_ _a_ _uniform_
_upper bound constant across all timesteps._
_Sketch of Proof._ _**x**_ [0] _θ_ [(] _**[x]**_ _[t][, t]_ [)][ is the reconstruction output for]
predicting _**x**_ 0 given _**x**_ _t_, which is also known as the posterior
mean E[ _**x**_ 0 _|_ _**x**_ _t_ ] [54]. Based on Tweedie’s formula [54] and
the L2-norm loss function [18], DPMs tend to predict the
mean value of the target data. Thus, _**x**_ [0] _θ_ [can] [be] [viewed]
as the mean prediction _**x**_ ¯0 of _**x**_ 0. By the variance identity
E[ _∥_ _**x**_ 0 _∥_ [2] ] = _∥_ _**x**_ ¯0 _∥_ [2] + Var( _∥_ _**x**_ 0 _∥_ ) and the non-negativity of
variance, we get


_**\**_ | [\] b ar _**{**_ \ _x_ } ___


Since the expectation of a constant is itself, we can obtain:


_\m_ _**a**_ [t] _h_ _[bb]_ [{][ E][ }][[] _[|]_ _**[|]**_ [{] _[\]_ [x] _[}]_ (11)


The assumption _**x**_ [0] _θ_ [=] _**[x]**_ [0][ +] _[ ϕ][t]_ _**[ϵ]**_ _[t]_ [implies that][ E][[] _[||]_ _**[x]**_ [0] _θ_ _[||]_ [2][]] [=]
E[ _||_ _**x**_ 0 _||_ [2] ] + _ϕ_ [2] _t_ [.] [Obviously, this conflicts with Eq.][ 11][.] [Thus,]
a more accurate formulation is given in Eq. 10, where _γt_ _<_ 1
denotes energy and information loss during the reconstruction of _**x**_ 0. In particular, ASBGM [36] also provides indirect
evidence for this view. Furthermore, more theoretical and
experimental evidence is provided in Appendix B.
Based on Assumption 5.1, we can derive the analytical
form of the SNR for _**x**_ **ˆ** _t_ in the reverse process:


**Theorem 5.1.** _For a specific timestep t in the reverse de-_
_noising process of DPMs, the SNR of the biased denoising_
_sample_ _**x**_ **ˆ** _t is given by:_

_\_
\t _e_ x t _{N_ [S] _[}]_ [R] _[(][t]_ )= _\_ _a_ h _t_ { _a_ g _mma_ } _\b_ ar [{][\] _a_ (12)
^ _2_ _{_ _ _t_ }{


_where_ 0 _<_ _γ_ ˆ _t_ ⩽ 1 _and ϕt_ +1 _is derived from the reconstruc-_
_tion model_ _**x**_ [0] _**θ**_ [(ˆ] _**[x]**_ _[t]_ [+1] _[, t]_ [ + 1)] _[ in Eq.][ 10][.]_
_Sketch of Proof._ For the sake of brevity of the formula,
we present the denoising process from _**x**_ **ˆ** _t_ to _**x**_ **ˆ** _t−_ 1. By substituting the reconstruction model in Eq. 5 into the inverse
denoising Eq. 8, we can obtain:



_{\x_ _}__
_\h_ a t



qr _t_ _{\_ ov {

_**n**_ _e_
e _r_ _li_



_{_

_{\x_ _}__ _\s_ qr _t_ _{\_ ov

{ _t_ _-1_ _**}=**_ _**[\]**_ _[f][r a]_ [c ] e _r_ _li_



_a_ \ _l_ _**p**_ h _a_


(13)


Type SNR


_**x**_ _t_ Forward _α_ ¯ _t/_ (1 _−_ ~~_√_~~ _α_ ¯ _t_ )
_**x**_ **ˆ** _t_ Reverse _γ_ ˆ _t_ [2] _[α]_ [¯] _[t][/]_ �1 _−_ _α_ ¯ _t_ + ( 1 _−α_ ¯ _tα_ ¯ _βtt_ +1+1 _[ϕ][t]_ [+1][)][2][�]


Table 1. The actual SNR of _**x**_ _t_ and _**x**_ **ˆ** _t_ .





|Col1|Col2|Col3|
|---|---|---|
|**DWT**|||
|**DWT**|||


**iDWT**


**Pixel Space** **Wave Domain**


Figure 2. The overall framework of Differential Correction in
Wavelet domain (DCW). At each denoising step, DPMs always
generate the reconstructed sample _**x**_ [0] _**θ**_ [for predicting] _**[ x]**_ [0] [based on]
_**x**_ _t_ . After each denoising is completed, DCW maps _**x**_ [0] _**θ**_ [and] _**[ x]**_ _[t][−]_ [1]
to the wavelet domain via DWT to obtain _**x**_ _[f]_ _**θ**_ [and] _**[x]**_ _[f]_ _t−_ 1 [,] [where]
_f_ _∈{ll, lh, hl, hh}_ . Then, DCW corrects the different frequency
components of _**x**_ _t−_ 1 using Eq. 18. Finally, DCW maps the corrected _**x**_ _[f]_ _t−_ 1 [back to the pixel space via iDWT.]


where _**ϵ**_ 1 _∼N_ ( **0** _,_ _**I**_ ). Substituting Eqs. 10 and 2 into Eq. 13
yields the analytical form of _**x**_ ˆ _t−_ 1:



SNR of _**x**_ **ˆ** _t_ in the inverse process is always lower than that
of _**x**_ _t_ at the same timestep _t_ in the forward process. Thus,
we can infer that if we move the predicted sample toward
the perturbed sample, the SNR-t bias can be alleviated. Interestingly, this gradient information pushing _**x**_ **ˆ** _t_ toward _**x**_ _t_
is implicitly contained in each step of the denoising process.
Now, we focus on the differential signal between the predicted sample _**x**_ **ˆ** _t−_ 1 and the reconstructed sample _**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)]
in Eq. 14. Based on Eq. 15 for **ˆ** _**x**_ _t−_ 1 and Eq. 10 for _**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)][,]
the differential signal is expressed as:


_(\_
_\h_ x _**_**_ [{] _**t**_ [-] _**[}]**_ **[1]** _[- ]_ [\ x] _[_][{][\]_ [T][h] _**[e]**_ _[}]_ [^] _[0]_ _**t**_ }, t _)=_ _**\**_ _h_ (16)
_x_ h ___ {


   where _ηt_ = _ϕ_ [2] _t_ [+] _[ ψ]_ _t_ [2] _−_ 1 [.] [Obviously, the differential signal]
based on Eq. 16 contains directional information pointing to
_**x**_ _t−_ 1. Inspired by various directional information guidance
strategies [55, 65], we integrate this gradient information
into each step of denoising to guide the predicted samples
_**x**_ **ˆ** _t−_ 1 to move toward the ideal perturbed samples _**x**_ _t−_ 1:


_\h_ x _**{**_ **_** _t-_ 1 } _=_ _**h**_ **\** _x_ _ _{_ _**t**_ [-] _**1**_ [}] _**[+]**_ _[\ l]_ [am] _[b]_ (17)


where _λt_ is a scalar guidance factor that adjusts the magnitude of the effect of the differential signal. More specifically,
the difference guidance shifts the predicted sample toward
the noisy direction targeting _**x**_ _t−_ 1. When the parameter is
properly selected, it will improve the accuracy of the predicted sample to mitigate the SNR-t bias.
We emphasize that correcting _**x**_ **ˆ** _t−_ 1 is more advantageous
than correcting _**x**_ **ˆ** _t_, as it not only enhances the quality of generation more effectively but also incurs less computational
overhead. Specifically, Eq. 13 shows that the denoising result _**x**_ **ˆ** _t−_ 1 of the current step _t_ is jointly influenced by _**x**_ **ˆ** _t_
and _**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] [(or] _**[ϵ][θ]**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)][).] [Meanwhile,] [the] [acquisition]
of _**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] [indicates] [the] [network] [has] [completed] [predic-]
tion. Thus, without increasing Neural Function Evaluations
(NFE), Eq. 17 can correct _**x**_ **ˆ** _t−_ 1 and has no effect on the
network output. Additionally, correcting the denoising result
_**x**_ **ˆ** _t−_ 1 will bring gains to both the predicted sample and the
network output in the next denoising process.


**5.3. Differential Correction in Wavelet Domain**


In this subsection, we introduce the **D** ifferential **C** orrection
method into the **W** avelet domain **(DCW)**, as shown in Fig. 2,
which stems from two key motivations: (1) During inference,
DPMs first focus on reconstructing the low-frequency contours of images and then concentrate on the high-frequency
details [61]. Thus, our method should align with this important characteristic of DPMs; (2) The direction indicated
by the differential signal based on Eq. 16 is disturbed by
Gaussian noise _ηt_ _**ϵ**_ _t_, thus performing correction in the timefrequency domain helps reduce noise interference.
Specifically, during the denoising process, DCW employs
Discrete Wavelet Transform (DWT) [14] to decompose _**x**_ **ˆ** _t_



_}_
_\h_ a t _{\x_ _{_ _ _t-_ 1 _**}**_ =



~~_m_~~
a _a_ m _}_ _ _{t_
\ _h_ _t_ a _{_ \ g _qr_

       - _1_ _\_ } _s_



t
_**{**_ \ _b_



(14)
where _**ϵ**_ 2 _∼N_ ( **0** _,_ _**I**_ ). By substituting timestep _t_ + 1 into
Eq. 14, we can calculate the actual SNR of the predicted
sample _**x**_ **ˆ** _t_, thereby completing the proof of Theorem 5.1.
With the aid of the forward noising Eq. 2, a more concise
expression form is obtained:


_\b_ e g _n_ i _{_ a _**l**_ _ig_ n e _d}_ & _**\**_ h _a_ (15)


where _**ϵ**_ 3 _∼N_ ( **0** _,_ _**I**_ ), with more details in Appendix C.
Tab. 1 and Eq. 15 clearly show that the actual SNR of
the predicted samples _**x**_ **ˆ** _t_ in the reverse process is always
lower than that of the perturbed sample _**x**_ _t_ in the forward
process, thus there is always a SNR-t bias where the SNR of
predicted samples does not match the timestep _t_ during the
inference phase, which provides solid theoretical evidence
for the experimental conclusions in Sec. 4.


**5.2. Differential Correction in Pixel Space**


In Sec. 4 and Sec. 5.1, we clarify the SNR-t bias of DPMs
and its specific manifestations from both empirical and theoretical perspectives. Meanwhile, we find that the actual


and _**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] [into] [four] [frequency] [subbands.] [For] [a] [given]
image sample _**x**_ in the pixel space, after DWT is applied to
_**x**_, the following are obtained: _**x**_ _[ll]_, _**x**_ _[lh]_, _**x**_ _[hl]_, and _**x**_ _[hh]_, where
the size of all four subbands is R _[H/]_ [2] _[×][W/]_ [2] . _**x**_ _[ll]_ represents
the low-frequency subband, which characterizes the lowfrequency information of the image, such as the shape of
a human face or a house. _**x**_ _[lh]_ _,_ _**x**_ _[hl]_, and _**x**_ _[hh]_ correspond to
the high-frequency subbands in different directions, which
characterize the high-frequency information of the image,
such as the wrinkles of an elderly person or the veins of
leaves. Subsequently, we separately perform differential
correction on each type of frequency subband:


_[\]_ _hx_ [^] _**[_]**_ **[f]** _[{]_ _t-_ 1 [}] _[=]_ [\] _**[x]**_ **[h]** _^f_ _ _[{]_ _**[ t]**_ _**1**_ _[-]_ [}] _**[+]**_ _[\ l]_ [am] _[b]_ (18)


where _f_ _∈{ll, lh, hl, hh}_, _λ_ _[f]_ _t_ [is an adjustment coefficient]
related to both timesteps and frequency components. Then,
we utilize the inverse discrete wavelet transform (iDWT) [14]
to map the samples back to the pixel space, thereby forming
a complete DCW operation:


_\t_ i l de {\x _[}]_ __{_ t _[-][1]_ _[} ][= \ tex trm {][i]_ [DWT] (19)


Next, we discuss the adjustment strategy for _λ_ _[f]_ _t_ [.] [For the]
low-frequency component, we propose a time-dependent
weighting strategy that follows a decaying schedule as the
denoising advances. Conversely, a decreasing strategy is
adopted for the high-frequency components. Specifically, in
early denoising steps, we assign a relatively large coefficient
to the low-frequency correction term to prioritize the generation of low-frequency components, which also effectively
mitigates the interference of high-frequency noise errors during the initial denoising phase. In the later denoising stages,
we assign a larger coefficient to the high-frequency correction to focus on the restoration of high-frequency details,
which helps suppress the over-expression of low-frequency
components towards the end of the process.
Notably, the reverse process variance _σt_ in DPMs serves
as a robust indicator of the denoising progress and has been
widely adopted for dynamic modulation in various sampling
techniques [11, 53, 64]. Consequently, we leverage this
reverse variance to implement our dynamic correction. The
low-frequency component coefficient is formulated as:


_\_ [l] _[ a][m]_ _[b][ d][a]_ (20)


where _λl_ denotes a scalar coefficient. Similarly, the highfrequency component coefficient is defined as:


_\_ [l am] _[ b][ d][a]_ _[_][t][^]_ (21)


where _λh_ also denotes a scalar coefficient. Furthermore,
inspired by SG-Minority [53], more weight design strategies
are provided in Appendix D.



**6. Experiments**


In this section, we conduct extensive experiments on numerous datasets and DPMs to show the effectiveness, generality,
superiority, and robustness of our method.
We evaluate it on multiple representative DPM frameworks and samplers, including IDDPM [37], ADM [11],
DDIM [49], A-DPM [2], EA-DPM [1], EDM [18], DiT [41],
PFGM++ [59], FLUX [3], and Qwen-Image [58]. Then,
we choose DPM-AE [57] (ICLR 2025) and DPM-AT [66]
(ICLR 2025) as comparative models. Furthermore, we also
integrate our method into the open-source bias-corrected
models ADM-IP [38] (ICML 2023), ADM-ES [39] (ICLR
2024), and DPM-FR [64] (ACM MM 2025) to further
demonstrate the superiority of our approach. Meanwhile,
experiments are conducted across datasets of varying resolutions, including CIFAR-10 [22], CelebA 64 _×_ 64 [29],
ImageNet 128 _×_ 128 [8], and LSUN Bedroom 256 _×_ 256 [62].
Overall, we categorize our evaluations into two main
types: stochastic generation [17] and deterministic generation [49]. To comprehensively assess generation quality,
we employ standard metrics including Frechet´ Inception
Distance (FID) [16] and Recall [16], where FID serves as
the primary metric. All quantitative results are computed
over 50K generated samples with the full training set as
the reference distribution. For qualitative evaluation, we
visualize text-to-image results to intuitively demonstrate the
effectiveness of our method.


**6.1. Results on Classic Diffusion Models**


To verify the effectiveness and generality of the proposed
method, we select several classic diffusion models, namely
IDDPM, ADM, and ADM-IP. Additionally, we choose
datasets with different resolutions, including CIFAR-10 [22]
32 _×_ 32, CelebA 64 _×_ 64 [29], ImageNet 128 _×_ 128 [8],
and LSUN Bedroom 256 _×_ 256 [62]. Meanwhile, we select
FID and Recall as evaluation metrics to assess fidelity and
diversity, and use 20 and 50 as sampling steps.
Tab. 2 clearly shows that our method comprehensively
improves the generation quality of the baseline models across
all models and datasets. For example, on the CIFAR-10
dataset, DCW helps IDDPM reduce the FID score by 42 _._ 6%
and 25% in the 20-step and 50-step tasks, respectively.
For a fair comparison with recent methods on exposure
bias, we follow previous works and use the same baselines,
namely DDIM [49] sampler applied to A-DPM and ADM.
Tab. 3 clearly shows our method consistently outperforms
DPM-AE [57] (ICLR 2025) and DPM-AT [66] (ICLR 2025)
across all generation results, further validating its superiority.


**6.2. Results on Bias-Corrected Diffusion Models**


To verify the generality and advancement of our method, we
select several improved models for exposure bias as comparative models and integrate DCW into them, namely ADM

_T_ = 20 _T_ = 50


Model Dataset FID _↓_ Rec _↑_ FID _↓_ Rec _↑_


IDDPM CIFAR-10 32 13.19 0.50 5.55 0.56
**+Ours** CIFAR-10 32 **7.57** **0.56** **4.16** **0.58**


ADM-IP CelebA 64 11.95 0.42 4.52 0.55
**+Ours** CelebA 64 **10.41** **0.47** **4.34** **0.57**


ADM ImageNet 128 12.28 0.52 5.18 0.58
**+Ours** ImageNet 128 **10.34** **0.54** **4.52** **0.58**


IDDPM LSUN 256 18.69 0.27 8.42 0.41
**+Ours** LSUN 256 **11.03** **0.36** **5.24** **0.45**


Table 2. FID and Recall (Rec) on datasets with different resolutions.


DDIM ADM


Model 10 20 50 10 20 50


Base 14.40 6.87 4.15 22.62 10.52 4.55
Base-AE 13.98 6.76 4.10 - - Base-AT - - - 15.88 6.60 3.34


**Base+Ours** **9.36** **4.64** **3.33** **13.01** **5.59** **2.95**


Table 3. FID _↓_ on CIFAR-10 using ADM and DDIM.


ES [39] and DPM-FR [64]. Notably, DPM-FR is the SOTA
model for exposure bias. To be consistent with them, we divide the generation task into two categories: stochastic sampling and deterministic sampling. In stochastic sampling, we
select A-DPM [2] and NPR-DM in EA-DPM [1] as the baseline models. In deterministic sampling, we use EDM [18]
and PFGM++ [59] as baseline models and measure the sampling cost by Neural Function Evaluations (NFE) [55].
Tab. 4 shows that in stochastic sampling, DCW comprehensively improves the generation quality of baseline
models. For different models, noise scheduling strategies,
and time-step settings, DCW consistently achieves a significant reduction in the FID scores. For the corrected models,
even though they have already achieved extremely low FID
scores, DCW can still further reduce the FID results, which
demonstrates the advancement of our method.
Tab. 5 shows that in deterministic sampling, DCW can
not only improve the generation quality of baseline models
but also further reduce the FID of corrected models. For
EDM, DCW reduces the FID by 47 _._ 1%, 47 _._ 4%, and 36 _._ 4%
in the 13, 21, and 35 NFE generation tasks, respectively.
Although ADM-ES and ADM-FR have already improved
generation performance by alleviating exposure bias, DCW
can still further improve the corrected models. For EDM-ES
the reductions of FID under the three NFE tasks are 7 _._ 0%,
5 _._ 3%, and 3 _._ 5%, respectively. For PFGM-FR, the corresponding reductions are 6 _._ 6%, 5 _._ 7%, and 2 _._ 0%, respectively.



CIFAR-10 (LS) CIFAR-10 (CS)


Model 10 25 50 10 25 50


A-DPM 34.26 11.60 7.25 22.94 8.50 5.50
**+Ours** **17.56** **8.81** **5.38** **12.44** **5.99** **4.06**


A-DPM-FR 12.38 6.63 4.52 11.61 4.40 3.62
**+Ours** **10.91** **6.03** **4.44** **9.80** **4.33** **3.56**


NPR-DM 32.35 10.55 6.18 19.94 7.99 5.31
**+Ours** **16.60** **8.64** **5.40** **11.44** **6.38** **4.80**


NPR-DM-FR 10.86 5.76 4.19 10.18 4.07 3.44
**+Ours** **9.81** **5.30** **4.11** **8.46** **3.96** **3.33**


Table 4. FID _↓_ on CIFAR-10 using A-DPM and EA-DPM.


EDM PFGM++


Model 13 21 35 13 21 35


Base 10.66 5.91 3.74 12.92 6.53 3.88
**+Ours** **5.67** **3.37** **2.41** **6.98** **3.83** **2.64**


Base-ES 6.59 3.74 2.59 8.79 4.54 2.91
**+Ours** **6.13** **3.57** **2.50** **8.00** **4.41** **2.84**


Base-FR 4.68 2.84 2.13 6.62 3.67 2.53
**+Ours** **4.57** **2.79** **2.12** **6.18** **3.46** **2.48**


Table 5. FID _↓_ on CIFAR-10 using different fast samplers.


Meanwhile, we also provide the DiT [41] experiments on
the ImageNet 256 _×_ 256 dataset in Appendix E.


**6.3. Qualitative Comparison**


To intuitively demonstrate the impact of DCW on the generation quality, we set the same random seed and sampling
steps for the baseline models and improved models during
inference, ensuring that they follow similar denoising trajectories. Specifically, we adopt FLUX [3] as the baseline
model and use 10 sampling steps. As shown in Fig. 3, images generated by FLUX suffer from distortion issues such
as over-smoothing and overexposure. In contrast, DCW significantly mitigates these problems, substantially enhancing
the aesthetic quality and visual appeal of the generated images. More qualitative results are provided in Appendix F,
including the qualitative experiments on Qwen-Image [58].


**6.4. Ablation Study**


In this subsection, we conduct detailed ablation experiments
to examine the role of each component in DCW. We primarily use CIFAR-10 as the test dataset.
**Effect of the Wavelet Domain.** First, we investigate the
impact of each component in DCW on generation quality via
four comparative variants. Differential correction applied


7.0

6.7

6.4

6.1

5.8

5.5


|Col1|Col2|Col3|Col4|A-DP|M|Col7|Col8|
|---|---|---|---|---|---|---|---|
|||||||||
|||||||||


|Col1|Col2|Col3|A-DP|M|Col6|
|---|---|---|---|---|---|
|||||||
|||||||



λh



7.5


7.2


6.9


6.6


6.3



EA-DPM


λl





EA-DPM



(a) Search experiments of _λl_ .



(b) Search experiments of _λh_ .



Figure 3. Qualitative comparison between FLUX (first row) and
FLUX-DCW (second row) using 10 steps.


Model Type 10 25 50


A-DPM Baseline 22.94 8.50 5.50


A-DPM-DC Pixel Space 15.71 6.38 4.31
A-DPM-DH High Frequency 16.72 6.05 4.06
A-DPM-DL Low Frequency 13.21 7.00 5.10


**A-DPM-DCW** **High** & **Low** **12.46** **5.99** **4.06**


Table 6. Ablation study (FID _↓_ ) of different frequency components.


solely in the pixel space is denoted as “DC”. Then, we denote
differential correction applied only to high frequency or low
frequency wavelet components as “DH” and “DL”, respectively. Finally, our complete framework involves applying
differential correction to both the high frequency and low
frequency components, denoted as “DCW”. Tab. 6 clearly
shows that the differential correction method is effective
in both the pixel and wavelet space, resulting in noticeable
improvements in the generation quality. Furthermore, the
simultaneous integration of differential correction into both
high-frequency and low-frequency components enhances
performance even further, underscoring the necessity and advantages of applying the method within the wavelet domain.
**Sensitivity of Hyperparameter** _λf_ **.** Next, we examine
the sensitivity of DCW to hyperparameters. DCW is robust
to variations in hyperparameters: for both low-frequency and
high-frequency adjustment factors, the intensity of differential correction gradually increases with the growth of the
adjustment parameters, and the FID of the final generated
results exhibits a trend of first decreasing and then increasing, as shown in Fig. 4. Therefore, we can quickly determine
the optimal values of the hyperparameters through a simple
two-stage search method, as presented in Appendix G.
**Impact of DCW on computational overhead.** Finally,
we evaluate the impact of DCW on computational overhead. Without loss of generality, we fix the random seed,



Figure 4. Hyperparameter search experiments on CIFAR-10 (CS)
using A-DPM and EA-DPM with _T_ = 25.


Model Dataset Time DCW Time Overhead


ADM-IP CelebA 64 4.25 4.27 0 _._ 47%
ADM ImageNet 128 12.59 12.60 0 _._ 08%
IDDPM LSUN 256 15.57 15.61 0 _._ 26%


Table 7. Batch generation time on a single NVIDIA A6000 GPU.


the number of timesteps, and batch size, then conduct extensive experiments on datasets of varying resolutions: CelebA
64 _×_ 64, ImageNet 128 _×_ 128, and LSUN Bedroom 256 _×_ 256.
To address statistical bias, each experiment is repeated 100
times, and the average runtime is reported. Tab. 7 demonstrates that the computational cost incurred by DCW for
DPMs is negligible, introducing virtually no generation latency. Specifically, DCW adds an additional time overhead
of approximately 0.47%, 0.08%, and 0.26% for the three
generation tasks, which is clearly minimal. These experimental results regarding time overhead further reinforce the
practicality and superiority of DCW.


**7. Conclusion**


In conclusion, we find that DPMs often suffer from a signalto-noise ratio–timestep (SNR-t) bias. This bias refers to the
mismatch between the SNR of a denoising sample and its associated timestep during inference. During training, the SNR
of a sample is a deterministic function of its timestep, but this
coupling is broken at inference due to accumulated prediction and discretization errors, which leads to error accumulation and degraded generation quality. We provide empirical
evidence and theoretical analysis for this phenomenon and
propose a simple differential correction method to mitigate
the SNR-t bias. Since diffusion models tend to reconstruct
low-frequency components before refining high-frequency
details in the reverse process, we decompose samples into
multiple frequency components and apply differential correction to each component separately. Extensive experiments
show that our approach improves the generation quality of
various diffusion models on datasets with different resolutions, while incurring negligible computational overhead.


**References**


[1] Fan Bao, Chongxuan Li, Jiacheng Sun, Jun Zhu, and Bo
Zhang. Estimating the optimal covariance with imperfect
mean in diffusion probabilistic models. In _ICML_, 2022. 6, 7

[2] Fan Bao, Chongxuan Li, Jun Zhu, and Bo Zhang. AnalyticDPM: an analytic estimate of the optimal reverse variance in
diffusion probabilistic models. In _ICLR_, 2022. 6, 7

[3] Black Forest Labs. Flux. [https://github.com/](https://github.com/black-forest-labs/flux)
[black-forest-labs/flux, 2024.](https://github.com/black-forest-labs/flux) 2, 6, 7

[4] Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis.
Align your latents: High-resolution video synthesis with latent diffusion models. In _CVPR_, 2023. 1

[5] Chubin Chen, Jiashu Zhu, Xiaokun Feng, Nisha Huang, Chen
Zhu, Meiqi Wu, Fangyuan Mao, Jiahong Wu, Xiangxiang
Chu, and Xiu Li. Stochastic self-guidance for training-free
enhancement of diffusion models. In _ICLR_, 2026. 2

[6] Nanxin Chen, Yu Zhang, Heiga Zen, Ron J Weiss, Mohammad Norouzi, and William Chan. Wavegrad: Estimating
gradients for waveform generation. In _ICLR_, 2021. 1

[7] Ruidong Chen, Yancheng Bai, Xuanpu Zhang, Jianhao Zeng,
Lanjun Wang, Dan Song, Lei Sun, Xiangxiang Chu, and Anan
Liu. Layer-wise instance binding for regional and occlusion
control in text-to-image diffusion transformers. _arXiv preprint_
_arXiv:2603.05769_, 2026. 2

[8] Patryk Chrabaszcz, Ilya Loshchilov, and Frank Hutter. A
downsampled variant of ImageNet as an alternative to the
CIFAR datasets. _arXiv preprint arXiv:1707.08819_, 2017. 6

[9] Xiangxiang Chu, Renda Li, and Yong Wang. Usp: Unified
self-supervised pretraining for image generation and understanding. In _ICCV_, 2025. 2

[10] Guillaume Couairon, Jakob Verbeek, Holger Schwenk, and
Matthieu Cord. DiffEdit: Diffusion-based semantic image
editing with mask guidance. In _ICLR_, 2023. 2

[11] Prafulla Dhariwal and Alexander Nichol. Diffusion models
beat GANs on image synthesis. In _NeurIPS_, 2021. 1, 2, 3, 6

[12] Tim Dockhorn, Arash Vahdat, and Karsten Kreis. Genie:
Higher-order denoising diffusion solvers. In _NeurIPS_, 2022.
2

[13] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing
Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and
Yoshua Bengio. Generative adversarial nets. In _NeurIPS_,
2014. 2

[14] Amara Graps. An introduction to wavelets. _IEEE Computa-_
_tional Science and Engineering_, 1995. 5, 6

[15] Haodong He, Xin Zhan, Yancheng Bai, Rui Lan, Lei Sun,
and Xiangxiang Chu. Texts-diff: Texts-aware diffusion model
for real-world text image super-resolution. _arXiv_ _preprint_
_arXiv:2601.17340_, 2026. 2

[16] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter. GANs trained by a two
time-scale update rule converge to a local nash equilibrium.
In _NeurIPS_, 2017. 6, 5

[17] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. In _NeurIPS_, 2020. 1, 2, 6




[18] Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine.
Elucidating the design space of diffusion-based generative
models. In _NeurIPS_, 2022. 2, 4, 6, 7

[19] Levon Khachatryan, Andranik Movsisyan, Vahram Tadevosyan, Roberto Henschel, Zhangyang Wang, Shant
Navasardyan, and Humphrey Shi. Text2video-zero: Textto-image diffusion models are zero-shot video generators. In
_ICCV_, 2023. 1

[20] Dongjun Kim, Yeongmin Kim, Se Jung Kwon, Wanmo Kang,
and Il-Chul Moon. Refining generative process with discriminator guidance in score-based diffusion models. In _ICML_,
2023. 1

[21] Zhifeng Kong, Wei Ping, Jiaji Huang, Kexin Zhao, and Bryan
Catanzaro. DiffWave: A versatile diffusion model for audio
synthesis. In _ICLR_, 2021. 1

[22] Alex Krizhevsky, Geoffrey Hinton, et al. Learning multiple
layers of features from tiny images. 2009. 3, 6

[23] Rui Lan, Yancheng Bai, Xu Duan, Mingxing Li, Dongyang
Jin, Ryan Xu, Lei Sun, and Xiangxiang Chu. Flux-text: A
simple and advanced diffusion transformer baseline for scene
text editing. _arXiv preprint arXiv:2505.03329_, 2025. 2

[24] Jiachen Lei, Keli Liu, Julius Berner, Y HoiM, Hongkai Zheng,
Jiahong Wu, and Xiangxiang Chu. There is no VAE: Endto-end pixel-space generative modeling via self-supervised
pre-training. In _ICLR_, 2026. 2

[25] Haoying Li, Yifan Yang, Meng Chang, Shiqi Chen, Huajun
Feng, Zhihai Xu, Qi Li, and Yueting Chen. Srdiff: Single
image super-resolution with diffusion probabilistic models.
_Neurocomputing_, 2022. 2

[26] Mingxiao Li, Tingyu Qu, Ruicong Yao, Wei Sun, and MarieFrancine Moens. Alleviating exposure bias in diffusion models through sampling with shifted time steps. In _ICLR_, 2024.
2, 4, 3

[27] Yangming Li and Mihaela van der Schaar. On error propagation of diffusion models. In _ICLR_, 2024. 2

[28] Xingchao Liu, Xiwen Zhang, Jianzhu Ma, Jian Peng, et al.
Instaflow: One step is enough for high-quality diffusion-based
text-to-image generation. In _ICLR_, 2023. 2

[29] Ziwei Liu, Ping Luo, Xiaogang Wang, and Xiaoou Tang.
Deep learning face attributes in the wild. In _ICCV_, 2015. 6

[30] Cheng Lu and Yang Song. Simplifying, stabilizing and scaling
continuous-time consistency models. In _ICLR_, 2025. 2

[31] Cheng Lu, Yuhao Zhou, Fan Bao, Jianfei Chen, Chongxuan
Li, and Jun Zhu. DPM-solver: A fast ODE solver for diffusion
probabilistic model sampling in around 10 steps. In _NeurIPS_,
2022. 1, 2

[32] Eric Luhman and Troy Luhman. Knowledge distillation in iterative generative models for improved sampling speed. _arXiv_
_preprint arXiv:2101.02388_, 2021. 2

[33] Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun
Wu, Jun-Yan Zhu, and Stefano Ermon. SDEdit: Guided image
synthesis and editing with stochastic differential equations.
In _ICLR_, 2022. 2

[34] Chenlin Meng, Robin Rombach, Ruiqi Gao, Diederik
Kingma, Stefano Ermon, Jonathan Ho, and Tim Salimans.
On distillation of guided diffusion models. In _CVPR_, 2023. 2


[35] Yingmao Miao, Zhanpeng Huang, Rui Han, Zibin Wang,
Chenhao Lin, and Chao Shen. Shining yourself: High-fidelity
ornaments virtual try-on with diffusion model. In _CVPR_,
2025. 2

[36] Amitoj Singh Miglani, Shweta Singh, and Vidit Aggarwal.
Analysing the spectral biases in generative models. In _The_
_Fourth Blogpost Track at ICLR 2025_, 2025. 4

[37] Alexander Quinn Nichol and Prafulla Dhariwal. Improved
denoising diffusion probabilistic models. In _ICLR_, 2021. 6

[38] Mang Ning, Enver Sangineto, Angelo Porrello, Simone
Calderara, and Rita Cucchiara. Input perturbation reduces
exposure bias in diffusion models. In _ICML_, 2023. 1, 2, 6

[39] Mang Ning, Mingxiao Li, Jianlin Su, Albert Ali Salah, and
Itir Onal Ertugrul. Elucidating the exposure bias in diffusion
models. In _ICLR_, 2024. 2, 4, 6, 7, 3, 5

[40] Gaurav Parmar, Krishna Kumar Singh, Richard Zhang, Yijun
Li, Jingwan Lu, and Jun-Yan Zhu. Zero-shot image-to-image
translation. In _ACM SIGGRAPH_, 2023. 2

[41] William Peebles and Saining Xie. Scalable diffusion models
with transformers. In _CVPR_, 2023. 6, 7, 5

[42] Yurui Qian, Qi Cai, Yingwei Pan, Yehao Li, Ting Yao, Qibin
Sun, and Tao Mei. Boosting diffusion models with moving
average sampling in frequency domain. In _CVPR_, 2024. 2

[43] Xiangyan Qu, Zhenlong Yuan, Jing Tang, Rui Chen, Datao
Tang, Meng Yu, Lei Sun, Yancheng Bai, Xiangxiang Chu,
Gaopeng Gou, et al. From scale to speed: Adaptive test-time
scaling for image editing. _arXiv preprint arXiv:2603.00141_,
2026. 2

[44] Zhiyao Ren, Yibing Zhan, Liang Ding, Gaoang Wang,
Chaoyue Wang, Zhongyi Fan, and Dacheng Tao. Multi-step
denoising scheduled sampling: Towards alleviating exposure
bias for diffusion models. In _AAAI_, 2024. 2

[45] Robin Rombach, Andreas Blattmann, Dominik Lorenz,
Patrick Esser, and Bjorn¨ Ommer. High-resolution image
synthesis with latent diffusion models. In _CVPR_, 2022. 1, 2

[46] Chitwan Saharia, Jonathan Ho, William Chan, Tim Salimans, David J Fleet, and Mohammad Norouzi. Image superresolution via iterative refinement. _TPAMI_, 2022. 2

[47] Tim Salimans and Jonathan Ho. Progressive distillation for
fast sampling of diffusion models. In _ICLR_, 2022. 2

[48] Jascha Sohl-Dickstein, Eric Weiss, Niru Maheswaranathan,
and Surya Ganguli. Deep unsupervised learning using
nonequilibrium thermodynamics. In _ICML_, 2015. 1, 2

[49] Jiaming Song, Chenlin Meng, and Stefano Ermon. Denoising
diffusion implicit models. In _ICLR_, 2021. 6

[50] Yang Song and Prafulla Dhariwal. Improved techniques for
training consistency models. In _ICLR_, 2024. 2

[51] Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano Ermon, and Ben Poole. Score-based
generative modeling through stochastic differential equations.
In _ICLR_, 2021. 1

[52] Yang Song, Prafulla Dhariwal, Mark Chen, and Ilya Sutskever.
Consistency models. In _ICML_, 2023. 2

[53] Soobin Um and Jong Chul Ye. Self-guided generation of
minority samples using diffusion models. In _ECCV_, 2024. 6

[54] Soobin Um, Suhyeon Lee, and Jong Chul Ye. Don’t play
favorites: Minority guidance for diffusion models. In _ICLR_,
2024. 4, 3




[55] Arash Vahdat, Karsten Kreis, and Jan Kautz. Score-based
generative modeling in latent space. In _NeurIPS_, 2021. 5, 7

[56] JiYuan Wang, Chunyu Lin, Lei Sun, Rongying Liu, Lang Nie,
Mingxing Li, Kang Liao, Xiangxiang Chu, and Yao Zhao.
From editor to dense geometry estimator. _arXiv_ _preprint_
_arXiv:2509.04338_, 2025. 2

[57] Zekun Wang, Mingyang Yi, Shuchen Xue, Zhenguo Li, Ming
Liu, Bing Qin, and Zhi-Ming Ma. Improved diffusion-based
generative model with better adversarial robustness. In _ICLR_,
2025. 2, 6

[58] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan
Gao, Kun Yan, Sheng ming Yin, Shuai Bai, Xiao Xu, Yilei
Chen, Yuxiang Chen, Zecheng Tang, Zekai Zhang, Zhengyi
Wang, An Yang, Bowen Yu, Chen Cheng, Dayiheng Liu, Deqing Li, Hang Zhang, Hao Meng, Hu Wei, Jingyuan Ni, Kai
Chen, Kuan Cao, Liang Peng, Lin Qu, Minggang Wu, Peng
Wang, Shuting Yu, Tingkun Wen, Wensen Feng, Xiaoxiao Xu,
Yi Wang, Yichang Zhang, Yongqiang Zhu, Yujia Wu, Yuxuan
Cai, and Zenan Liu. Qwen-image technical report, 2025. 6, 7

[59] Yilun Xu, Ziming Liu, Yonglong Tian, Shangyuan Tong, Max
Tegmark, and Tommi Jaakkola. PFGM++: Unlocking the
potential of physics-inspired generative models. In _ICML_,
2023. 6, 7

[60] Yuzhe YAO, Jun Chen, Zeyi Huang, Haonan Lin, Mengmeng
Wang, Guang Dai, and Jingdong Wang. Manifold constraint
reduces exposure bias in accelerated diffusion sampling. In
_ICLR_, 2025. 2

[61] Mingyang Yi, Aoxue Li, Yi Xin, and Zhenguo Li. Towards
understanding the working mechanism of text-to-image diffusion model. In _NeurIPS_, 2024. 2, 5

[62] Fisher Yu, Ari Seff, Yinda Zhang, Shuran Song, Thomas
Funkhouser, and Jianxiong Xiao. Lsun: Construction of a
large-scale image dataset using deep learning with humans in
the loop. _arXiv preprint arXiv:1506.03365_, 2015. 6

[63] Meng Yu and Kun Zhan. Bias mitigation in graph diffusion
models. In _ICLR_, 2025. 2

[64] Meng Yu and Kun Zhan. Frequency regulation for exposure
bias mitigation in diffusion models. In _ACM MM_, 2025. 2, 4,
6, 7, 3

[65] Guoqiang Zhang, Kenta Niwa, and W Bastiaan Kleijn. Lookahead diffusion probabilistic models for refining mean estimation. In _CVPR_, 2023. 4, 5, 3

[66] Junyu Zhang, Daochang Liu, Eunbyung Park, Shichao Zhang,
and Chang Xu. Anti-exposure bias in diffusion models. In
_ICLR_, 2025. 2, 6

[67] Wenliang Zhao, Lujia Bai, Yongming Rao, Jie Zhou, and
Jiwen Lu. Unipc: A unified predictor-corrector framework
for fast sampling of diffusion models. In _NeurIPS_, 2024. 2

[68] Zangwei Zheng, Xiangyu Peng, Tianji Yang, Chenhui Shen,
Shenggui Li, Hongxin Liu, Yukun Zhou, Tianyi Li, and Yang
You. Open-sora: Democratizing efficient video production
for all. _arXiv preprint arXiv:2412.20404_, 2024. 1

[69] Zhenyu Zhou, Defang Chen, Can Wang, and Chun Chen. Fast
ODE-based sampling for diffusion models in around 5 steps.
In _CVPR_, 2024. 2


## **Elucidating the SNR-t Bias of Diffusion Probabilistic Models** Supplementary Material



**A. Difference from Prior Works**


In this section, we outline the differences between the second
experiment (Fig. 1c) in Sec 4 of this paper and prior work

[38, 39]. We emphasize that ADM-ES [39] only provides
a phenomenological conclusion and does not delve into the
underlying causes of the phenomenon. In contrast, the SNRt bias discovered in this paper, along with the sliding window
experiments on neural networks based on Fig. 1b, provide
in-depth explanations and evidence for this phenomenon.
Additionally, this section offers more robust experimental
analyses for the phenomenon.

(1) The SNR-t bias is the underlying cause of exposure
bias proposed by ADM-IP [38] and ADM-ES [39]. ADMIP and ADM-ES define the exposure bias as an intuitively
inter-sample bias between the perturbed sample _**x**_ _t_ and the
predicted sample _**x**_ **ˆ** _t_ . Meanwhile, ADM-ES also claims that
exposure bias leads to the accumulation of errors, yet it fails
to provide fundamental evidence for such error accumulation. In contrast, we explicitly demonstrate when the SNR
of the input sample mismatches the timestep, the network’s
predictive output exhibits significant errors, as shown in the
Key Finding 1 (Fig. 1b). Furthermore, since the SNR of
reverse-process samples is consistently lower than the ideal
level, as shown in the Key Finding 2 (Fig. 1c), the network’s
predictions during the reverse process are invariably erroneous, specifically manifesting as overestimated outputs. In
summary, the SNR-t bias stems primarily from the forced
coupling of sample SNR and timestep during training.

(2) Unlike ADM-ES, this paper focuses on drawing
deeper conclusions and uncovering the underlying patterns.
Specifically, Figure 2 in ADM-ES concludes that the _L_ 2norm of _**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ) in the reverse process is always larger than
that of _**ϵθ**_ ( _**x**_ _t, t_ ) in the forward process. However, ADM-ES
does not explore the deep-seated reasons for this overestimation phenomenon. In this paper, we derive Finding 1
through the sliding window experiments in Sec. 4: for the
fixed timestep _s_, when handling the sample _**x**_ _t_ with a lower
SNR, where _t_ _>_ _s_, the network tends to overestimate the
predicted output. Conversely, when dealing with the sample
_**x**_ _t_ with a higher SNR, the predicted output is typically underestimated. Therefore, combining the findings of ADM-ES
and Finding 1 of this paper, we arrive at Finding 2: Reverse
denoising samples often exhibit lower SNR compared to
their corresponding forward samples at the same timestep.

(3) Unlike exposure bias, an inter-sample bias, the SNR-t
bias is a more specific SNR-timestep bias. Meanwhile, our
method based on the SNR-t bias can be naturally integrated
into state-of-the-art models for correcting exposure bias,



such as ADM-IP, ADM-ES, and DPM-FR, further improving
the generation quality of these correction models as shown in
Sec. 6.2. Additionally, our method can significantly enhance
the generation quality in the latest text-to-image models,
as shown in Appendix E. Thus, these experiments further
illustrate the differences between SNR-t bias and exposure
bias, as well as the necessity of researching SNR-t bias.
Furthermore, we also provide more robust experimental
evidence for Fig. 1c to eliminate interference caused by
random seeds and sampling batch sizes. Specifically, we
fix the sampling batch size at 2000 and then select different
random number seeds (16, 42, and 99) to obtain distinct
sampling trajectories, as illustrated in Figs. 5a, 5b, and 5c,
respectively. Subsequently, we fix the random number seed
and vary the sampling batch sizes (10, 100, and 1000), as
shown in Figs. 5d, 5e, and 5f, respectively. Fig. 5 clearly
demonstrates that regardless of the random number seed
and sampling batch size, the network output of the reverse
process is consistently larger than that of the forward process,
which provides more robust evidence for our analysis.


**B. Theoretical evidence of Assumption 5.1**


**Assumption 5.1.** _During both the forward and reverse pro-_
_cesses, the reconstruction sample_ _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] _[ can be expressed]_
_in terms of the original data_ _**x**_ 0 _as follows:_


_**\**_ [x ] _**[^]**_ _[0][_ \]_ [T h] _[ e]_ _**[(]**_ [\] [h] _[ a][t]_ _[{][\]_ (22)


_where_ 0 _<_ _γt_ ⩽ 1 _,_ _ϕt_ _<_ _M_ _,_ _and_ _M_ _denotes_ _a_ _uniform_
_upper bound constant across all timesteps._
Specifically, we emphasize that both the forward reconstructed sample _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ and the reverse reconstructed sam-]
ple _**x**_ [0] _**θ**_ [(ˆ] _**[x]**_ _[t][, t]_ [)][ adhere to the form specified in Eq.][ 22][.]
In this section, we present the detailed proof of Assumption 5.1. As stated in the main text, previous work proposed
two distinct linear assumptions but lacked supporting evidence. However, we provide both experimental evidence and
theoretical proofs to support our findings. Under Gaussian
perturbation _**q**_ _σ_ ( _**y**_ _|_ _**x**_ ), the Tweedie’s formula is


_**\**_ _m_ _**a**_ t h _**b**_ b [{] _E_ _**}**_ [\x _|_ \ _**y**_ _] =_ (23)


where _**q**_ _σ_ ( _**y**_ ) := - _**q**_ ( _**y**_ _|_ _**x**_ ) _**q**_ ( _**x**_ )d _**x**_ . Now, by substituting the
forward perturbation distribution _**q**_ ( _**x**_ _t|_ _**x**_ 0) of DPMs into
Eq. 23, we can obtain:


_[{]_ [ E }[] _[ \]_ [x] _[_]_ [0] _[|]_ _**[\]**_ _[x]_ [ _t] _**[]]**_ [=] _**[\]**_ _[f]_ [r]
_**\**_ m _a_ _**t**_ _h_ b b ~~_a_~~ _\_ (24)
c _{_


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||~~orwa~~|~~rd~~|~~rd~~|
|||||||||R|ever|se||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||


t


(c) Seed=99, Batch Size=2000

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||~~rd~~|~~rd~~|
|||||||||~~F~~|~~orwa~~|~~rd~~|~~rd~~|
||||||||||ever|e||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||



t


(f) Seed=99, Batch Size=1000



54
51
48
45
42
39
36


54

51

48

45

42

39

36



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||~~orwa~~|~~rd~~|~~rd~~|
|||||||||R|ever|se||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||


t


(a) Seed=16, Batch Size=2000

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||rd|rd|
|||||||||F|orwa|rd|rd|
|||||||||R|ever|se||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||



t


(d) Seed=42, Batch Size=10



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||~~orwa~~|~~rd~~|~~rd~~|
|||||||||R|ever|se||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||


t


(b) Seed=42, Batch Size=2000

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|
|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||~~rd~~|~~rd~~|
|||||||||~~F~~|~~orwa~~|~~rd~~|~~rd~~|
||||||||||ever|e||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||
|||||||||||||



t


(e) Seed=42, Batch Size=100



54
51
48
45
42
39
36


54
51
48
45
42
39
36



54
51
48
45
42
39
36


54
51
48
45
42
39
36



Figure 5. Robust experimental results for Fig. 1c with varied random number seeds and sampling batch sizes. These figures show the
network output _||_ _**ϵθ**_ ( _·, t_ ) _||_ 2 using forward samples _**x**_ _t_ via Eq. 2 and reverse predicted samples _**x**_ **ˆ** _t_ via Eq. 8, respectively. _||_ _**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ) _||_ 2 is
always larger than _||_ _**ϵθ**_ ( _**x**_ _t, t_ ) _||_ 2 in every figure.



Based on the relationship between the score and the noise
_**sθ**_ ( _**x**_ _t, t_ ) = _−_ _**[ϵ]**_ ~~_√_~~ _**[θ]**_ 1 [(] _**[x]**_ _−_ _[t]_ _α_ ¯ _[,t]_ _t_ [)], we further derive:

_[{][ E ][}]_ [[] _[ \]_ [x] _[_]_ _**[0][|]**_ [\] _**[x]**_ _[_ t]_ []]
_**\**_ m _a_ _**t**_ _h_ b b ~~_=_~~ a _**c{**_ [\] _**[x]**_ _[_ t]_ [-] _[\]_ (25)
_f_ \ _r_


which clearly demonstrates that the reconstructed sample
_**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] [is] [essentially] [the] [posterior] [mean] [based] [on] [the]
Tweedie formula. Furthermore, the score network trained
with the L2 norm-MSE loss function always have a theoretical analytical solution [54], which is also the posterior mean:


\ _**s**_ __ \_ T h e ( _**\**_ x _**_**_ _t_, t _)_ _=_ \m _a_ t _**h**_ _b_ _b_ {E} ___ (26)


Based on the equivalence between the score and noise, the
optimal solution for noise prediction is also the same posterior mean. Therefore, based on the mean tendency of
denoising operations and network predictions, we can regard
_**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ as the mean estimate] _**[x]**_ [¯][0][ of] _**[ x]**_ [0][.]
The variance formula is expressed as:


_\_ _**m**_ a _t_ [h] b b _**E**_ {} _[_ [\] | \x ___ _**0**_ _\_ | _^_ (27)


Based on the non-negativity of the variance, we obtain:


_**\**_ | [\] b ar _**{**_ \ _x_ } ___


We substitute _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] [for] _**[x]**_ [¯][0][,] [then] [given] [that] [the] [expec-]
tation of a constant is the constant itself, we can take the
expectation of both sides of the above equation to obtain:



_\_ _**m**_ [a] _**t**_ [h] _**[b]**_ _[b][ {]_ [E] _[}]_ [[][\][ |] [\] _[x]_ [^] _[0]_ [_][\] _[T]_ (28)


Eq. 28 clearly demonstrates that the L2 norm of reconstructed samples is always smaller than that of real samples,
which indicates that the reconstruction operation is always
accompanied by information loss.
However, previous work [26, 39] argues that reconstructed samples should be modeled as:


_**\**_ [x] _[^][0 _]_ [\ T] _**[ h]**_ [e] _[(][\]_ _**[x]**_ _[_]_ (29)


which is clearly inconsistent with Eq. 28. Thus, We use
the form in Eq. 22, consistent with the assumption of LADPM [65] and DPM-FR [64].
In addition, we also provide experimental evidence for
the above proof. Following the experimental setup described
in Sec. 4, we perform the following operations sequentially:
(1) We generate perturbed samples _{_ _**x**_ 1 _,_ _**x**_ 2 _, . . .,_ _**x**_ _T }_ via
Eq. 2, and feed _**x**_ _t_ and timestep _t_ into the network to obtain
_**ϵθ**_ ( _**x**_ _t, t_ ) to compute _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ via Eq.][ 5][.] [(2) Then, we ini-]
tialize 2,000 standard Gaussian noise and iteratively denoise
operation via Eq. 8 to obtain samples _{_ _**x**_ **ˆ** 1 _,_ **ˆ** _**x**_ 2 _, . . .,_ **ˆ** _**x**_ _T }_
and corresponding network outputs _**ϵθ**_ ( _**x**_ **ˆ** _t, t_ ) to compute
_**x**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] [via] [Eq.] [5][.] [(3)] [Finally,] [we] [compute] [and] [plot] [the]
expectation of _||_ _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] _[||]_ 2 [2][,] _[ ||]_ _**[x]**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] _[||]_ 2 [2][, and] _[ ||]_ _**[x]**_ [0] _[||]_ [2] 2 [.]
Fig. 6 clearly demonstrates that DPMs fail to fully reconstruct real data _**x**_ 0, both in the forward and reverse processes.


27

25

23

21

19

17

15



|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||
||||||||||||||
||||||||||||||
||||Fo|rward|||||||||
||||Re<br>~~Tr~~|verse<br>~~uth~~|||||||||
||||||||||||||
||||||||||||||
||||||||||||||
||||||||||||||


t



Then, substituting Eq. 25 into Eq. 32, we can obtain an
equivalent form of the reverse denoising process:



_\b_ e g & _\h_ _**a**_ t _{\_ _**x**_ }_

n _e_ _}_ d
_{_
_t-_ 1} = _\f_ ra _r_

_[r]_



_\_ { _x_ } __{_
_\h_ a t



t _{_ _b_ \ _ar_ { ~~_~~

_**a**_ }
\ _a_ _p_ l _h_



_t_ { _**-**_ _1_



1} = _\f_ ra _r_

q _[r]_ t _{_ _**\**_ b a
c _\_ { _s_



_s_

_\_ { _x_ } __{_ _qr_ t _{_ _b_ \ _ar_ {

_**=\**_ [f] _**[r]**_ _[a][c ]_ [{\]
t _-_ _}_ 1 \ _a_ _p_ l _h_



~~}~~
_{_ _a_ \ _l_ _**p**_ ha



(33)
By substituting Eqs. 31 and 22 into Eq. 33 to replace
_**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ and] _**[ x]**_ _[t]_ [, we can obtain:]



_i_
n _{a_ l _ig_
_\b_ e g



_{_ _ _t_ 


Figure 6. The expectation of _||_ _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)] _[||]_ 2 [2][,] _[ ||]_ _**[x]**_ [0] _**θ**_ [(] _**[x]**_ **[ˆ]** _[t][, t]_ [)] _[||]_ 2 [2][, together]
with the ground-truth norm of _**x**_ 0.


This further indicates that the reconstruction operation incurs information loss. Notably, similar experiments are also
reported in DPM-FR [64]. However, it focuses on the differences between the forward and reverse processes, whereas
our work places greater emphasis on whether DPMs can fully
reconstruct real data. Additionally, we argue that conducting
experiments in the data space is more persuasive. This experiment further demonstrates that _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ and] _**[ x]**_ [0] _**θ**_ [(ˆ] _**[x]**_ _[t][, t]_ [)]
adhere to the form specified in Eq. 22.


**C. Proofs of Theorem 5.1 and Eq. 15**


In this section, we present the detailed proofs of Theorem 5.1
and Eq. 15. Our derivation process is mainly based on DPMFR [64]. However, we provide a more rigorous derivation
process, particularly for _γt_ and ˆ _γt_ . Specifically, we focus on
SNR, the core theme of this work.


**Theorem 5.1.** _For a specific timestep t in the reverse de-_
_noising process of DPMs, the SNR of the biased denoising_
_sample_ _**x**_ **ˆ** _t is given by:_

_\_
\t _e_ x t _{N_ [S] _[}]_ [R] _[(][t]_ )= _\_ _a_ h _t_ { _a_ g _mma_ } _\b_ ar [{][\] _a_ (30)
^ _2_ _{_ _ _t_ }{


_where_ 0 _<_ _γ_ ˆ _t_ ⩽ 1 _and ϕt_ +1 _is derived from the reconstruc-_
_tion model_ _**x**_ [0] _**θ**_ [(ˆ] _**[x]**_ _[t]_ [+1] _[, t]_ [ + 1)] _[ in Eq.][ 10][.]_
Firstly, we emphasize that all subsequent noise terms
_**ϵ**_ follow the standard Gaussian distribution. We rewrite
the fundamental formula of DPMs and the forward noising
process is expressed as:



_}_
1 _\_ } _be_ t _a_ __{_




_-_ _h_

_\_ } _be_ t _a_ __{_ _\_ ba _r_ _{\a_ lp a _}_

t _}_ _{_ } _1_ _ _{_ _}_ t _}_



( m
_**\**_ g a _a_ m _**_**_ t



_0_ + _\ph_ __t_ ) _+_ _\\_ &\ _[f]_ r _a_ c _{_

_**e**_ _p_ s
i _t_ _ _\_ \ _s_ _r_ q _t_



_x_
__0_ + _\ph_
\



_ _{_ _}_ t _}_



{
\ _s_ _r_ q _t_



(34)
For Eq. 34, we first focus on the coefficient of _**x**_ 0:



_d_ _s_

_\be_ g _in_ _{_ _}_ &\ _f_ _a_ r _c_ {\ _r_ q _t_

e
a _l_ _g_ i _n_ _{_ _b_ \ _a_



_\be_ g _in_ _{_



_{_ _b_ \ _a_



_\_ { _al_ pha _} _{_ t _-_ _1}_ }\ _b_ _t_ e _a_ _{t
r



(35)



_m_
} _\_ _a_ g _m_



Given that _γt_ ⩽ 1, we use the scaling method to amplify
it to 1, yielding the following inequality:


_\be_ gin _{ al_ i _gn_ e _d}_ & _\_ _r_ f _ac_ {\



s _q_ _t_ r



_\a_ b _r_ {\al _p ha_ } __{_ t _-_ _1}}_ \bi
{



(36)



g _(_ ( _1_

- _[{]_ _a_ \ _lp_ h



Given that 1 _−_ _αt_ _>_ 0 _, γt_ ⩽ 1, We may rigorously define
a novel coefficient ˆ _γt−_ 1 ⩽ 1 for _**x**_ **ˆ** _t−_ 1 where



_g_ _in_ g _ed_ } \h _a t_ { _\g_ a _mm_ a _}_ _{_ _ _t-_ 1}\
_\b_ e _n_ i _{_ a l



_{_
s _q_ _t_ r



(37)
For the standard Gaussian noise component in Eq. 34,
based on the properties of the Gaussian distribution, we
define a new coefficient _ψ_ [ˆ] _t−_ 1 such that:



_n_
_{al_ i _gn_
_\b_ e g i



_\_

_{al_ i _gn_ _ps_ i _}_ _{_ _ _t-_ 1}

_\h_ a [t] {
e _d_ } _&_ = _(_ _f_ \ _r_



= _(_ _f_ \ _r_



a



c _\_ { _sq_ rt { _b_ [\] _a_



h _i_ __{_



_q_
\ _[x]_ __t_ _**=**_ \ s



r _t_ _{\_ _**b**_ a _r_ (31)



_{_
_a_ \ _lp_ h _a_
r

_)_ } ___ _t_ { _-_
_{_ ^ _2}_ + _(\_
t }

f _r_ _c_ a

_-_
_}_ 1 _)}_ { _1-_
{ t



_a_ \ _lp_ h _a_ _[t]_ [{] _[}][}]_ [{][1][-]

_1}_ } [\] b _[e][t]_ [a ] _[_]_
} ___ _t_ { _-_ \ _b_ _r_ a




_[_]_ _[t]_ [{] _[}][}]_ [{][1][-] _[h]_ [p] _[a]_ [}][_{t] _[ }][ }][\]_ [p]

{ [\a] _[ l]_
\ _b_ _r_ a h _i_ __{_



We assume the current predicted sample is ideal. Thus, the
reverse denoising process is expressed as:



_{_ ^ _2}_ + _(\_ [{\] _[ a]_ _[p]_ [l] _[h][a]_ [_][{][ t }}] _[ (]_ _[-]_ [1] _[\][b]_ [a][r {] _[ \][ a][l]_ [p]

_{\_ s [q] r _[t]_
f _r_ _c_ a h _a_ _}__



h _a_ _}__



(38)



_)}_ { _-_

_{\_ a [l] p h _a_ _}_{_ t _}_
\ _b_ _r_ a



_{\_ h x ~~_}_~~
__{_



t _**-**_ _1 }_ ~~_f_~~ _[=]_ _[\]_ _**1}**_ { _**\**_ _sq r_ t { _\a_ _**l**_ p _h_ (32)
r _a_ c _{_


Based on Eqs. 37 and (38), we can obtain



_l_
_\b_ e g _n_ i _{_ a _g_ i _ne_ d _**}**_ \



~~h~~



~~_{_~~

_-_ t _1}_ _=\_
a _t_ _{\x_ } _



_\g_ a [m] _**m**_ _a_ }
h _a_ t _{_



Table 8. FID and Recall (Rec) on DiT.


_T_ = 20 _T_ = 50


Model Dataset FID _↓_ Rec _↑_ FID _↓_ Rec _↑_


DiT ImageNet 256 12.83 0.54 3.78 0.58
DiT-ES ImageNet 256 10.00 - 3.30 **DiT+Ours** **ImageNet** 256 **7.99** **0.51** **3.09** **0.56**


threshold _ts_, based on empirical experience, we classify
_t > t_ s as the early stage of denoising and _t_ ⩽ _ts_ as the later
stage of denoising. Accordingly, the piecewise weight for
low-frequency components can be defined as:


_w_ [_] _[ t][^]_ _[l]_ _[=]_ [w] _[ _][l]_ _[\cdo]_ (42)


where I( _·_ ) denotes the indicator function. In a similar vein,
the piecewise weight for high-frequency components is naturally defined as:


_w_ [_] _[ t][^]_ _[h]_ _[=][ w _][h]_ _[\cdo]_ (43)


Furthermore, to simplify the implementation, we also design
a constant weighting strategy, where the weights remain
unchanged throughout the entire denoising process.
In particular, we emphasize that all three aforementioned
weighting strategies are effective after extensive experimental evaluations, as shown in Sec.6. Specifically, the
variance-based scheduling strategy and the piecewise weighting strategy achieve superior generation quality, which further demonstrates the necessity of aligning the weight design
with the denoising dynamics of DPMs.


**E. Additional Results**


Given the extensive influence of transformer-based diffusion
models, we select DiT [41] as the baseline model, ADMES [39] as the comparative model. Subsequently, we adopt
Frechet´ Inception Distance (FID) [16] and Recall [16] as
evaluation metrics, and select ImageNet 256 _×_ 256 as the
test dataset for our experiments.
Tab. 8 clearly demonstrates that our method achieves
a comprehensive reduction in the FID scores of DiT and
outperforms the comparative models significantly. In the
subsequent appendix, we also provide the evaluation results
of two text-to-image models, which are also based on the
DiT architecture.


**F. Qualitative Comparison**


To show the improvement effect of DCW on the generation
quality of DPMs, we select two **state-of-the-art** text-toimage models, namely **Qwen-Image**, which demonstrates
strong instruction following and text rendering ability, and



(39)
Ultimately, based on Eq. 39, we obtain the SNR of _**x**_ _t−_ 1 as:



\t _e x_ t { _N_ S _}_ [R] _(_ t _[1]_ [-] _[)][=]_ [\] _[h]_ at _\_ { _ga_ m m a _^_ } _2__ { _t-_



_2_ { _-_

_ar_ [{][\]
1 _}_ _\_ { _b_



(40)
By replacing the timestep in Eq. 40, we ultimately obtain the
actual SNR of _**x**_ **ˆ** _t_ to complet the proof.
To obtain a more concise and intuitive form, we use the
piecing-together method to derive:



_b_ [\] _e_ g [i n] _a_ { _li_ g _ne_ _at_ [{] \ ps _i_ _}{_ [_] _t_  - [1}^] _[ 2]_ _[=]_ [&] _[(][\]_ [f][r]

d _}_ _\h_



a c _\_ [{] _s_ q [rt] _[\]_ [{] _[b][a]_ [r]


In conclusion, we have obtained the biased mean and variance of the reverse process:



_\b_ e g _n_ i _{_ a _lg_ i _ne_ d _**}**_ & \h _at_ {\



x _}_ _{_ _ _t-_ 1} _**=**_ \



a



_\_ { _ga_ m _ma_
t _-1_ } [\] s qr _t_ _{b_ [\] _a_ r [ {\] _[ a]_ _[p]_ [l] _[h][a]_ [}_] _**[{]**_ [t]

_}_ _{_ _ _t_



h



(41)



 - _1}_ } _**\**_ _x_ __0+_ + _**\**_ h _a_

where _ψt−_ 1 = �( ~~_√_~~ 1 _α_ ¯ _−t−α_ ¯1 _tβt_ _ϕt_ ) [2] + (1 _−_ _γ_ ˆ _t_ [2] _−_ 1 [)(1] _[ −]_ _[α]_ [¯] _[t][−]_ [1][)][.]

Thus, we have completed the proof of Eq. 15. Finally, we
emphasize again that _γt_ is the coefficient of the reconstruction sample _**x**_ [0] _**θ**_ [(] _**[x]**_ _[t][, t]_ [)][ in Eq.][ 22][, and][ ˆ] _[γ][t][−]_ [1][ is the coefficient]
of the predicted sample _**x**_ **ˆ** _t−_ 1 in Eqs. 39 and 41.


**D. Weight Strategy Design**


The denoising process of DPM inherently follows a coarseto-fine paradigm: the early stages primarily generate lowfrequency global structures, while the later stages progressively recover high-frequency details. To this end, our proposed differential correction method is designed to align with
this intrinsic property, prioritizing low-frequency correction
in the initial phases and shifting focus to high-frequency
correction in the later stages.
Based on the above reasoning, we assign larger correction coefficients to low-frequency components in the early
stage of denoising and higher weighting coefficients to highfrequency components in the later stage of denoising. On
this basis, we propose three weighting scheduling strategies.
Firstly, considering that the variance _σt_ in the reverse
process of DPM can dynamically characterize the denoising
progress, we adopt the weighting forms shown in Eqs. 20
and 21 in the main text. Second, we design a piecewise
weighting strategy. For the timestep _t_ (0 ⩽ _t_ _<_ _T_ ) and


Figure 7. Qualitative comparison between **Qwen-Image** (first row) and **Qwen-Image-DCW** (second row) using **10 steps**, where the prompt
is “A woman is walking on the beach by the sea”.



**FLUX**, which is known for its high visual fidelity, to conduct
extensive experiments. Given that our study focuses on the
SNR-t bias, we conduct tests with a small number of steps to
amplify the sampling errors of the baseline models as much
as possible, thereby verifying how effectively DCW corrects
such bias. As shown in Figs. 7, 8, 9, 10, 11, 12, 13, 14,
and 15, our method can significantly enhance the aesthetic
quality across different models and time steps.
Specifically, as shown in Figs. 7 and 10, our method
consistently improves the visual quality of the generated
images under a small number of sampling steps. Compared
with the original models, our method produces results with
more coherent scene structure, better semantic fidelity, and
clearer details. It also alleviates common artifacts caused
by sampling bias, leading to images that are more natural and visually appealing. These results demonstrate that
DCW is effective across different baseline models and can
reliably enhance generation quality in low-step sampling settings. Moreover, the improvements are consistently observed
across diverse scenes and content types, further highlighting
the robustness and generality of our method.


**G. Parameter sensitivity**


To demonstrate the insensitivity of DCW to hyperparameters
_λl_ and _λh_, we first apply DCW to A-DPM to obtain the



Table 9. The search process of _λl_ and _λh_ on CIFAR-10 (CS) using
A-DPM-DCW with 25 sampling steps.


Value 0.02 0.03 0.04 0.05 0.06 0.07 0.08


FID 7.64 7.37 7.24 7.18 7.19 7.35 7.66


optimal parameter _λl_ on CIFAR-10 (CS). Then, based on the
optimal parameter _λl_, we apply DCW to obtain the optimal
parameter _λh_ . Fig. 4 clearly shows that DCW can achieve
performance gains over a wide range of _λl_ and _λh_, indicating
the insensitivity of DCW to hyperparameters.
Benefiting from the strong robustness of the proposed
method to hyperparameter perturbations, the parameter
search process is fast via the two-stage search. Firstly, a
coarse search with a step size of 0.01 was performed. After
identifying a turning point in the FID curve around 0.05, we
conducted a fine-grained search with a step size of 0.001 and
quickly determined the optimal value to be 0.052, as shown
in Tab 9. Then, after fixing the optimal _λ_ _[∗]_ _l_ [at 0.052, quickly]
derive the optimal parameter _λ_ _[∗]_ _h_ [=] [0] _[.]_ [010] [using] [the] [same]
method. In summary, the above experimental process further
demonstrates the robustness and practicality of our method
with respect to hyperparameters.


Figure 8. Qualitative comparison between **Qwen-Image** (first row) and **Qwen-Image-DCW** (second row) using **10 steps**, where the prompt
is “There is a house and a path on a snowy mountain”.


Figure 9. Qualitative comparison between **Qwen-Image** (first row) and **Qwen-Image-DCW** (second row) using **10 steps**, where the prompt
is “ **A balloon** gently climbs into a serene blue sky”.


Figure 10. Qualitative comparison between **FLUX** (first row) and **FLUX-DCW** (second row) using **10 steps**, where the prompt is “There is
a house and a path on a snowy mountain”.


Figure 11. Qualitative comparison between **FLUX** (first row) and **FLUX-DCW** (second row) using **10 steps**, where the prompt is “A woman
is walking on the beach by the sea”.


Figure 12. Qualitative comparison between **FLUX** (first row) and **FLUX-DCW** (second row) using **10 steps**, where the prompt is “A balloon
gently climbs into a serene blue sky”.


Figure 13. Qualitative comparison between **Qwen-Image** (first row) and **Qwen-Image-DCW** (second row) using **20 steps**, where the
prompt is “A woman is walking on the beach by the sea”.


Figure 14. Qualitative comparison between **FLUX** (first row) and **FLUX-DCW** (second row) using **20 steps**, where the prompt is “There is
a house and a path on a snowy mountain”.


Figure 15. Qualitative comparison between **FLUX** (first row) and **FLUX-DCW** (second row) using **20 steps**, where the prompt is “A balloon
gently climbs into a serene blue sky”.


