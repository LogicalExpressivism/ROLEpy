if [ ! -d "stanford-corenlp-4.1.0" ]
then
    echo "Installin Stanford CoreNLP"
    curl -O -L http://nlp.stanford.edu/software/stanford-corenlp-latest.zip
    unzip stanford-corenlp-latest.zip
    rm stanford-corenlp-latest.zip
fi

if [ ! -d "UDepLambda" ]
then
    if ! command -v ant 2 > &2
    then
        echo "Error: building UDepLambda requires ant."
        exit
    fi
    git clone https://github.com/sivareddyg/UDepLambda.git
    pushd UDepLambda
    git submodule update --init --recursive lib
    git submodule update --init --recursive lib_data/ud-models-v1.3
    git submodule update --init --recursive lib_data/ud-models-v1.2
    ant build
    popd
fi