import click
import json
import os
os.environ["CORENLP_HOME"] = "./corenlp"
import stanza
from stanza.server import CoreNLPClient
from pprint import pprint

# src/parse.py
from parse import Formula, Sentence, printTree

@click.group()
def cli():
    pass

def defaultParser():
    stanza.download('en')
    return stanza.Pipeline('en')

def coreParser():
    return CoreNLPClient(annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse', 'coref'], timeout=30000, memory='16G')

@cli.command()
@click.option('--core', is_flag=True)
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
def parsefile(core, input, output):
    try:
        infile = open(input, "r")
        outfile = open(output, "w")
    except OSError as err:
        click.echo('Error: {}'.format(err))
    else:
        if core:
            with coreParser() as client:
                ann = client.annotate(infile.read(), output_format='json')
                outfile.write(json.dumps(ann))
        else:
            en_nlp = defaultParser()
            parsed = en_nlp(infile.read())
            outfile.write(json.dumps(parsed.to_dict()))

@cli.command()
@click.argument('input', type=click.File('r'))
def formulas(input):
    with coreParser() as client:
        doc = client.annotate(input.read())
        sentences = [Sentence(s) for s in doc.sentence]
        formulas = [s.parseFormulas() for s in sentences]
        for i, f in enumerate(formulas):
            print('[{}]----------'.format(i + 1))
            # printTree(sentences[i].sentence.binarizedParseTree)
            f.prettyPrint(1)


if __name__ == '__main__':
    cli()