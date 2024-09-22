# document_similarity

Given a corpus of several thousand 20k word articles, how do you find the 2% of articles that are "on topic" when "on topic" is not necessarily among the primary topics of the article?

This code was used in the research that culminated in the publication of ["The New Rules of Marketing Across Channels" (https://hbr.org/2024/06/the-new-rules-of-marketing-across-channels)].

Latent Dirichlet Allocation and Stochastic Block Modeling did a good job of extracting the topics that frequently occurred.  However, the topic of interest was not a topic that frequently occurs in marketing journals and attempts to “drill-down” into the results from LDA and SBM quickly became counter-intuitive and difficult to interpret.

We eventually settled on choosing “prototype” articles representing the topic and measuring the "distance" of the unknown articles from the prototypes.  In order to do this, we needed a metric of similarity.

I extended traditional bag-of-words frequency counts by encoding part-of-speech values into the frequency counts.

The reason for doing this was to address one of the inherent problems with bag-of-words processing:

* Document 1:  Bob likes big data.  Bob likes Judy.
* Document 2:  Big data likes Bob.  Judy likes Bob.

Only using frequency counts, these two documents are evaulated as being exactly the same.

I extended this by having the frequency counts be a two-dimensional vector that encoded the "nouniness" and "verbiness" of the tokens using a complex representation with nouniness mapped to the real component and verbiness mapped to the imaginary component.

Using this encoding the token values break down as:

Document 1
| Usage | NPROP, nsubj | VERB ROOT  | ADJ, amod   | NOUN, dobj | PROP, nsubj | VERB, ROOT | PROP, nsubj |
| ----- | ------------ | ---------- | ----------- | ---------- | ----------- | ---------- | ----------- |
| Token | bob          | like       | big         | data       | bob         | like       | judi        |
| Value | 1.0 + 0.0i   | 0.0 + 1.0i | 0.25 + 0.0i | 0.5 + 0.0i | 1.0 + 0.0i  | 0.0 + 1.0i | 0.5 + 0.0i  |

Document 2
| Usage | ADJ, amod   | NOUN, nsubj | VERB, ROOT | PROPN, dobj | PROP, nsubj | VERB, ROOT | PROP, nsubj |
| ----- | ----------- | ----------- | ---------- | ----------- | ----------- | ---------- | ----------- |
| Token | big         | data        | like       | bob         | judi        | like       | bob         |
| Value | 0.25 + 0.0i | 1.0 + 1.0i  | 0.0 + 1.0i | 0.5 + 0.0i  | 1.0 + 0.0i  | 0.0 + 1.0i | 0.5 + 0.0i  |

Which gives us the bag-of-words frequency counts of:

|      | Document 1  | Document 2  |
| ---- | ----------- | ----------- |
| big  | 0.25 + 0.0i | 0.25 + 0.0i |
| bob  | 2.0 + 0.0i  | 1.5 + 0.0i  |
| data | 0.5 + 0.0i  | 1.0 + 0.0i  |
| judi | 0.5 + 0.0i  | 1.0 + 0.0i  |
| like | 0.0 + 2.0i  | 0.0 + 2.0i  |

I then chose the magnitude of one minus the log2 variant of Shannon-Jenson Divergence to calculate the probability of interest an unknown document given a known prototype document.

