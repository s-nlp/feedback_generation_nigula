import re
import os

def preprocessing(text: str, offset: [tuple, list]):
    
    assert len(offset) == 2
    off1, off2 = [int(el) for el in offset]

    text = text[:off1] + "< < " + re.sub("\s+", " > > < < ", text[off1:off2].strip()) + " > > " + text[off2:]
    text = re.sub("\s+", " ", text.strip()).lower()
    
    return text

current_dir = os.path.dirname(os.path.realpath(__file__))


sorted_content_termins_twoplus = []
with open(os.path.join(current_dir,'complex_content_termins.txt')) as f:
    for l in f.readlines():
        sorted_content_termins_twoplus.append(l.strip())
        
sorted_grammar_termins_twoplus = []
with open( os.path.join(current_dir,'complex_grammar_termins.txt')) as f:
    for l in f.readlines():
        sorted_grammar_termins_twoplus.append(l.strip())

def adjust_grammar_terms(string):
    
    string = re.sub('(?<!\b)[ ](?=>)','',string)
    
    string = re.sub(' - ','-',string)
    string = re.sub(' \+ ','+',string)
    
    used_terms = []
    for gt in sorted_grammar_termins_twoplus:
        if len(re.findall(f"[ ](?={gt}>)",string))>0:
            used_terms.append(gt)
            string = re.sub(f"[ ](?={gt}>(?!>))"," <",string)

    open_brack = False
    new_list = []
    for t in string.split():
        if ">" in t and '>>' not in t:
            if open_brack == False:
                t = '<' + t
                new_list.append(t)
                open_brack = False
                continue
            open_brack = False
        elif '<' in t and '<<' not in t:
            open_brack = True
        new_list.append(t)
    
    return ' '.join(new_list)


def adjust_content_terms(string, verbose = False):
#     used_terms = []
    for ct in sorted_content_termins_twoplus:  

        string, subcount = re.subn(f"[ ](?={ct}>>)"," <<",string)
        if subcount > 0:
            if verbose == True: print(ct)
#             used_terms.append(ct)
            
    open_brack = False
    new_list = []
    for t in string.split():
        if '>>' in t:
            if open_brack == False:
                t = '<<' + t
                new_list.append(t)
                open_brack = False
                continue
            open_brack = False
        elif  '<<' in t:
            open_brack = True
        new_list.append(t)

    return ' '.join(new_list)


def upper_repl(match):
     return match.group(0).upper() 
    
    
def post_process_string(model_gener_string):
    adj_string = adjust_grammar_terms(model_gener_string.strip())
    adj_string = adjust_content_terms(adj_string)
    adj_string = adj_string[0].upper() + adj_string[1:]
    adj_string = re.sub(r"(?<=\. )\w", upper_repl, adj_string)
    return adj_string