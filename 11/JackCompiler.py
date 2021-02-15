import sys
import os

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

def process_file(path):
    jack_tokenizer = JackTokenizer(path)
    token_list = jack_tokenizer.tokenize()
    compilation_engine = CompilationEngine(path,token_list)
    compilation_engine.Compile()


def process_dir(path):
    files_in_dir = os.listdir(path)
    jack_files = [file for file in files_in_dir if file.endswith(".jack")]
    
    for file in jack_files:
        process_file(os.path.join(path,file))

if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Usage:")
        print("JackAnalyzer.py <file.jack>")
        exit(1)
    
    path = sys.argv[1]

    if (os.path.isfile(path)):
        process_file(path)
    if (os.path.isdir(path)):
        process_dir(path)
    
    


    

    
        
