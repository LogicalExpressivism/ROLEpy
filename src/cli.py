import click
import json
import os
os.environ["CORENLP_HOME"] = "./corenlp"
import stanza
from stanza.server import CoreNLPClient
from pprint import pprint

@click.group()
def cli():
    pass

def defaultParser():
    stanza.download('en')
    return stanza.Pipeline('en')

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
            with CoreNLPClient(annotators=['tokenize','ssplit','pos','lemma','ner', 'parse', 'depparse','dcoref'], timeout=30000, memory='16G') as client:
                ann = client.annotate(infile.read(), output_format='json')
                outfile.write(json.dumps(ann))
        else:
            en_nlp = defaultParser()
            parsed = en_nlp(infile.read())
            outfile.write(json.dumps(parsed.to_dict()))


if __name__ == '__main__':
    cli()