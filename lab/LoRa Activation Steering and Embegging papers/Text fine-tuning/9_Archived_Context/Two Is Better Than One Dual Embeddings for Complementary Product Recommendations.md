# Two Is Better Than One: Dual Embeddings for Complementary Product Recommendations

Giorgi Kvernadze [1][§], Putu Ayu G. Sudyanti [1][§], Nishan Subedi [1], Mohammad Hajiaghayi [1,2]

1 Overstock.com Inc., Salt Lake City, USA
2 University of Maryland, College Park, USA
giorgi.csv@gmail.com, pasudyan@gmail.com, nishansubedi@gmail.com, hajiaghayi@gmail.com



Abstract—Embedding based product recommendations have
gained popularity in recent years due to its ability to easily
integrate to large-scale systems and allowing nearest neighbor
searches in real-time. The bulk of studies in this area has predominantly been focused on similar item recommendations. Research
on complementary item recommendations, on the other hand, still
remains considerably under-explored. We define similar items as
items that are interchangeable in terms of their utility and complementary items as items that serve different purposes, yet are
compatible when used with one another. In this paper, we apply
a novel approach to finding complementary items by leveraging
dual embedding representations for products. We demonstrate
that the notion of relatedness discovered in NLP for skip-gram
negative sampling (SGNS) models translates effectively to the
concept of complementarity when training item representations
using co-purchase data. Since sparsity of purchase data is a major
challenge in real-world scenarios, we further augment the model
using synthetic samples to extend coverage. This allows the model
to provide complementary recommendations for items that do not
share co-purchase data by leveraging other abundantly available
data modalities such as images, text, clicks etc. We establish
the effectiveness of our approach in improving both coverage
and quality of recommendations on real world data for a major
online retail company. We further show the importance of task
specific hyperparameter tuning in training SGNS. Our model is
effective yet simple to implement, making it a great candidate
for generating complementary item recommendations at any ecommerce website.
Index Terms—Recommendation Systems, Candidate Retrieval,
Complementary Product Recommendations, SGNS, Representation Learning


I. INTRODUCTION


Product recommendations have become one of the most
important tools in e-commerce for product discovery, and have
proven to drive significantly increased sales in various settings.
A study conducted by Barilliance Research estimated that up
to 31% of total website revenue and, on average, 12% of sales
were associated with product recommendations. For website
users that clicked on recommended items, they were five times
more likely to make a purchase than those who did not.
Additionally, recommendation systems provide a better overall
customer experience, which leads to better retention rates. In
general, we encounter two different types of recommendations:
similar and complementary recommendations. Similar product
recommendation provides relevant items that have identical
functionality (e.g. brown sofas and black sofas). Due to its


§Co-first authors.



interchangeability, customers often purchase one over the
other, but would rarely purchase both. The goal of showing this
type of recommendation is then to convince users to eventually
make a purchase by providing a diverse set of related items
to their original intended product of interest. On the other
hand, complementary product recommendation aims to suggest
products that serve a different purpose but are compatible
when used in conjunction (e.g. mattresses and mattress pads).
This type of recommendation has been shown to contribute
significantly to increasing conversion as well as average order
value in e-commerce websites. Both types can be customized
at the user level, creating more personalized recommendations
for each user based on their past interactions with the website
(e.g. purchases, browsing, add-to-carts, etc.).
We focus our attention on the generation of complementary
recommendations. Extensive research has been done in the
area of similar product recommendation from the classic
collaborative filtering methods [13, 19, 31], to the widely
implemented matrix factorization model [20, 29, 41], and
most recently, to the use of vector representation learned
from different data modalities through various neural network
architecture [2, 15, 25]. While there is substantial research in
the area of similarity recommendation, limited work can be
found for complementary recommendations. As we discuss
below, the problem of finding products that are complementary to each other is an inherently more difficult task than
finding items that are interchangeable in nature. Unlike similar
product recommendation, complementary products adheres to
additional rules such as asymmetry where the direction of the
recommendations is typically relevant in its evaluation. One
example would be phones and screen protectors. Customers
who purchase a phone would likely be interested in buying
screen protectors, however, they would rarely purchase a
phone when looking to buy screen protectors. Additionally, the
transitive property between the recommended products does
not always hold in complementary relationship. A coffee table
would be a good complementary item for a sofa, a coaster is
a good complementary item for a coffee table, but a coaster
would be less relevant to a sofa.
The earliest work in discovering complementary relationships centered upon mining historical purchases to find patterns of products that are frequently bought together while
accounting for other additional measures [1]. Although simple,
effective, and interpretable, this method suffers from ineffi


1


ciencies in large data sets as well as the cold-start problem for
items that were never purchased. Another approach is through
the use of a supervised learning methods. Manually labeled
sets of products can be used as positive examples that are feed
into a classifier to build models that learn to identify patterns of
complementarity between pairs of products [2]. One advantage
of this approach is that it allows learning from different sources
of data. However, human labeled data is expensive to obtain
and thus sparsely available, leading to limitations in training
certain models. For this reason, most studies substitute the use
of human labeled data with historical customers’ behavior data
such as co-purchases, views, and co-clicks [25]. These labels
come with their own noise and biases, but as we show in this
paper, a careful pre-processing of the data can alleviate some
of these issues.
A related line of research on complementary recommendations involves the bundling of a set of products, where business
components such as price and discount savings as well as other
constraints are contributing factors in the optimization of the
models [4, 42]. These studies are disparate from our goal of
solely focusing on finding complementary relationships between goods without constraints on factors such as discounts.
We concentrate on the latent representation approach to
producing complementary recommendations. Representation
learning has been widely applied to predict similarity between items. This framework uses low-dimensional vectors
to summarize information about an entity. These vectors can
be generated from different data modalities such as images

[25], text [24], or any other relevant signals. One of the most
commonly used models for learning vector representations for
products is the Prod2Vec model [5, 15], it has gained attention
as a method for product recommendations due to its simplicity,
efficiency, and effectiveness. The main idea behind this model
is to use the Word2Vec algorithm [26, 27] on sequences of
products. The Word2Vec model uses a shallow neural network
architecture to learn low-dimensional vector representation of
words from sequences of text, such that semantically similar
words are placed close to each other in the embedding space.
In the Prod2Vec model, the sequences of words translate to
sequences of user actions on products, e.g., clicks, add-tocarts, purchases etc. A model trained on such data will learn to
represent products in a lower-dimensional space that captures
certain semantic relationships between products. For example,
if two products often appear in similar contexts, the vectors
representing these products will lie close to each other in
the embedding space. This effectively reduces the problem
of producing similar items recommendations to a nearest
neighbor search using simple distance functions like inner
product or cosine similarity. The existence of numerous fast
approximate nearest neighbor search algorithms [14, 32, 38]
makes this method particularly attractive, since it can scale
to large datasets, even in settings where inference is done in
real-time.
While finding substitute items is a straightforward procedure
using the Prod2Vec model, it is not as clear whether we
can produce complementary recommendations in the same



manner. If we train the model on sequences of products that
reflect complementary relationships, commonly found in copurchase data, the assumption is that these relationships will
be uncovered in the resulting embedding space. However, we
show in this paper that the process is more involved. The
Word2Vec architecture produces two weight matrices: the input
and output matrix. In practice, only one of these matrices is
being used (input) as the vector representation of the entities.
Several studies [3, 28] in NLP have found that the dot product
between two word embeddings from the two different matrices
provides an indicator for relatedness, whereas that of the
same matrix provides a measure of similarity. In this paper,
we explore this relationship as we translate relatedness in
NLP to complementarity in recommendation systems. Our
contribution is threefold:
1) We describe a simple at-inference-time adaptation of
SGNS that transforms the model into a highly efficient
and effective complementary product candidate retrieval
method.
2) We introduce a practical data augmentation method for
overcoming the challenge of coverage, often encountered
when dealing with purchase data. This allows the model
to provide complementary candidate sets for items that
do not share co-purchase data by utilizing similarity
measurements derived from other types of abundantly
available data sources, such as clicks or product metadata.
Our results show that our method not only substantially
expands the coverage, but also improves the relevancy of
the candidates.
3) We show the importance of tuning the hyperparameters
of SGNS as opposed to using the default hyperparameters
passed down from the original implementation [27]. We
show an upwards of 300% improvement on relevant metrics when tuning the hyperparameters on the appropriate
downstream task.

In the next section, we will discuss related research in
the area. In Section IV we present our proposed method
followed by experimentation and results in Section V. Lastly,
we will summarize and conclude our finding in the final
section (Section VI) of this paper.


II. RELATED LITERATURE

Since the introduction of the Word2Vec model [26, 27], a
variety of models have been proposed for its adaptation to
recommender systems. The Prod2Vec and bagged-Prod2Vec

[15] were among the first models proposing this adoption,
where email receipts of purchases were used to create a
sequence of products for learning product vector representation
for recommendation. A variation of that which involves textual
information of the products were introduced in [35]. Graphbased approaches [16, 37] were proposed by incorporating the
network structure between different entities (products, users,
taxonomy, etc.) and learning the latent space from random
walks sampled from the distribution of this network.
While the majority of the literature focuses on generating
similar recommendations under the Prod2Vec framework, very



2


little has been done on exploring how the model performs in
generating complimentary recommendations. One study that
has attempted to do this in the grocery shopping domain is the
Triple2Vec model [36]. The authors proposed creating triplets
of (item, item, user) from the user shopping basket to recover
the complementary, compatibility, and loyalty relationship of
products and users. However, the paper failed to explore the
relationship between the two resulting matrices from the model
and resort to the conventional method of using one matrix as
embeddings while discarding the other. Additionally, it does
not mention ways of tackling the cold-start problem for items
that were never purchased.
BB2vec [34] proposed the use of baskets and browsing
session data to create the product embeddings. A multi-task
learning layer were used on top of the learned representation
and assumed some representations are shared between learning
tasks, which represent different types of data sources (browsing and baskets). While the author touched upon the use of
both resulting matrices from the model, there were limited
explanation of why this mechanism works. Further, multi-task
learning can be difficult to train, especially on browsing data
that are inherently noisy.
Other studies such as [9] demonstrated the use of both
types of matrices to compute complementarity between two
products. Again, the authors failed to provide explanation on
why this method works in finding the complementary relationship. We seek to fill this void in the literature by providing
a thorough explanation backed by experiments conducted on
two real world data sets from major online retail companies.


III. RELATED MODELS


In the following section we first briefly introduce the Skipgram model made popular by Word2Vec, we then describe
how we adapt the model to our specific problem. Finally,
we show how the model can be used to infer complementary
relationships.


A. Prod2Vec: Product Representation Learning


The Skip-gram model was first introduced in NLP as a
technique to learn vector representations of words, but has
since been adopted into various other domains [10, 12, 15, 35].
In e-commerce, it can be used to learn low dimensional
product representations by training the model on a sequence
of user actions e.g. clicks, add-to-cart, purchases, add-to-wishlist etc. The training objective of Skip-gram is to learn to
represent items in such a way that it becomes a good predictor
of its surrounding items in a sequence. More formally, given a
collection of sequences S, where each sequence is composed
of products p in the vocabulary P, the objective is to maximize
the log-likelihood:



the context window. The conditional probability of observing
a context product given a target product is computed as:

P(pc | pt) = �|Pexp ( | vp [T] t [·][ v] p′ c [)] ′ (2)
m=1 [exp (][v] p [T] t [·][ v] m [)]

where vp, vp′ [∈] [R][d] [are] [the] [d] [dimensional] [input] [and] [output]
vectors for the product p. Computing the normalization factor
of the conditional probability can be expensive with large
vocabularies. A popular approach is to instead optimize a
different objective function that approximates the softmax
introduced by Mikolov et al. [27]. The resulting model for
P(pc | pt) is often referred to as Skip-gram with negative
sampling or SGNS for short and is defined as follows:



′
log σ(vp [T] t [·][ v] pc [) +]



�k ′

Epi∼N (p) log σ(−vp [T] t [·][ v] pi [)] (3)
i=1



In order to simplify both the data pre-processing and
training procedure, we process the purchase sequences into
purchase pairs by taking all pairwise combinations in each
session. That is, for a given session s = {p1, p2, p3, ..., pn}
we take the Cartesian product with itself s × s = {(pi, pj) |
pi ∈ s, pj ∈ s, pi = pj}. By doing this with each session,
we get a new pairwise co-purchase data D and the objective
function defined in (1) becomes:


   


arg max
Win,Wout



log P(pi | pj) + log P(pj | pi) (4)

(pi,pj )∈D






pi∈s




 
log P(pi+j | pi) (1)

−w≤j≤w,w=0



Having the data defined in this form allows us more
flexibility with filtering based on heuristics, e.g. removing
pairs that have identical taxonomy hierarchies or removing
pairs that do not have a strong enough connection in terms
of co-occurrences (more on this in a later chapter about data
preprocessing in Section V-C). It also allows us to discard
the hyperparameter w, since context window size is no longer
relevant.


B. Dual Embedding Model for Relatedness


The feed forward neural network architecture of the
Word2Vec model consist of two different weight matrices: the
input (word) and output (context) matrix. Once training is
completed and the model is optimized, the common practice
is to discard the output matrix and use the input matrix as
the final product embeddings. Subsequent similarity search
tasks between products are then performed through the vector
representation of each product in this embedding space. Even
though this works effectively in practice, little is known on the
additional information uncovered on the distribution of joint
behavior of these two matrices. Simple combination of the
two vectors such as concatenation, addition [30], or averages

[21] have been investigated, more thorough studies are still
needed to prove its significance in boosting performance over
using the standalone input matrix. On the other hand, multiple
studies in NLP have found evidence to support that using the
input vectors as word embeddings predicts better similarity,



arg max
Win,Wout






s∈S



Where Win and Wout are the input and output embeddings
respectively and w is a hyperparameter defining the size of



3


while using a combination of the two vectors resulted in improved relatedness between words. An example of pairs with
high similarity score would be ”sea” and ”ocean”, and pairs
with high relatedness score would be ”ocean” and ”coast”.
The Dual Embedding Space Model (DESM) [28] explores
this relationship for search and document retrieval task. The
authors investigated the relatedness aspect between a query
word and all the terms in the document. They found that by
using both the input and the output representations jointly, they
were able to better rank the aboutness aspect of a document
with respect to a query term. The authors discovered that the
embeddings of words in the input vector space tend to be
closer to the output vector representation of words that would
co-occur together. This mean that the cosine similarity between
words amongst the input-input and output-output vector space
are higher for words that are functionally similar, whereas
in cross-vector relationship, input to output vector space, the
similarity are higher for words that appear together often in the
training sample. One of their example was for the word ”Yale”.
The neighborhood of the input vector of ”Yale” in the input
vector space corresponds to words like ”Harvard”, ”NYU”,
”Tulane”, and ”Tufts” which are words that would be found
in a similar context to the query word ”Yale”. A comparable
pattern was found for the output vector in the neighborhood
of the output vector space. In contrast, if we look at the
neighborhood of the input vector of the word ”Yale” in the
output vector space, they find words like ”faculty”, ”alumni”,
and ”graduate” which are related to the query word and would
appear together in a sentence but would not be used in the
same context.
Another relevant study in support of the idea of using
both the input and output embeddings to measure relatedness
between words was done by Asr et al. [3]. The authors used
two distinct word data sets, where one was designed for
participants to exclusively measure the degree of similarity
between pairs of words (e.g. ”sea” and ”ocean”) and the other
for relatedness (e.g. ”clothes” and ”closet”). More formally,
let vin [w] [and] [v] out [w] [be] [the] [input] [and] [output] [embeddings] [for] [any]
word w ∈ V where V is the vocabulary of all words and let
(wi, wj ) be pairs of words in the data sets for wi, wj ∈ V .
They found that the cosine similarity between vin [w][i] [and] [v] in [w][j]
across all pairs have the highest Spearman correlation to the
human similarity judgements data set. On the other hand, the
cosine similarity between vin [w][i] [and] [v] out [w][j] [across] [all] [pairs] [have]
the highest correlation to the relatedness scores of the second
data set. In particular, they discovered that the cosine similarity
between vin [w][i] [and][ v] out [w][j] [performed better than that] [of][ v] out [w][i] [and,]
vin [w][j] [which] [suggest] [that] [the] [likelihood] [of] [seeing] [w][j] [in] [the]
context of wi is higher than the likelihood of seeing wi in
the context of wj. This indicates and signifies that the model
is able to recognize the notion of forward relatedness and
asymmetry of the pairs.
In the following section, we describe how we can translate
the concept of dual embeddings into the recommendation systems domain, specifically in the generation of complementary
product recommendations.



Fig. 1. Example recommendations produced by different dot products of the
input and output vectors. Given kitchen faucet as a target item, the IN-OUT
variation provides recommendations that are complementary to the target (e.g.
soap dispensers, sink accessories, kitchen sinks). In contrast, both the IN-IN
and OUT-OUT variation resulted in similar recommendations (other kitchen
faucets).


IV. PROPOSED METHOD


In this section, we describe our proposed method for
complementary product recommendations, as well as our data
augmentation approach to expand product coverage to coldstart items.


A. Dual Embeddings for Complementary Product Retrieval
(DE)


As previously mentioned, one of the key details that is
often looked over in SGNS models is the fact that every
produces two vectorsvitemp andhasvp′two [are] representations. [the] [vectors] vp, vp′ [contained][corresponding to that item, where] For every [in] [the] item [input] p, [embedding] the model
matrix Win and output embedding matrix Wout, respectively.
Once the model is trained, practitioners usually discard one of
the vector representations and use the other for inference, a
popular choice is to keep the vectors in the input embedding
matrix Win. In order to retrieve candidates for a target item
p, we then find the items that correspond to the highest cosine
similarity score:


arg max cosine(vp, v) (5)
v∈Win


While this is valid for problems where the goal is to capture
similarity between two items, it is not as effective when we
require co-occurrence relationships such as complementarity.
This is because the objective of the SGNS model is to maximize the likelihood of predicting the surrounding items given
a target item, where the surrounding items are represented
using the outputs vectors and the target item is represented
using the input vector. This causes the model to learn to
represent items within each of the embedding spaces (Win



4


TABLE I
COMPARISON BETWEEN THE DUAL EMBEDDINGS MODEL (IN-OUT) AGAINST BASELINE MODELS.


Overstock Instacart
Model
Precision@20 Recall@20 Precision@50 Recall@50 Precision@20 Recall@20 Precision@50 Recall@50

Co-Purchases 0.0348 0.2745 0.0153 0.2800 0.0409 0.0514 0.0276 0.0792

Top-Sellers 0.0149 0.1029 0.0073 0.1141 0.0305 0.0698 0.0174 0.1156

IN-IN 0.0142 0.1244 0.0073 0.1514 0.0138 0.0136 0.0099 0.0237

OUT-OUT 0.0187 0.1364 0.0104 0.1694 0.0163 0.0117 0.0134 0.0199

IN-OUT 0.0391 0.3229 0.0187 0.3523 0.0437 0.0702 0.0322 0.1226



and Wout) in a way that makes them a good predictor for
their neighbors, meaning that items that share neighbors or
contexts will be represented similarly, implying substitutionary
relationships. On the other hand, the model also learns to
place items that often co-occur together near each other across
the embedding spaces, since this is what is directly being
optimized at training time. Hence, we should be expecting
mostly similar relationships being captured within each of the
embedding spaces but co-occurrence based relationships (e.g.
complementarity) across the two embedding spaces. This is
consistent with what we see in the NLP setting (Section III)
where the use of both vectors to compute the cosine similarity
resulted in a better indication of relatedness between words,
whereas the use of a single vector is best for measuring
similarity.
We can translate the concept of relatedness between words
to the concept of complementarity between products. In
particular, we can best illustrate this relationship using copurchase pairs. Given two pairs of co-purchased items, r1
and r2 where r1 = (queen mattress, bed sheet) and r2 =
(twinmattress, bedsheet). The resulting input matrix of the
model will be able to capture that queen mattress is similar
to, twinmattress since they both appear in a similar ”context”
to bedsheet. In the same way, the resulting matrices will also
be able to recognize that bedsheet is related or complementary
to queen mattress and twin mattress as they co-occur.
For the rest of the paper, we introduce the following notation
to denote the different sets of recommendations generated
using the input and output vectors of a given product p:


′
IN-OUT : arg max cosine(vp, v )
v [′] ∈Wout


IN-IN : arg max cosine(vp, v)
v∈Win


′ ′
OUT-OUT : arg max cosine(vp [,][ v] )
v [′] ∈Wout


′
OUT-IN : arg max cosine(vp [,][ v][)]
v∈Win


To capture complementary relationships, we will be relying
on inference using IN-OUT. In our experiments, we do
not consider the OUT-IN variant because we are concerned
with the forward relationship between pairs of products (e.g.
bed sheet as a complementary item to queen mattress but
not the other way around). This is consistent with the study
conducted by Asr et al. [3] on forward relatedness.



B. Data Augmentation (DA)


One of the main issues of working with purchase data is
sparsity. Purchase data on products isn’t as widely available as
other types of user generated signals like clicks or add-to-carts.
Furthermore, content data such as product title, description or
images are usually available for all products. The question we
want to investigate is, how can we use these other product
signals to augment the data on purchases? More specifically,
we want a method that can use existing co-purchased product
pairs to synthesize new product pairs that are not yet observed
in the training set. Inspired by related work in NLP on data
augmentation for classification tasks [39, 40], we introduce
a simple yet effective method for data augmentation for
complementary recommendations.
Given a similarity function that can provide a real-valued
score for any given pair of products, we use the function to
infer possible new pairwise relationships not yet observed in
the training data by creating pairs that are similar to existing
ones. For example, let (pa, pb) be a real co-purchased pair and
pa′ and pb′ be products that have high similarity to pa and pb
respectively, then we create new pairs (pa′, pb), (pa, pb′ ) and
add it to the dataset. We can similarly create a new pair by
replacing both of the original products by the similar items of
each to get (pa′, pb′). This idea relies on a simple fact that if
two items are similar then they probably complement the same
item, e.g., two very similar lamps should both complement the
same couch.
One key question is what co-purchase count do we assign
to the synthetic pairs? We think a reasonable choice would
be to rely on the original co-purchase count cab of (pa, pb)
and adjust it according to the strength of similarity to the new
product. For example, for the new pair, (pa′, pb) we assign
co-purchase count ca [′] b = ⌊cab · s(a, a [′] )⌋ where s(., .) ∈ [0, 1]
is a similarity function. The justification for the similarity
score multiplier is that highly similar products should have
comparable co-purchase counts, whereas items that are not as
similar should be penalized.
For completeness, we define the two operations to synthesize new pairs below. Note that we introduce an additional
hyperparameter γ ∈ (0, 1) that is used to tamper down some
effects the synthetic pairs will have on the entire dataset, since
if synthetic pairs are added with too high of co-purchase counts
this can dominate the entire dataset and could potentially have
a negative impact on performance.



5


1) Replace Single: We replace one of the members of the
real co-purchase pair by its most similar item, e.g., we
can create a synthetic pair (pa′, pb) with a co-purchase
count set to ca′b = ⌊γ   - cab · s(a, a [′] )⌋. We can similarly
create a pair (pa, pb′).
2) Replace Both: We replace both of the products in the pair
with their respective similar items to get (pa′, pb′) with
a co-purchase count of ca′b′ = ⌊γ · cab · [s][(][a,a][′][)+] 2 [s][(][b,b][′][)] ⌋.

Although the method we described creates synthetic pairs
using only the most similar one item to the existing one, in
practice this can be replaced by k most similar items which
can allow for an upwards of k [2] + 2k synthetic pairs to be
created using only a single real pair. In practice, we would also
recommend introducing a parameter that defines the minimum
threshold θ on the similarity scores, as this can allow for better
control on the quality of the added synthetic pairs.


C. Inference Augmentation (IA)


We can apply a similar idea at inference time as well.
That is, for a given target product that is not represented in
our training set, meaning that we are not able to generate
recommendations for it, we can first look up the most similar
item that does appear in the training set and use it to infer
complementary products on the original target item. Let pa′
be a target product that does not exist in our training set,
we first retrieve a product pa from our training set such that
pa = arg maxp∈P s(a [′], p) and then we proceed to recommend
items using (IV-A). We refer to this method as inference
augmentation or IA for short.


V. EXPERIMENTS AND RESULTS


We compare the performance of our model against the
following baselines:


 - Top-Sellers Recommend most popular (the highest selling) items for every target item. This heuristic can be
effective for items that are complementary to many other
items, e.g., eggs and milk in grocery shopping data.

 - Co-Purchases For a given target item, recommend most
frequently co-purchased items (in descending order). This
model is typically used as a baseline model, as it generally produces high relevancy.

 - IN-IN & OUT-OUT Recommend nearest neighbors of
the target item based on either the input or output vectors.


A. Datasets


We evaluate our models on real world data from two major
online retail companies:


 - Overstock.com: Proprietary data from major online
home-goods retail company. This dataset consists of two
years worth of transactions made through the Overstock.com website. All orders in the most recent month
are used as held out test set and the rest are used for
training. It contains over 18 million users across 24
million sessions with around 1.6 million distinct product
IDs. The product IDs spans beyond 3 thousands different
sub-categories and 168 departments.




 - Instacart.com [17]: Publicly available data from a major
grocery delivery company. This data contains over 3
million orders across 21 departments, 134 different aisles
from more than 200 thousands users. The dates of the
transactions were not included, however, the add-to-cart
order were part of the additional information. We used
the training set that were made available and pre-process
the data accordingly.


B. Implementation Details


To train the SGNS model we use fastText++ [33] which
is an extended version of the popular library fastText [6]
developed by Facebook AI Research lab. We disable the
subword embedding option, as we do not have text as input.
All the hyperparameters of the model are optimized using Ray
Tune [22] on a cluster of e2-highcpu-32 machines on Google
Cloud Platform, more details on hyperparameter tuning are
provided in a later section. At inference time, for fast approximate nearest neighbor searches, we use Hierarchical Navigable
Small World (HNSW) [23] graphs as implemented in Faiss

[18].


C. Data Pre-processing


We remove overly active users (higher number of unique
purchases than 99.9% population), as these users are likely
associated with drop-shipping. We similarly remove purchase
sessions that have a high number of unique purchases (again
above 99.9%) since a high number of purchases in a session
potentially provides a weaker signal on the relationship between pairs of items in that session. We create a pairwise
product dataset from the purchase sessions by taking all
unique pairs in a given purchase session. We remove any
product pair that does not have at least 3 co-purchases. We
measure Pointwise Mutual Information (PMI) [11], as defined
below, to further identify pairs that provide weaker signal on
complementarity by removing all pairs with negative PMI.




      PMI(pi, pj) = log (ni/Tnij )(/Tnj/T )





(6)



where ni is the number of times the product pi was purchased,
nij is the number of times the pair (pi, pj) was co-purchased,
and T is the total number of sessions.
We also discard product pairs that have identical taxonomies, since these usually coincide with similar products
rather than complementary. There are some exceptions to this
rule (e.g. throw pillows) which we account for by creating a
taxonomy exception list curated from highly purchased pairs
from the same taxonomy. Similar to the product pairwise data,
we also create a taxonomy dataset aggregated in pairwise
manner. We compute PMI between the pairs of taxonomies,
which allows us to use it for another round of filtering at
the product level, i.e. if a product pairs’ taxonomy PMI is
lower than a minimum threshold, we discard that pair. The
aforementioned processing technique is especially important
for filtering synthetic pairs at the data augmentation stage
because those pairs do not have actual purchases associated



6


TABLE II
THE EFFECTS OF DATA AND INFERENCE AUGMENTATION ON DIFFERENT SUBSET OF THE VALIDATION SET


In-Coverage Out-of-Coverage Combined
Model
Precision@20 Recall@20 Precision@20 Recall@20 Precision@20 Recall@20

Random 0.0093 0.0383 0.0006 0.0052 0.0059 0.0262

Top-Sellers 0.0216 0.1419 0.0017 0.0253 0.0149 0.1029

IN-OUT 0.0584 0.4847 0.0000 0.0000 0.0388 0.3224

IN-OUT+DA 0.0589 0.4912 0.0012 0.0163 0.0396 0.3322

IN-OUT+IA N/A N/A 0.0018 0.0251 0.0368 0.3232

IN-OUT+DA+IA N/A N/A 0.0038 0.0269 0.0398 0.3345



with it, but we can still rely on taxonomy level scores for
discarding noisy pairs.


D. Dual Embeddings Evaluation


We evaluate our models on a held out test set processed
in the same way as our training sets. Pairs of products were
created from the purchase data, then for each query product
q ∈ Q, where Q is the sets of all query products, we ranked the
co-purchase product IDs based on the number of times they
co-occur. Let Lq be the list of ranked co-purchase products for
the item q deduced from the test set, and Rq [K] be the top K
predicted list of complementary product recommendations for
the item q produced by the model. As our goal for the model
is to retrieve candidate sets, we focus on two main metrics
that best align with this goal: Precision@K and Recall@K.
We define these metrics as follows:


q [|] q [|]
Precisionq@K = [|][L][q][ ∩] K [R][K], Recallq@K = [|][L][q] | [ ∩] Lq [R] | [K]


We report the mean of both metrics ∀q ∈ Q in our test set
and choose K ∈{20, 50}. We see from Table I that the INOUT dual embeddings model performed best compared to the
others on both datasets, followed closely by the co-purchases
baseline. This table proves that the cross embeddings’ cosine
similarity measure is better able to capture the complementary
relationship between products, compared to the conventional
technique of using only one embedding IN-IN, OUT-OUT.


E. Hyperparameter Tuning


Quite often, Word2Vec is used off-the-shelf without optimizing the hyperparameters on the relevant task. While this
may be satisfactory when the model is applied to natural
language datasets, it is almost always suboptimal when applied
to recommender systems datasets. Following previous work
on studying the importance of Word2Vec hyperparameters in
the recommender systems setting [7, 8], we optimize all the
relevant parameters of our model, namely the number of negative samples ns ∈ (5, 30), the negative sampling distribution
exponent α ∈ (−1, 1), the random sub-sampling parameter
t ∈ (10 [−][4], 10 [−][2] ), the initial learning rate λ ∈ (0.05, 0.15) and
the embedding dimension d ∈ (20, 100). We set the number of
epochs to a large fixed number because we use early stopping
during training. We note that the parameter for the context
window size is irrelevant for our setting, since our dataset is in



the form of pairs rather than sequences. We optimize the model
on a co-purchase prediction task, using a subset (10%) of the
unique co-purchase pairs in the training set. We make sure to
remove all of the co-purchase pairs present in the development
set from the training set, thus creating a completely disjoint
set. The model is essentially tasked with predicting unobserved
co-purchase relationships between products. The development
set co-purchase pairs are aggregated to have a single target
product as the input and the ranked list of frequently copurchased products as the ground truth. At evaluation time, we
query the model with the target item and measure the recall
and precision at the top k outputs (nearest neighbors).
Our tuned IN-OUT model on the Overstock dataset has
the following hyperparameters: ns = 20, d = 50, α =
−0.1, λ = 0.045, t = 0.0001 and for the Instacart dataset:
ns = 30, d = 100, α = 0.0, λ = 0.015, t = 0.001. Table III
shows the relative increase of the evaluation metrics between
the optimal and default values. The gains seen in both of the
datasets further emphasizes the importance of properly tuning
the Word2Vec model.


TABLE III
RELATIVE INCREASE IN OPTIMIZED HYPERPARAMETERS COMPARED TO
DEFAULT VALUES


Overstock Instacart
Values
Precision@20 Recall@20 Precision@20 Recall@20

Default 0.0236 0.1271 0.0101 0.0173

Optimized 0.0391 0.3229 0.0437 0.0702

Rel. Increase 65.6% 154% 332.6% 300%


F. Data Augmentation Results


In order to better understand the effects of the data and
inference augmentation techniques, we split our validation
set into two parts. One part only contains target products
that appear in the original (unaugmented) training set, this is
referred to as the in-coverage, the second part is composed of
target products that do not appear in the training set, we refer
to this portion as the out-of-coverage set. While the primary
goal of the data augmentation is to provide improvement on
the out-of-coverage item prediction, we are also interested in
seeing if there are any improvements on the in-coverage set. As
baselines, we consider a popularity based recommender (TopSellers) and a random recommender (Random) that simply



7


randomly samples products from the training set for each
target item. These heuristics are good choices as baselines
since they do not suffer from coverage issues, as they always
produce recommendations on any given target product. The
models that have +DA or +IA imply that those models had
either data augmentation, inference augmentation, or both. We
omit evaluation numbers for IA on in-coverage, since IA is
only applicable to out-of-coverage predictions. In order to get
similarity measurements on product pairs, we train a separate
SGNS model on user click sequences. Each sequence consists
of clicks accumulated during a 30-minute session. We optimize
the hyperparameters of the model on frequently co-clicked
product prediction task, where the co-clicks are collected only
from search and navigation pages. The reason we chose this
evaluation set is to curb some effects of the feedback loop
bias introduced by other product recommender systems that
are currently in production.
The results in Tables II and IV suggest that the data augmentation has a positive impact on both the in-coverage and
the out-of-coverage subsets in terms of predictive relevancy
as well as total coverage. Although, the improvement on the
out-of-coverage is modest and what’s even more surprising, a
simple popularity based recommender is seemingly doing as
well as our model.
We hypothesize that part of the issue is because the added
synthetic pairs may be capturing novel relationships that are
simply not covered by the existing historical data. To gain
more insight into the effects of data augmentation, we create
an altered version of the validation set where the prediction
task is at the taxonomy level rather than at the product level.
We think that if the recommended products from the model
have relevant taxonomies to the target product’s taxonomy,
then the recommended products themselves will be relevant as
well. Different from the product level evaluation, we measure
the metrics at a smaller cutoff (@1 and @3), since any given
taxonomy will at most have a handful of relevant taxonomies,
as opposed to products that have a much larger relevant
candidate set.


TABLE IV
TAXONOMY AND PRODUCT COVERAGE


Model Taxonomy Coverage Product Recommendation
Coverage


IN-OUT 15.40% 66.5%
IN-OUT+DA 17.18% 77.12%
IN-OUT+IA 16.20% 75.2%
IN-OUT+DA+IA 17.48% 81.08%


The results of the taxonomy prediction task shown in Table
V suggest that the data augmentation is making a measurable
impact on the out-of-coverage set. We see a clear difference
between the popularity baseline and our model at the taxonomy level. This points to our models’ ability to provide
actually relevant recommendations. This is further confirmed
by visual validation of the recommendations as well, we refer



TABLE V
OUT-OF-COVERAGE TAXONOMY PREDICTIONS


Model Precision@1 Recall@1 Precision@3 Recall@3


Random 0.0292 0.0100 0.0252 0.0301
Top-Sellers 0.0198 0.0161 0.0221 0.0382
IN-OUT 0.0000 0.0000 0.0000 0.0000
IN-OUT+DA 0.0598 0.0417 0.0326 0.0676
IN-OUT+IA 0.0512 0.0392 0.0318 0.0661
IN-OUT+DA+IA 0.0802 0.0581 0.0444 0.0919


Fig. 2. Example candidate sets produced by our model on out-of-coverage
target products.


the reader to Figure 2 for example recommendations provided
by the model.


VI. CONCLUSION


In this paper, we describe an effective method for retrieving complementary products using product embeddings
learned with SGNS. Our approach relies on the fact that
SGNS learns two separate embeddings for each item. At
inference time, we make use of both embeddings to retrieve
relevant complementary items. We show that using both of
the embeddings rather than the standard approach of only
using one significantly improves the results on multiple real
world datasets for complementary product recommendations.
The advantage of our model is the ease of which it can be
implemented and scaled using existing and widely available
libraries and software packages. Given enough data, the model
can be implemented at a large scale with relatively low latency,
especially beneficial for major online e-commerce companies.
To handle data sparsity issues often exhibited in settings
where purchases are used for modeling, we propose a straightforward data augmentation method that has parallels to prior
studies in data augmentation for NLP tasks. We rely on
similarity measurements learned from other readily available
sources of data, such as clicks, to generate novel product pairs.
This allows the model to extend its retrieval capability to products that have no or very little purchase data. Our experiments



8


demonstrate that we were able to not only effectively expand
product coverage, but also improve relevancy. We hope that
our approach can serve as a strong baseline for future work
in the space of complementary product recommendations.
Future studies can explore further development on expanding coverage to even more products without sacrificing, or
better yet, improving the performance of the existing covered
products. We note that in general, the ability to perform
inference on unseen products is an important step in recommendation systems, as newly exposed products will eventually
garner more data which will, in time, improve the relevancy
of recommended products. In addition, we see a connection
between the number of augmented products included in the
training set and the concept of exploration vs. exploitation in
reinforcement learning. This connection can be investigated
further. In particular, an interesting phenomenon which often
happens during an exploration phase is that more co-purchases
and co-clicks data are obtained for explored items, which can
later improve our recommendations. We call this process selfhealing which can be further quantified and measured in the
future.


REFERENCES


[1] R. Agrawal, T. Imieli´nski, and A. Swami. Mining
association rules between sets of items in large databases.
In Proceedings of the 1993 ACM SIGMOD international
conference on Management of data, pages 207–216,
1993.

[2] M. Angelovska, S. Sheikholeslami, B. Dunn, and A. H.
Payberah. Siamese neural networks for detecting complementary products. In Proceedings of the 16th Conference
of the European Chapter of the Association for Computational Linguistics: Student Research Workshop, pages
65–70, 2021.

[3] F. T. Asr, R. Zinkov, and M. Jones. Querying word embeddings for similarity and relatedness. In Proceedings
of the 2018 Conference of the North American Chapter
of the Association for Computational Linguistics: Human
Language Technologies, Volume 1 (Long Papers), pages
675–684, 2018.

[4] J. Bai, C. Zhou, J. Song, X. Qu, W. An, Z. Li, and J. Gao.
Personalized bundle list recommendation. In The World
Wide Web Conference, pages 60–71, 2019.

[5] O. Barkan and N. Koenigstein. Item2vec: neural item
embedding for collaborative filtering. In 2016 IEEE 26th
International Workshop on Machine Learning for Signal
Processing (MLSP), pages 1–6. IEEE, 2016.

[6] P. Bojanowski, E. Grave, A. Joulin, and T. Mikolov.
Enriching word vectors with subword information. arXiv
preprint arXiv:1607.04606, 2016.

[7] H. Caselles-Dupr´e, F. Lesaint, and J. Royo-Letelier.
Word2vec applied to recommendation: Hyperparameters
matter. In Proceedings of the 12th ACM Conference on
Recommender Systems, pages 352–356, 2018.

[8] B. P. Chamberlain, E. Rossi, D. Shiebler, S. Sedhain,
and M. M. Bronstein. Tuning Word2vec for Large Scale



Recommendation Systems, page 732–737. Association
for Computing Machinery, New York, NY, USA, 2020.

[9] F. Chen, X. Liu, D. Proserpio, I. Troncoso, and F. Xiong.
Studying product competition using representation learning. In Proceedings of the 43rd International ACM SIGIR
Conference on Research and Development in Information
Retrieval, pages 1261–1268, 2020.

[10] E. Choi, M. T. Bahadori, E. Searles, C. Coffey,
M. Thompson, J. Bost, J. Tejedor-Sojo, and J. Sun. Multilayer representation learning for medical concepts. In
proceedings of the 22nd ACM SIGKDD international
conference on knowledge discovery and data mining,
pages 1495–1504, 2016.

[11] K. W. Church and P. Hanks. Word association norms,
mutual information, and lexicography. Computational
Linguistics, 16(1):22–29, 1990.

[12] J. Du, P. Jia, Y. Dai, C. Tao, Z. Zhao, and D. Zhi.
Gene2vec: distributed representation of genes based on
co-expression. BMC genomics, 20(1):7–15, 2019.

[13] M. D. Ekstrand, J. T. Riedl, and J. A. Konstan. Collaborative filtering recommender systems. Now Publishers
Inc, 2011.

[14] C. Fu, C. Xiang, C. Wang, and D. Cai. Fast approximate
nearest neighbor search with the navigating spreadingout graphs. PVLDB, 12(5):461   - 474, 2019.

[15] M. Grbovic, V. Radosavljevic, N. Djuric, N. Bhamidipati,
J. Savla, V. Bhagwan, and D. Sharp. E-commerce in your
inbox: Product recommendations at scale. In Proceedings
of the 21th ACM SIGKDD international conference on
knowledge discovery and data mining, pages 1809–1818,
2015.

[16] A. Grover and J. Leskovec. node2vec: Scalable feature
learning for networks. In Proceedings of the 22nd
ACM SIGKDD international conference on Knowledge
discovery and data mining, pages 855–864, 2016.

[17] Instacart.com. The instacart online grocery
shopping dataset, 2017. Accessed on June 2022.
https://www.instacart.com/datasets/grocery-shopping2017.

[18] J. Johnson, M. Douze, and H. J´egou. Billion-scale
similarity search with GPUs. IEEE Transactions on Big
Data, 7(3):535–547, 2019.

[19] Y. Koren. Collaborative filtering with temporal dynamics.
In Proceedings of the 15th ACM SIGKDD international
conference on Knowledge discovery and data mining,
pages 447–456, 2009.

[20] Y. Koren, R. Bell, and C. Volinsky. Matrix factorization techniques for recommender systems. Computer,
42(8):30–37, 2009.

[21] O. Levy, Y. Goldberg, and I. Dagan. Improving distributional similarity with lessons learned from word embeddings. Transactions of the association for computational
linguistics, 3:211–225, 2015.

[22] R. Liaw, E. Liang, R. Nishihara, P. Moritz, J. E. Gonzalez, and I. Stoica. Tune: A research platform for
distributed model selection and training. arXiv preprint



9


arXiv:1807.05118, 2018.

[23] Y. A. Malkov and D. A. Yashunin. Efficient and robust
approximate nearest neighbor search using hierarchical
navigable small world graphs. 42(4):824–836, apr 2020.

[24] J. McAuley, R. Pandey, and J. Leskovec. Inferring
networks of substitutable and complementary products.
In Proceedings of the 21th ACM SIGKDD international
conference on knowledge discovery and data mining,
pages 785–794, 2015.

[25] J. McAuley, C. Targett, Q. Shi, and A. Van Den Hengel.
Image-based recommendations on styles and substitutes.
In Proceedings of the 38th international ACM SIGIR
conference on research and development in information
retrieval, pages 43–52, 2015.

[26] T. Mikolov, K. Chen, G. Corrado, and J. Dean. Efficient
estimation of word representations in vector space. arXiv
preprint arXiv:1301.3781, 2013.

[27] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and
J. Dean. Distributed representations of words and phrases
and their compositionality. Advances in neural information processing systems, 26, 2013.

[28] B. Mitra, E. Nalisnick, N. Craswell, and R. Caruana.
A dual embedding space model for document ranking.
arXiv preprint arXiv:1602.01137, 2016.

[29] A. Mnih and R. R. Salakhutdinov. Probabilistic matrix
factorization. Advances in neural information processing
systems, 20, 2007.

[30] J. Pennington, R. Socher, and C. D. Manning. Glove:
Global vectors for word representation. In Proceedings
of the 2014 conference on empirical methods in natural
language processing (EMNLP), pages 1532–1543, 2014.

[31] J. B. Schafer, D. Frankowski, J. Herlocker, and S. Sen.
Collaborative filtering recommender systems. In The
adaptive web, pages 291–324. Springer, 2007.

[32] H. V. Simhadri, G. Williams, M. Aum¨uller, M. Douze,
A. Babenko, D. Baranchuk, Q. Chen, L. Hosseini,
R. Krishnaswamy, G. Srinivasa, S. J. Subramanya, and
J. Wang. Results of the neurips’21 challenge on billionscale approximate nearest neighbor search, 2022.

[33] N. Subedi. fasttext++: Batteries included, August 2018.

[Online; posted 25-August-2018].

[34] I. Trofimov. Inferring complementary products from
baskets and browsing sessions. arXiv preprint
arXiv:1809.09621, 2018.

[35] F. Vasile, E. Smirnova, and A. Conneau. Meta-prod2vec:
Product embeddings using side-information for recommendation. In Proceedings of the 10th ACM Conference
on Recommender Systems, pages 225–232, 2016.

[36] M. Wan, D. Wang, J. Liu, P. Bennett, and J. McAuley.
Representing and recommending shopping baskets with
complementarity, compatibility and loyalty. In Proceedings of the 27th ACM International Conference on
Information and Knowledge Management, pages 1133–
1142, 2018.

[37] J. Wang, P. Huang, H. Zhao, Z. Zhang, B. Zhao, and
D. L. Lee. Billion-scale commodity embedding for e


commerce recommendation in alibaba. In Proceedings
of the 24th ACM SIGKDD International Conference on
Knowledge Discovery & Data Mining, pages 839–848,
2018.

[38] M. Wang, X. Xu, Q. Yue, and Y. Wang. A comprehensive survey and experimental comparison of graph-based
approximate nearest neighbor search, 2021.

[39] W. Y. Wang and D. Yang. That’s so annoying!!!: A lexical and frame-semantic embedding based data augmentation approach to automatic categorization of annoying
behaviors using #petpeeve tweets. In Proceedings of the
2015 Conference on Empirical Methods in Natural Language Processing, pages 2557–2563, Lisbon, Portugal,
Sept. 2015. Association for Computational Linguistics.

[40] J. Wei and K. Zou. EDA: Easy data augmentation
techniques for boosting performance on text classification
tasks. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the
9th International Joint Conference on Natural Language
Processing (EMNLP-IJCNLP), pages 6382–6388, Hong
Kong, China, Nov. 2019. Association for Computational
Linguistics.

[41] H.-J. Xue, X. Dai, J. Zhang, S. Huang, and J. Chen. Deep
matrix factorization models for recommender systems.
In IJCAI, volume 17, pages 3203–3209. Melbourne,
Australia, 2017.

[42] T. Zhu, P. Harrington, J. Li, and L. Tang. Bundle
recommendation in ecommerce. In Proceedings of the
37th international ACM SIGIR conference on Research
& development in information retrieval, pages 657–666,
2014.



10


