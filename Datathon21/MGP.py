from numpy.random import multinomial
from numpy import log, exp
from numpy import argmax
from wordcloud import WordCloud
import json
import matplotlib.pyplot as plt

'''
Generates 4 clusters out of a list of lists, where each list is a sentence,
each word of the sentence is an element of the list. Example:
    -> ['THE', 'FOOD', 'WAS', 'GOOD']

Based off of:
    http://dbgroup.cs.tsinghua.edu.cn/wangjy/papers/KDD14-GSDMM.pdf
'''


class MovieGroupProcess:
    '''Class to generate the clusters. The higher the amount of iterations
    the better as it converges to the ideal clusters.'''

    def __init__(self, K=8, alpha=0.1, beta=0.1, n_iters=30):
        self.K = K
        self.alpha = alpha
        self.beta = beta
        self.n_iters = n_iters

        # slots for computed variables
        self.number_docs = None
        self.vocab_size = None
        self.cluster_doc_count = [0 for _ in range(K)]
        self.cluster_word_count = [0 for _ in range(K)]
        self.cluster_word_distribution = [{} for i in range(K)]

    @staticmethod
    def from_data(K, alpha, beta, D, vocab_size, cluster_doc_count, cluster_word_count, cluster_word_distribution):
        mgp = MovieGroupProcess(K, alpha, beta, n_iters=30)
        mgp.number_docs = D
        mgp.vocab_size = vocab_size
        mgp.cluster_doc_count = cluster_doc_count
        mgp.cluster_word_count = cluster_word_count
        mgp.cluster_word_distribution = cluster_word_distribution
        return mgp

    @staticmethod
    def _sample(p):
        return [i for i, entry in enumerate(multinomial(1, p)) if entry != 0][0]

    def fit(self, docs, vocab_size):
        '''Function that generates the clusters out of the list of lists and size.'''
        alpha, beta, K, n_iters, V = self.alpha, self.beta, self.K, self.n_iters, vocab_size

        D = len(docs)
        self.number_docs = D
        self.vocab_size = vocab_size

        # Unpacking a couple parameters
        m_z, n_z, n_z_w = self.cluster_doc_count, self.cluster_word_count, self.cluster_word_distribution
        cluster_count = K
        d_z = [None for i in range(len(docs))]

        # Initialising the clusters
        for i, doc in enumerate(docs):

            # choose a random  initial cluster for the doc
            z = self._sample([1.0 / K for _ in range(K)])
            d_z[i] = z
            m_z[z] += 1
            n_z[z] += len(doc)

            for word in doc:
                if word not in n_z_w[z]:
                    n_z_w[z][word] = 0
                n_z_w[z][word] += 1

        for _iter in range(n_iters):
            total_transfers = 0
            for i, doc in enumerate(docs):
                # remove the doc from it's current cluster
                z_old = d_z[i]

                m_z[z_old] -= 1
                n_z[z_old] -= len(doc)

                for word in doc:
                    n_z_w[z_old][word] -= 1

                    # compact dictionary to save space
                    if n_z_w[z_old][word] == 0:
                        del n_z_w[z_old][word]

                # Drawing sample from distribution to find new cluster
                p = self.score(doc)
                z_new = self._sample(p)

                # Transfering doc to the new cluster
                if z_new != z_old:
                    total_transfers += 1

                d_z[i] = z_new
                m_z[z_new] += 1
                n_z[z_new] += len(doc)

                for word in doc:
                    if word not in n_z_w[z_new]:
                        n_z_w[z_new][word] = 0
                    n_z_w[z_new][word] += 1

            cluster_count_new = sum([1 for v in m_z if v > 0])
            print("In stage %d: transferred %d clusters with %d clusters populated" % (_iter, total_transfers, cluster_count_new))

            if total_transfers == 0 and cluster_count_new == cluster_count and _iter>25:
                # print("Converged.  Breaking out.")
                break
            cluster_count = cluster_count_new
        self.cluster_word_distribution = n_z_w
        return d_z

    def score(self, doc):
        alpha, beta, K, V, D = self.alpha, self.beta, self.K, self.vocab_size, self.number_docs
        m_z, n_z, n_z_w = self.cluster_doc_count, self.cluster_word_count, self.cluster_word_distribution

        p = [0 for _ in range(K)]

        lD1 = log(D - 1 + K * alpha)
        doc_size = len(doc)
        for label in range(K):
            lN1 = log(m_z[label] + alpha)
            lN2 = 0
            lD2 = 0
            for word in doc:
                lN2 += log(n_z_w[label].get(word, 0) + beta)
            for j in range(1, doc_size +1):
                lD2 += log(n_z[label] + V * beta + j - 1)
            p[label] = exp(lN1 - lD1 + lN2 - lD2)

        # Normalizng the probability vector
        pnorm = sum(p)
        pnorm = pnorm if pnorm>0 else 1
        return [pp/pnorm for pp in p]

    def choose_best_label(self, doc):
        p = self.score(doc)
        return argmax(p),max(p)

def test(docs):
    '''Generates and shows 4 clusters out of a list of lists.'''

    # Setting the initial parameters
    mgp = MovieGroupProcess(K=4, alpha=0.1, beta=0.1, n_iters=200)

    vocab = set(x for doc in docs for x in doc)
    n_terms = len(vocab)
    n_docs = len(docs)

    # Generating the clusters
    y = mgp.fit(docs, n_terms)

    # Labelling the clusters
    text = ['' for i in range(max(y) + 1)]
    for i in range(len(y)):
        text[y[i]] += " ".join(docs[i])
        text[y[i]] += " "

    clusters = set(y)
    clusters = list(clusters)


    # Plotting the 'world clouds' to visualize the clusters
    axes=[]
    fig = plt.figure()
    for a in range(len(clusters)):
        axes.append( fig.add_subplot(len(clusters)/2 + int(len(clusters) % 2 != 0), 2, a+1) )
        wordcloud = WordCloud(width = 800, height = 800,
                              background_color = 'white',
                              min_font_size = 10).generate(text[clusters[a]])
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

    fig.tight_layout()
    plt.show()
