import spacy
nlp=spacy.load('en_core_web_md')

from transformers import pipeline

def isbetween(index, offset_list):
    return offset_list[0] <= int(index) <= offset_list[1]


def get_smart_truncated_string(text, err_word_offset, debug = False):
    
    spacy_parsing = nlp(text)
    err_word = text[err_word_offset[0]:err_word_offset[1]]
    
    text = text.lower()
    text_keep_initial = text[:err_word_offset[1]]
    err_word = err_word.lower()
    
    if debug == True:
        print(text)
        print(err_word_offset)
        print(f"error word <{err_word}>")
    
    words_to_keep = err_word.split()
    last_index_to_keep = err_word_offset[1]

    error_syntax_pairs = []
 
    for token in spacy_parsing:
        # print("{:<15} {:^10} {:>15} {:>15}".format(str(token.head.text), str(token.dep_), str(token.text), str(token.head.idx)))
        if token.dep_ != 'punct':
            if isbetween(token.head.idx, err_word_offset) or isbetween(token.idx, err_word_offset):
                if debug == True:print("{:<15} {:^10} {:>15} {:>15}  {:>15}".format(str(token.head.text), str(token.dep_), str(token.text), str(token.idx), str(token.head.idx)))

                words_to_keep.append(token.head.text)
                words_to_keep.append(token.text)
                
                end_of_token = token.idx + len(token.text)
                end_of_token_head = token.head.idx + len(token.head.text)
                maximal_end = max(end_of_token, end_of_token_head)
                
                pair = token.head.text + '_' + token.dep_ + '_' + token.text
                error_syntax_pairs.append(pair)

                if maximal_end > last_index_to_keep:
                    last_index_to_keep = maximal_end
                    if debug == True:print("Enlarge index", maximal_end)

            else:
                # print(f"{token.head.idx} and {token.idx} not between {err_word_offset}")
                pass
        
        
    words_to_keep = list(set(words_to_keep))
    
    
    THRESHOLD = 3
    #if there are not enough connections engage more words
    if len(words_to_keep) - len(err_word.split()) <=THRESHOLD:
        for token in spacy_parsing:
            if token.dep_ != 'punct':
                if token.head.text in words_to_keep or token.head.text in words_to_keep:

                    if any([t not in words_to_keep for t in [token.head.text, token.text]]):
                        
                        if debug == True:print("{:<15} {:^10} {:>15} {:>15}  {:>15}".format(str(token.head.text), str(token.dep_), str(token.text), str(token.idx), str(token.head.idx)))
                        
                        token_to_process = token.head if token.head.text not in words_to_keep  else  token

                        end_of_token = token_to_process.idx + len(token_to_process.text)
                        
                        words_to_keep.append(token_to_process.text)
                        
                        pair = token.head.text + '_' + token.dep_ + '_' + token.text
                        error_syntax_pairs.append(pair)

                        if end_of_token > last_index_to_keep:
                            
                            last_index_to_keep = end_of_token
                            
                            if debug == True:print("Enlarge index by force", end_of_token)
                        else:
                            if debug == True:print(f"Force adding of word <{token_to_process.text}>")
 
            if len(words_to_keep)> THRESHOLD:# if the dependent word are already available in the back then it is ok and we stop
                break  
        
    text_to_keep = text[:last_index_to_keep]
    words_to_keep = '_'.join(sorted(set(words_to_keep))).lower()
    
    error_syntax_pairs = sorted([el.lower() for el in error_syntax_pairs if el.split('_')[0] != el.split('_')[1]])
    error_syntax_pairs = '&'.join(error_syntax_pairs)
    
    if debug == True:
        print(text_keep_initial)
        print(">>>")
        print(text_to_keep)
        
        print(f"words_to_keep {words_to_keep}")
        
        print(f"error_syntax_pairs {error_syntax_pairs}")
        
    return text_to_keep


class Augmenter():
    
    def __init__(self, cuda_index: [int, str], model_name = "EleutherAI/gpt-neo-1.3B"):
        
        self.generator = pipeline('text-generation', model=model_name, device = cuda_index)
        
    def augment(self, text: str, is_text_truncated: [list, tuple], err_word_offset = None,
               min_length = 20, max_length = 100, do_sample = True):
        
        if is_text_truncated == False:
            assert err_word_offset is not None
            text = get_smart_truncated_string(text,err_word_offset)
            
        new_texts = self.generator(text, do_sample=do_sample, min_length=min_length, max_length = max_length)
        
        return new_texts