from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch

from processing import preprocessing, post_process_string

class FeedbackGenerator():
    
    def __init__(self, cuda_index: [bool, int, str], model_name = "SkolkovoInstitute/GenChal_2022_nigula"):
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.model.eval();
        
        if cuda_index != False:
            device = torch.cuda.device(cuda_index)
            self.model.to(device);
        
        
    def paraphrase(self, text, error_offsets:list, temperature=1.1, beams=3, 
                   num_return_sequences = 1, do_sample = False,
                  repetition_penalty = 1.1, max_length_multiplier = 3):
        texts = [text] if isinstance(text, str) else text
        assert len(error_offsets) == len(texts)
        
        texts_processed = []
        for txt, off in zip(texts,error_offsets):
            txt_processed = preprocessing(txt, off)
            texts_processed.append(txt_processed)        
            
        print(texts_processed)
        
        inputs = self.tokenizer(texts_processed, return_tensors='pt', padding=True)['input_ids'].to(self.model.device)
        result = self.model.generate(
            inputs, 
            num_return_sequences=num_return_sequences, 
            do_sample=do_sample, 
            temperature=temperature, 
            repetition_penalty=repetition_penalty, 
            max_length=int(inputs.shape[1] * max_length_multiplier) ,
            bad_words_ids=[[2]],  # unk
            num_beams=beams,
        )
        texts = [self.tokenizer.decode(r, skip_special_tokens=True) for r in result]
        
        print(texts)
        
        if isinstance(text, str):
            return post_process_string(texts[0])
        
        texts = [post_process_string(t) for t in texts]
        
        return texts