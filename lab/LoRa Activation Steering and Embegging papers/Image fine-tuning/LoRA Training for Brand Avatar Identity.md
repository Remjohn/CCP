# **Persistent Identity Encoding for Per-Coach Brand Avatar LoRAs in FLUX 2 Diffusion Architecture**

The maturation of generative artificial intelligence has necessitated a rigorous transition from generic prompt-based imagery to hyper-specific, persistent identity encoding. Within the professional coaching industry, where visual branding is inextricably linked to trust and authority, the phenomenon of identity drift—the tendency of diffusion models to revert to a statistical mean or "professional archetype"—presents a significant obstacle to scalable content production.1 Standard diffusion models, including the early iterations of the FLUX.1 architecture, often converge on a generic "coaching face," diluting the unique anatomical markers that constitute an individual’s personal brand.2 The advent of the FLUX 2 architecture, characterized by a latent flow matching system and a 32-billion parameter transformer, provides the technical foundation necessary to address these failures through specialized Low-Rank Adaptation (LoRA) protocols.1 By synthesizing facial individuation neuroscience with advanced dataset curation and hyperparameter optimization, the Coach-Marketing Framework (CMF) can deploy persistent brand avatars that maintain identity across diverse environments and lighting conditions, ensuring brand fidelity at a cost-effective scale.5

## **Theoretical Foundations of Facial Identity and Neural Perception**

The encoding of identity within a generative model must align with the biological mechanisms the human brain utilizes to recognize and verify individuals. Research into the neurobiology of face perception, particularly the work of Rossion (2018), emphasizes that facial identification is not a simple aggregate of pixel-level features but a holistic process dependent on diagnostic spatial frequencies and orientation bands.7 Specifically, the human visual system relies disproportionately on horizontal orientation energy—often referred to as "biological bar codes"—that clusters around the eyes and eyebrows.8 These horizontal structures convey the highest diagnostic value for identity, facilitating recognition by aligning high-contrast facial features into a predictable one-dimensional sequence.9

Diagnostic information is primarily situated within mid-range spatial frequencies, specifically between 8 and 16 cycles per face.8 These frequencies capture the essential configuration of the face while filtering out irrelevant high-frequency noise or low-frequency global illumination shifts.8 Sensitivity to these horizontal structures is so foundational that even infants as young as three months demonstrate a preference for upright faces where these horizontal "bar codes" are preserved, whereas the inversion of the face disrupts this processing, leading to the well-documented face inversion effect.11 For the development of Brand Avatar LoRAs, this implies that the training data must prioritize images that preserve these mid-range frequencies and horizontal orientations, as any degradation of these features during the diffusion process will result in a perceived loss of identity persistence.8

Parallel to the neurobiological mechanisms of identity is the psychological assessment of authenticity. A comprehensive study involving 508 participants analyzed how viewers perceive AI-generated portraits, identifying three primary predictors of authenticity: Expression Naturalness (EN), Skin Texture (ST), and Facial Proportion (FP).13

### **Quantitative Impact of Visual Features on Perceived Authenticity**

| Feature Code | Visual Cue Category | Impact on Perceived Authenticity | Functional Requirement for LoRA Training |
| :---- | :---- | :---- | :---- |
| **EN** | Expression Naturalness | High (Strongest Predictor) | Diverse training on smiling, neutral, and serious expressions to avoid "uncanny" rigidity.13 |
| **ST** | Skin Texture | Moderate-High | Preservation of pore-level detail and micro-pigmentation; avoiding oversmoothing.13 |
| **FP** | Facial Proportion | Moderate-High | Correct mathematical scaling of eyes, nose, and mouth relative to head size.13 |
| **PN** | Pose Naturalness | Moderate | Alignment of the neck and shoulders with facial orientation. |
| **LR** | Limb Realism | Low (Secondary) | Peripheral detail; less critical for facial identity persistence. |

The study’s findings indicate a counterintuitive relationship between visual "perfection" and trust; images that are overly smoothed to eliminate micro-expression asymmetries or skin imperfections are often rated as less authentic than those that retain textured, slightly imperfect details.13 This "perfection-trust paradox" has immediate implications for dataset curation: images used to train per-coach LoRAs should be high-resolution but not airbrushed, as the model must learn the "tonal micro-gradients" and "skin-level imperfections" that ground the coach's identity in reality.13

## **Architectural Overhaul: The FLUX 2 Paradigm Shift**

The transition from FLUX.1 to FLUX 2 represents more than an incremental update; it is a fundamental reimagining of the text-to-image architecture. While FLUX.1 utilized a dual-encoder system involving CLIP and T5-XXL, FLUX 2 simplifies and enhances the process by integrating a single 24-billion parameter Mistral-3 vision-language model (VLM) as its primary text encoder.1 This integration allows the model to leverage intermediate layers of the Mistral-3 encoder, which are known to carry richer semantic information, thereby improving the model's adherence to complex, structured instructions.4

The model’s core is a 32-billion parameter transformer trained with a latent flow matching objective.1 Flow matching provides a more stable training signal than traditional diffusion objectives, allowing for better learnability and reconstruction fidelity.15 The FLUX 2 Variational Autoencoder (VAE) has been retrained from scratch to optimize the balance between compression and reconstruction, resulting in fewer artifacts in high-frequency regions like hair and skin pores.1

### **Technical Divergence in FLUX Architectures**

| Parameter | FLUX.1 (MM-DiT) | FLUX 2 (Latent Flow Matching) |
| :---- | :---- | :---- |
| **Total Parameters** | 12 Billion | 32 Billion (Dev Variant).1 |
| **Text Encoding** | CLIP-L \+ T5-XXL | Mistral-3.1 Small (24B VLM).1 |
| **Prompt Sequence Length** | 256 Tokens | Up to 32,000 Tokens (Pro/Max).2 |
| **Native Resolution** | 1 Megapixel | 4 Megapixel.1 |
| **Double-Stream Blocks** | 19 | 8\.4 |
| **Single-Stream Blocks** | 38 | 48\.4 |
| **Activation Function** | GELU | SwiGLU (No bias parameters).4 |

The architectural shift significantly impacts how LoRAs are trained and deployed. Due to the complete overhaul of the text encoder and the transformer layers, LoRAs trained for FLUX.1 are entirely incompatible with the FLUX 2 architecture.1 Furthermore, the increased proportion of single-stream blocks in FLUX 2—now making up approximately 73% of the total transformer parameters—requires a recalibration of the rank and alpha settings used during fine-tuning.4 The removal of bias parameters throughout the attention and feedforward sub-blocks further necessitates a clean training environment where identity markers are not diluted by historical biases in the pre-trained weights.4

## **Operational Protocols for Dataset Curation and Stratification**

The quality of a Brand Avatar LoRA is a direct function of its training dataset. To mitigate identity drift, the methodology employs a multi-stage curation pipeline that prioritizes variety and representative diversity over raw volume. A dataset of 30 to 50 real high-resolution images is the recommended baseline for character-specific training.5 Larger datasets risk diluting the model's focus, while smaller sets often fail to capture the identity’s three-dimensional structure.5

### **Dataset Composition and Environmental Stratification**

Images must be sourced from authentic media, such as full-resolution screenshots from Instagram Reels or 4K YouTube thumbnails, to capture the subject in natural motion and lighting.5 Faceswap outputs are strictly prohibited because they introduce skin-boundary artifacts and halo effects that the LoRA training will interpret as part of the identity, resulting in "plastic" or "edged" facial reconstructions.5

To ensure the avatar generalizes across the diverse scenarios required by the CMF pipeline, the dataset is stratified across three primary axes:

1. **Lighting Conditions**: The model must encounter the identity under hard daylight, soft studio arrays, warm indoor tungsten, and cool blue-hour outdoor light. This prevent the LoRA from associating the identity with a specific lighting setup.5  
2. **Expression Categories**: Following the facial individuation theory, the dataset includes neutral baselines, warmth/smiling, authority/seriousness, and contemplative states. Training on varied expressions facilitates better identity persistence when the model is asked to generate novel, unobserved expressions in production.14  
3. **View Angles**: A comprehensive map of the face includes frontal views, 3/4 profiles (left and right), and slight upward/downward pitches. This ensures the model learns the "Facial Proportion" (FP) in three-dimensional space.5

### **Augmentation via Synthetic Inpainting**

To augment a limited set of real photographs, FLUX inpainting can be utilized to generate 13 to 18 additional images.17 This process involves taking a high-resolution face from a real source image and placing it into a newly generated environment. The face region remains unmodified, but the surrounding pixels (hair, clothing, background, lighting) are varied. This technique effectively doubles the environmental diversity of the dataset without introducing the identity artifacts associated with faceswapping.17

### **Strategic Dataset Stratification Matrix**

| Category | Stratification Variable | Percentage of Total Dataset | Objective |
| :---- | :---- | :---- | :---- |
| **Lighting** | Hard Sunlight / High Contrast | 25% | Photometric resilience.5 |
| **Lighting** | Soft Studio / Neutral | 25% | Baseline texture detail.5 |
| **Expression** | Active (Smiling/Speaking) | 30% | Dynamic identity persistence.13 |
| **Expression** | Static (Neutral/Serious) | 20% | Structural grounding. |
| **Angle** | Frontal (0°) | 20% | Primary landmark mapping.5 |
| **Angle** | Profile / Side (45°-90°) | 40% | Depth and ear-to-eye ratio. |
| **Augmentation** | Synthetic Inpainting | 20% | Contextual generalization.17 |

## **Hyperparameter Stabilization and Training Configurations**

The stabilization of identity encoding in FLUX 2 requires precise control over the LoRA network's rank, alpha, and step count. For character identity, a standard configuration of Rank-16 and Alpha-8 has been shown to provide an optimal balance between learning capacity and memory efficiency.17 While higher ranks (e.g., Rank-32 or 64\) are often required for style LoRAs that must capture abstract concepts, character-specific adapters benefit from the tighter focus of lower ranks, which prevents the model from "memorizing" the background or clothing of the training images.19

The training is conducted on NVIDIA H100 hardware, utilizing an optimized pipeline for fast convergence.6 The learning rate is set at ![][image1] with a linear warmup over the first 100 steps to prevent gradient explosions in the early phase of adaptation.5 AdamW is the preferred optimizer, incorporating weight decay of 0.01 to improve the generalization of the learned weights.17

### **Optimization Benchmarks for NVIDIA H100 Training**

| Configuration Parameter | Value | Impact on Identity Persistence |
| :---- | :---- | :---- |
| **Model Version** | FLUX 2 Dev | Maximum available world knowledge (32B).3 |
| **LoRA Rank** | 16 | Prevents overfitting to training poses.19 |
| **LoRA Alpha** | 8 | Standard scaling for identity adapters.17 |
| **Learning Rate** | **![][image1]** | Optimal for fast convergence on H100s.5 |
| **Training Steps** | 1,200 \- 1,800 | Stability reached without memorization.16 |
| **Effective Batch Size** | 8 \- 16 | Controlled via gradient accumulation (micro-batch 1-2).20 |
| **Resolution** | 1024x1024 | Native 4MP scaling requires 1024 base for training.1 |

Training durations on an enterprise GPU typically range from 15 to 75 minutes, depending on the target step count and resolution.16 At $1.69 to $3.99 per hour for A100/H100 instances, the compute cost for a single coach's Brand Avatar LoRA is approximately $0.50 to $5.00, aligning with the $4 production delivery target.16

### **Captioning and Trigger Word Architecture**

To ensure the identity is correctly disentangled from the context, a specific captioning strategy is employed. Captions must be detailed and clinical, utilizing a trigger word (e.g., the coach's name or a unique ID) but avoiding generic descriptions like "a photo of a person." A standard caption follows the structure: ", a photo of, in \[LightingCondition\], with,".5 By explicitly labeling the variable factors (lighting, expression, angle), the model learns that these factors are separate from the subject's identity, allowing for flexible prompting at inference time.5

## **Multi-Reference Inference and CMF Pipeline Integration**

The primary utility of the Brand Avatar LoRA lies in its integration into the broader Coach-Marketing Framework. Once trained, the LoRA is applied at an inference weight of 0.4 to 0.5.18 This conservative weighting is crucial when stacking the identity LoRA with other adapters, such as scene-specific color grades (PAD color grades) or architectural styles.18

In the FLUX 2 architecture, stacking multiple LoRAs requires careful weight balancing. Experience suggests that the combined weight of all active LoRAs should stay below 1.1 to avoid "fuzzy" artifacts and image degradation.18 If the identity LoRA is used at 0.5, the remaining 0.6 weight budget is allocated to stylistic and environmental adapters.22

### **Native Multi-Reference Support in FLUX 2**

A distinct advantage of FLUX 2 is its native multi-reference support, allowing for the inclusion of up to 10 reference images in a single generation without external tools.1 In the CMF pipeline, this feature is utilized to "anchor" the LoRA's output. By providing real reference images of the coach during the text-to-image process, the model can cross-reference the LoRA’s learned weights with the ground-truth pixels of the reference images, further increasing the Identity Persistence Score (IPS).1

### **Strategic Inference Weight Configuration for CMF**

| LoRA Layer | Purpose | Recommended Weight |
| :---- | :---- | :---- |
| **Coach Identity LoRA** | Core facial identity persistence | 0.40 \- 0.55.18 |
| **PAD Color Grade** | Brand-specific aesthetic consistency | 0.20 \- 0.30.18 |
| **Somatic Hook** | Posture and body language alignment | 0.15 \- 0.25.22 |
| **Gaze Vector** | Control over eye contact and focus | 0.10 \- 0.20.23 |

## **Quantifiable Success Benchmarks and Validation**

Deployment of a Brand Avatar LoRA is contingent on meeting rigorous validation metrics. The Identity Persistence Score (IPS) is the primary metric, calculated as the cosine similarity between the CLIP embeddings of generated outputs and the original source images across five novel prompts.24 A production threshold of ![][image2] is required to ensure the coach is recognizable to their audience.

The Anti-Generic Specificity Scale (AGSS) Level 4 benchmark requires that the generated face remains a specific distance from the "generic professional portrait" cluster in the FLUX 2 latent space. This is measured via the Euclidean distance formula:

![][image3]  
Where ![][image4] represents the latent coordinates of the generated coach avatar and ![][image5] represents the centroid of the generic archetype.13 Maintaining a high ![][image6] ensures the preservation of idiosyncratic features like eyebrow density, mouth asymmetry, and the "biological bar codes" identified in Rossion’s research.9

### **Final Success Criteria Matrix**

1. **Identity Persistence Score (IPS)**: ![][image7] across 5 novel prompts (different lighting/angles).24  
2. **Skin Texture Authenticity (ST)**: Pore-level detail present in 100% of samples; no "AI smoothness".13  
3. **Expression Naturalness (EN)**: Average blind rater score of ![][image8] for realism and emotional resonance.13  
4. **Facial Proportion (FP)**: Deviation of ![][image9] from source image anatomical landmarks.13  
5. **Production Readiness**: Sub-10 second generation time for 2K resolution outputs on enterprise hardware.2

## **Future Outlook and Scalability**

The implementation of per-coach Brand Avatar LoRAs on FLUX 2 allows for the creation of high-volume, hyper-personalized content without the ongoing logistical burden of traditional photography. For the $50/week CMF subscription tier, the ability to generate 24 pieces of high-fidelity visual content at a marginal cost of $4 per coach constitutes a paradigm shift in brand management.6 As the FLUX 2 architecture continues to mature, and with the release of even larger vision-language models like the 32B Mistral-3, the gap between AI-generated and photographic content will continue to close, eventually rendering the "identity drift" failure mode obsolete through near-perfect latent space representations of the human face.1 The strategic use of horizontal orientation energy and diagnostic spatial frequency analysis ensures that these generative identities remain grounded in the same biological markers that have guided human recognition for millennia.8

#### **Sources des citations**

1. Flux 1 vs Flux 2: The Detailed Upgrade Guide for Creators \- SeaArt AI, consulté le mars 27, 2026, [https://www.seaart.ai/blog/flux-1-vs-flux-2](https://www.seaart.ai/blog/flux-1-vs-flux-2)  
2. FLUX.2: What It Is & How To Use It In LTX | LTX Studio, consulté le mars 27, 2026, [https://ltx.studio/blog/flux-2-in-ltx](https://ltx.studio/blog/flux-2-in-ltx)  
3. What is FLUX and How to Use It for Image Generation \- MindStudio, consulté le mars 27, 2026, [https://www.mindstudio.ai/blog/flux](https://www.mindstudio.ai/blog/flux)  
4. Diffusers welcomes FLUX-2 \- Hugging Face, consulté le mars 27, 2026, [https://huggingface.co/blog/flux-2](https://huggingface.co/blog/flux-2)  
5. Training a Personal LoRA on Replicate Using FLUX.1-dev \- Pelayo Arbués, consulté le mars 27, 2026, [https://www.pelayoarbues.com/notes/Training-a-Personal-LoRA-on-Replicate-Using-FLUX.1-dev](https://www.pelayoarbues.com/notes/Training-a-Personal-LoRA-on-Replicate-Using-FLUX.1-dev)  
6. Train FLUX LoRA Fast | 10x Faster AI Model Training \- Fal.ai, consulté le mars 27, 2026, [https://fal.ai/models/fal-ai/flux-lora-fast-training](https://fal.ai/models/fal-ai/flux-lora-fast-training)  
7. Effects of Age on Face Perception: Reduced Eye Region Discrimination Ability but Intact Holistic Processing \- Boston University, consulté le mars 27, 2026, [https://www.bu.edu/ballab/pubs/Fry22023.pdf](https://www.bu.edu/ballab/pubs/Fry22023.pdf)  
8. A face detection bias for horizontal orientations develops in middle childhood \- Frontiers, consulté le mars 27, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00772/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2015.00772/full)  
9. (PDF) Biological "bar codes" in human faces \- ResearchGate, consulté le mars 27, 2026, [https://www.researchgate.net/publication/26815696\_Biological\_bar\_codes\_in\_human\_faces](https://www.researchgate.net/publication/26815696_Biological_bar_codes_in_human_faces)  
10. The role of horizontal facial structure on the N170 and N250 | Request PDF \- ResearchGate, consulté le mars 27, 2026, [https://www.researchgate.net/publication/323916518\_The\_role\_of\_horizontal\_facial\_structure\_on\_the\_N170\_and\_N250](https://www.researchgate.net/publication/323916518_The_role_of_horizontal_facial_structure_on_the_N170_and_N250)  
11. An implicit neural familiar face identity recognition response across widely variable natural views in the human brain \- ResearchGate, consulté le mars 27, 2026, [https://www.researchgate.net/publication/338728902\_An\_implicit\_neural\_familiar\_face\_identity\_recognition\_response\_across\_widely\_variable\_natural\_views\_in\_the\_human\_brain](https://www.researchgate.net/publication/338728902_An_implicit_neural_familiar_face_identity_recognition_response_across_widely_variable_natural_views_in_the_human_brain)  
12. Three-Month-Old Infants' Sensitivity to Horizontal Information Within Faces \- ResearchGate, consulté le mars 27, 2026, [https://www.researchgate.net/publication/301620987\_Three-Month-Old\_Infants'\_Sensitivity\_to\_Horizontal\_Information\_Within\_Faces](https://www.researchgate.net/publication/301620987_Three-Month-Old_Infants'_Sensitivity_to_Horizontal_Information_Within_Faces)  
13. Which Visual Features Influence Perceived Authenticity in AI-Generated Portrait Photography? A Mixed-Methods Study \- IEEE Xplore, consulté le mars 27, 2026, [https://ieeexplore.ieee.org/iel8/6287639/10820123/11222595.pdf](https://ieeexplore.ieee.org/iel8/6287639/10820123/11222595.pdf)  
14. Which Visual Features Influence Perceived Authenticity in AI ..., consulté le mars 27, 2026, [https://ieeexplore.ieee.org/document/11222595/](https://ieeexplore.ieee.org/document/11222595/)  
15. FLUX.2: Analyzing and Enhancing the Latent ... \- Black Forest Labs, consulté le mars 27, 2026, [https://bfl.ai/research/representation-comparison](https://bfl.ai/research/representation-comparison)  
16. Fine-tuning Flux.1-dev LoRA on yourself \- lessons learned : r/StableDiffusion \- Reddit, consulté le mars 27, 2026, [https://www.reddit.com/r/StableDiffusion/comments/1etszmo/finetuning\_flux1dev\_lora\_on\_yourself\_lessons/](https://www.reddit.com/r/StableDiffusion/comments/1etszmo/finetuning_flux1dev_lora_on_yourself_lessons/)  
17. Flux Lora Training \- RunDiffusion, consulté le mars 27, 2026, [https://www.rundiffusion.com/flux-lora-training](https://www.rundiffusion.com/flux-lora-training)  
18. Flux LoRa stacking question : r/FluxAI \- Reddit, consulté le mars 27, 2026, [https://www.reddit.com/r/FluxAI/comments/1ibxq07/flux\_lora\_stacking\_question/](https://www.reddit.com/r/FluxAI/comments/1ibxq07/flux_lora_stacking_question/)  
19. Fine-tuning a FLUX.1-dev style LoRA \- Modal, consulté le mars 27, 2026, [https://modal.com/blog/fine-tuning-flux-style-lora](https://modal.com/blog/fine-tuning-flux-style-lora)  
20. Diffusion Model Lora Training on Large Datasets \- Hugging Face Forums, consulté le mars 27, 2026, [https://discuss.huggingface.co/t/diffusion-model-lora-training-on-large-datasets/169431](https://discuss.huggingface.co/t/diffusion-model-lora-training-on-large-datasets/169431)  
21. 1-hour to train 1500 Flux Dev Lora on a 4090 (is this normal?) : r/StableDiffusion \- Reddit, consulté le mars 27, 2026, [https://www.reddit.com/r/StableDiffusion/comments/1g20png/1hour\_to\_train\_1500\_flux\_dev\_lora\_on\_a\_4090\_is/](https://www.reddit.com/r/StableDiffusion/comments/1g20png/1hour_to_train_1500_flux_dev_lora_on_a_4090_is/)  
22. Multiple stacked LORA? : r/StableDiffusion \- Reddit, consulté le mars 27, 2026, [https://www.reddit.com/r/StableDiffusion/comments/1g5sxyg/multiple\_stacked\_lora/](https://www.reddit.com/r/StableDiffusion/comments/1g5sxyg/multiple_stacked_lora/)  
23. When stacking LORAs, is there a "Maximum" weight total for FLUX and SDXL? \- Reddit, consulté le mars 27, 2026, [https://www.reddit.com/r/StableDiffusion/comments/1jyj18e/when\_stacking\_loras\_is\_there\_a\_maximum\_weight/](https://www.reddit.com/r/StableDiffusion/comments/1jyj18e/when_stacking_loras_is_there_a_maximum_weight/)  
24. Person Knowledge and Facial Identity Perception \- OSF, consulté le mars 27, 2026, [https://osf.io/preprints/psyarxiv/sdup8/download?utm\_source=consensus](https://osf.io/preprints/psyarxiv/sdup8/download?utm_source=consensus)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAATCAYAAADI876sAAAA9ElEQVR4Xu3VsQpBURzH8b/BIAMZRCk3WWyK1WaRTZ6AlNGm5AU8gixKyiaDJ/AkVouFQQZ+p3vk+EfdazrnnvOtz3LPXf6dc+4lcrmsLgYjGPKFqNeAG4z5QtSzbvCCtIMrWTJ4HGZSG44UbPASTCHBF2QpmECaL+hSB3pSnoIPLmrCnPwh1XKwhAp7rk0e+Tstdl0IO7ioDivI0PvKrKGsvqRTryPuKc/+GVxUhT1speLnsl71YQFdxQDO5O9Yi37fX55Rg4v7pw4tiJ2+U7jBjTvq36pRuN+ZsR83nlWDJ2EjneABFzhAVnmPZ/x/3OWKcE9L9TECGxvZQwAAAABJRU5ErkJggg==>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAAAXCAYAAAD0v0pBAAAEQElEQVR4Xu2Ya6hmUxjHHxmFcUkGyTDjlobCZIyScpIPJJdQxmUmmZhRzJdJNEmjSbmmJHJLFMo1IQZpzEgYjUzDBzWFNEKIUO7+P8+z5l17nb33u1/njCPtf/16z9l7vWfvtZ5n/Z9nHbNevXr1+k9omlgm7q3h1GzcjuKqoByXWCx2S1/INNP8/ubgLjFX3BjwDv+2dhBHiPnmc+uiQ8W+5cUG7SJOEAcH21dvD7Sd2NN8seFncbv5g/gj5ThYJP4Ul8c4OEq8ID4SswLE5xvi5PgdnSa+F1cHTbrUPDlgenFvIpoj3hLLxWXibTGvMqJeD5nPu4mUsBeIx8QCcV2wzgZrUqslwR9WXaw63SC+Np9IrmPFT+b3gSx7XFyRD5J2FavNMwSaRNCPDJ4RN5knwD/VTsFzVn2nU8QGsXd2rRQJ8LR42Mbv/DXxyXwPE3fHz7kuEo9ay27vAzCFAWCiDwafmXt2nfBKwGrYUixkrjPMt2IKAAEiUKfng8ytjWftF3QVk2Nr3yH2L+510THBF1YNPO/5lVVrXql9xC1WXUACBiRZWjPm+pJ5oHORnASw1kr3EOsDFrepKPEQIEgsQi6CeKf41rzAApP9UawVh8SYNJbg8ZmujaIDxX3iCfOgdNXZAe/EuyVRwz6x9npEEc0Tjgy/NTguu57m/Kr5WvE9ICGXZuMqSl+CFcW9XFgTYFNMJIkHnC++K66T6S/boEj9YL5wTTtsVLFwBP15cXjQplT0mwJwf3ZtmM4R1wZ5ErFDuMZ8fxHvBdfYeFvaqgvNF3WY/xMcYNw75t4H74rbrL5Foy29Xnxsg0Bssna/7SoCf5J4RVwStO2oYQGgy+ki6hCJlSyt1AHmNvSbDeb8ppidjdmq5P/YyjD/x54Aq8K2RtXu4gHxq7UX32Eik2jxWAQ+GzOr0GQFgGeSRDOCXNQT2m7OGCQfZx4gCGus2tr/Lf7ABzZY3Cb/P0h8HgzbqnQVULebWHiKYF3mDBOFjSx/TZxpLYebBk2kBiRhMTQCeDwFtSyq1Ma8w0p17jzzhoRiXFHy/9S5NCl5P2BZbbo5OLG8Yf5dDkHshi5Kk+QwxrbGckZd+KRkGd9YNTk4RNI80MUNU0rYut2SXKLs+lDeeleU/D8V2CYRHE6vwAs3iQfRosIqq3ryXubbkwLWRReLJwPOAm3+3kXpHEAgy3PA++atJkpdHIHi7JErtdZ1AUArzS29tEW6wBctq30LxafmlRp/+jJ4ROycBklXmteG32McbLHxL5bECz4V3GO+VRebZ/BG8+dOdCEnKv7t8KG5LYyZNxT5GSAPwPLsOiL5SMImG2Zncy541rxWMG94XRydjdtmIsvpEgCRVWzJMWuuL1Mh3mUsGOW9SB7+gVcW31yMmS3OMg82lDtim6kPwBQHYDI1S5zbkeODqba3/5X6APTq1avX5OsvdGwGIpi39PEAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,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>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAaCAYAAACO5M0mAAAAy0lEQVR4Xu3RPQtBcRgF8EcZ5CWKEpnMSpLVZFE2izLaDJSvYPMZfAGyWmRQymL1tpp9Cee453IT5ZZMTv2W557b/7n3b/bPzxOAKrQkDGXoS8YtFqAHE9lCByqygByLHJZgLkNzTonKCtosxiALR6lxiKRkDwNfRYa7nCSvWVEu9nj5tsNSIp4Z8ZS0ZjaGmQQhbs7XUtMtccc1bGQEU+gK/4C/Ipc/mHMblICQ+9CbOuzs8TvehgufoSH8mJfhpVNS7js95+Pid3MFEOsqlQwWoAQAAAAASUVORK5CYII=>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAkAAAAZCAYAAADjRwSLAAAAwUlEQVR4Xu3QrQoCQRiF4TEIIgZNIoiiQTAZBdFm8Rq8C21GwWYSbDavweItmI02f7pgMAi+x/0Gdteyi9UDT5jZj5mz49w/aZNBy4wxQB79VENZLLE1dczwwMoPTXFE2Sg1XFxwqmvgjIV99BniirYWI7xsMxxdd0BJiwluaIYGcti5UB+dcELVb5CuC0p/+iiJhvT7a2wwN+pyR8cP+RRRMJHS8aiwL62Tv6L30KvLE3v0IhMuuK4So71IEg39ljfERSJsoa4VwwAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADUAAAAYCAYAAABa1LWYAAADKklEQVR4Xu2XS6iNURTHl1Dk/U55RFKSvEKKiSgSeQwolIkYiCKPlIgMlIFId2KCxEAZiIgiBkQJxUAk5REyUZQB+f/uXtvZ3z7fcU5u7ql7/evX7dtnf/vba+312Nfsvzq+uohlTntro5iSDzai3mKfuCfOi17Fn22lOCq6ZePtoX6iRYzOf6inDmlUVzFG3BXHkvGRzmX/2yzNFRctOB8a1gjxRqxJxvYnNFM9xSWxwmlY88U7McGfB4v7zpw4qYmiYJxzStOAajbe2WrBoL3igRjgczDkiTPMx6L6ivViuoUPwCyxXYyrTGtYg8Ryh/ztI6aJIcmcGeKhk+/Huosj4oxDAu4RP8XJZB5heMtJ4xgDDlko7y/ETWetmGSh2Cz9Pbu+FlvYKE6BeeK1eGwhWqJIj+hknFkQ3nxqwdpo8Sjx1or5tEucclIRnpzqZPFJrHKimH/BaoRIpqnig1iYjFG0qMD5GsMtGAtLkvHWCkcxwNOpCD82yEajahnVw8LJ4QDWwoOAaAU3nLwt5GLD5Eca8ojTwenkUKrOZRQP5A5GpCKn8sVrGRVFP6N/YSSgseK9/1ZPhP5Lq55LQfho1RW3plHbLHyUj0exITZHkeDFGN8YxXjceCqMxwk4IxUF4puYnY2Xiaj4YsU8RpwQJ5UWCcTenjkFgzkhvBPDBVFxvlpYnISPXuDvHYcSm4pi8VlsTsa4zlwXOy20DMLrtIWwnuikimEWmynvw22rLhIIJzx3Yi9tFeX8hIVTOeCQX4QYJ3LcwsKIFx856ckiHIAjKOWcPtDxd1j4BmJTLRbCnbINuTAIp20R15zvFtbLtcgq7aP0qtTfivcoPDvQKhtCXE2uOKuTcRTziWKAxyF9NxWbqWUUIrRpvrFPleUT4pukBLRJeBLOWmXTMZ/yClomnEU4cuqFkCkRuQSkR+yfUTxftVC9oU3CECAsF1g4kYPih4WQxbN/0kwLzR7joExEyAbxyuH+uc5CpCDe2y02+XOb1SGNior/qHEBprRGShM2ETlXK9eiyKl0TRhq4bqEqNiHrf46fyUWrXdL+BeinUQDO4d+AY5PsdH+9uwCAAAAAElFTkSuQmCC>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADcAAAAWCAYAAABkKwTVAAACfElEQVR4Xu2XS6hNURjH//KIvCMS5ZEBUgaKmCjllcdACqHUnXrkCqUMDGQgKYQMCEl5leSRZEIGTEyk3GugbpkxMub/b33fOWuve9be57huctu/+nXOXXvvu9f3fWt9ex+gpqbmXzCKDksHB8gE8yC9Sk/QGYUzWrOEXqbbzMWmrpWT7DzNdzk9Ty+ZG+lwO95gFX1E99Kx5kCYRt+a2xEmspK+obOj81qxlf4q8bCdt4cep2PoSFN/X7HvDYZ0cMLLfN88TacUzmifffS1Od7G9P9v04v2PUc33YzmMnS30HMIE59Kn9h4zGT6AmFplzIXYa/coYtQPqEYVf0lvWHGHKMfESaX4whC5R1VWmofTrSx6bSHnkSonDMT4d76bAtVTzd8TlejxYZN0I2/IB/cNzovGc+hKp01l0XjSvRRhGXaS3eatxCaSseo5A/oNYTuKluhpfIV+eB+0qXJeI7d9IKZrhwl+RSK+/EpnRWfVIUmewYhK+0sz78VnJagGtIGM0ZzUGO5ThfQh6YC/IySpqULpQJRQAos3bhlaD9pX+WC60N72V1PvyMkIk3GCvoKzYbnc15HfyA0pQIqs/bUY/MA/uyRMAKh26qbydHRMT1w3yMs8Sq05LQCvFvG7Ef/xDm6TvdpsBahrP6Er2oaVexAqJ5UgxHqampKqp5Q9d6ZejwoKY4nKBdcWjlHDegmXRMPKpiqvdQJuolat9SjRK9PWt530WznCu6TeQ/FCvvjRF1XyfEEOb7nPtAuust8Rg/Z8QZDOrjBwDf5HLrJPju5qTre/HQwQYnSlnI9cQUWovkWXqXeEX3i/wXj0P9dLqf/5KipGSR+A3jxj7nh4yByAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFAAAAAWCAYAAABXEBvcAAADb0lEQVR4Xu2YW6hNQRjHP7nkfolIKYdIpCRHIiJJ5PIgOsLDiVwehBSiJEquL6QIKUnkmlCUosgD5U2eFKWUByIepPD/mRl79uy19lnn5lL7X7/O3rPWnDXzn+/7ZvYyq6mmmmr6Z9RJ7BID0gvtrS6iQ9rYhuJ/bxLr0gs56i02ipOenWJw2R3ZGiv2WGkuU8QSMcTD/+AextLX31NNo8RBc2NYJrp5KlQzMFuFDZwubohGT4/4YhtomvgqtqUXMjRQPBYN5owAjHgkhkb3ZWm9mBx953k/Ej6KudE9eZolnokRoqPYLk54Okf3/RYDneS5IvaJ/mV3tEysPIvzxYoZiAkPRa+ojbGdF8f85yz1EUf93yCeR/Qu9tRbzuQTEWV3xI6ojXm89MyJ2nM1zFzoXhBjLH/g1cRgD4h54rU1bSCRf0+cTS+Y6/vc8jcIJrU2aaPPgqStiMaJT1bet6d44GGhCoso3GJuRWaaC2cookVipbnaU8TAQeZWOM/At2J40h7SfH/GNfpQd3d7bok1llPHIpHipHuegWQoO36z1E9cFWc8bDx5qvMQfURhUQPDfXkGUgYmJO1kChy2yklhAKnPpgQsPKWJKI9TPRX9qhkIfC8kJnVInLNSKkOeQtpCnW9rTwNJW8iqSyxyWvMmis9iVdIeq9UGYhBmYRrmFTlCBDGwU55QvFeLD+aigfTISyHqG3Uuz8A35op5EJM47klrI9E21Sp3bhaAhTidtMdiB/5u+QYyj4og4oHUOLgpNljLjjOjrWRcgMl/s6YNJAWpL7dF1+QahfupuVISxJFlqydV2Ajuiu4eFAzc679niVpKvY03pbC4UNF3trhmbreEoptEUYVBxykcDrdPzB1PQv1aam6QbChB4VgR9ycCODRzMIZU9GchRibtjVZeCjCassHhGhBj4fTBuEKk8YxwjEnLyC/DKkKyDUQEXxTvzNUUag9nPA7LwcAX4rKVIo6aRUoygWAOZeSSlRd+DDpiVX4dmAuG62K5Z7N4JRZaab7jxXsr1e0gUp+IJxMx7L65MypUeFUzsJUG/mtigHVivofP6aAbPE2JRaREwQyrrK3VxGLWm+tb7diTWfjz4HcppBP6k6JGUcjjOvlXxRbNUaUIvMUo8iajPUVax29damqmVlj5W5ea/lf9BP1KwAvqYcl0AAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAXCAYAAAB0zH1SAAACS0lEQVR4Xu2WzYvNURjHH6GIYqKMvEXKa2nyVjJNiSyk5KUkbCg2hhBFSmFhxmKMhZKFjURiIS8LjcnGxpY1ZWPDn8D30/Oc+d17Zu793TsmY3K/9anfPef87nnO83Z+Zi219M9rkjgSvBHPxMaqFa6pQY9Yl82Ni/6q4Ww2Ix+sofnBFXFPnIvfSevFh2CemCPei/tiu1goDoiPwQXz/ZvSZLFLvBAnxJSgljaJOwEGwEPxM+bQWTEYzIyxbrFCLBZd5mvvBmlNQ8K7x8SA2GMesjJxoCdWGJW8vFR8Ey/FNHGxYk0y6qR5JBB73RbLg1KlEPeKp2KzNRcijHouvgd4EGHcoPhq/v8HxbuAOQ7MnqQNwvukSl1h2GrxSPQHi6pWNCe8RbQq62GB+GJeiNPFLHPvw2FxSJwxt4UUuWkNRPi0+CRW5hNjKNLghxU5jjgA7BBbzWuJA1HM1AWHIHXgkhXRG9KENRyRGqQI6QKkTjO5XU8Y+1lsyycysd910Rm/95kfAtrMe3lHzA1Tyk2Kg/bHZnhitNpgXpSrsvGRtNuKPE/FvDdAa8X5eK4rioM2+EocNQ9ro0ptjAulPcZwyC1z7+VaYt6vSRVE56EDcRhIY9fiuSHhAdriY3HKyi8gjHgbHBf7A4x+YMPfTVf6moqxueZ1V2n4MvNUGpXyTXPh1dfiVw1uFEuHxCWX92yc1SeuBojevzOex1V4EC7byD07pRbwTcNtW7WOwknhLGOLuTfGquP8kSas4bSe9I1Sxux4p6X/Sr8Byy9ri9iXspgAAAAASUVORK5CYII=>