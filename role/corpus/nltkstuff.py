from role.corpus import *
from nltk.corpus import brown
from nltk.sem.glue import *
nltk.sem.logic._counter._value = 0
from nltk.parse.malt import MaltParser

# file = read_stanza_document_file("role/corpus/kant/fpmm_1_stanza.ann")
# tagged = [[(w.text, w.xpos) for w in s.words] for s in file.sentences]

brown_train = brown.tagged_sents(categories="news")
unigram_tagger = UnigramTagger(brown_train)
# bigram_tagger = BigramTagger(brown_train, backoff=unigram_tagger)
# trigram_tagger = TrigramTagger(brown_train, backoff=bigram_tagger)
main_tagger = RegexpTagger(
    [(r"(A|a|An|an|The|the)$", "ex_quant"), (r"(Every|every|All|all|Any|any)$", "univ_quant")],
    backoff=unigram_tagger,
)

depparser = MaltParser('./maltparser-1.9.2', tagger=main_tagger.tag)
glue = DrtGlue(depparser=depparser)
print(main_tagger.tag("The grand jury produced no evidence that any irregularities took place".split()))
readings = glue.parse_to_meaning("The grand jury produced no evidence that any irregularities took place".split())