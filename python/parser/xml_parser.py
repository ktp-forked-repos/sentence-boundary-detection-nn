import xml.etree.ElementTree, sys, os.path, re
from argparse_util import *
from text import *
from abstract_parser import AbstractParser
from nlp_pipeline import NlpPipeline


class XMLParser(AbstractParser):
    def __init__(self, filename):
        super(C, self).method(filename)
        self.nlp_pipeline = NlpPipeline()

    def parse(self):
        mteval = xml.etree.ElementTree.parse(self.filename).getroot()
        srcset = mteval.find("srcset")
        for doc in srcset.findall('doc'):
            talk = Text()

            for sentence in doc.findall("seg"):
                sentence_text = unicode(sentence.text)

                sentence = Sentence()
                sentence.set_sentence_text(sentence_text)
                sentence.set_tokens(self.nlp_pipeline.parse_text(sentence_text))
                talk.add_sentence(sentence)

            yield talk

    def progress(self):
        return self._no_progress_function()

################
# Example call #
################

def main(filename):
    parser = XMLParser(filename)
    talks = parser.parse()
    for talk in talks:
        print(talk)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test the xml file parsing')
    parser.add_argument('filename', help='XML file containing talks', type=lambda arg: is_valid_file(parser, arg))
    args = parser.parse_args()

    main(args.filename)
