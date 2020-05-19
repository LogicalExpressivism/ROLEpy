sent = """Socrates is human implies Socrates is mortal. Socrates is human. Socrates is mortal."""

uconnectives = ["not"]

bconnectives = ["and", "or", "implies"]

def parse(sentence):
    atoms = []
    props = [sent.strip() for sent in sentence.split(".") if sent]
    for p in props:
        trybconn = partitionBConn(p)
        if trybconn:
            atoms.append(trybconn)
            continue
        atoms.append(p)
        
    print(atoms)

def partitionBConn(sent):
    for conn in bconnectives:
        if ' ' + conn + ' ' in sent:
            return sent.partition(' ' + conn + ' ')
    return False

parse(sent)