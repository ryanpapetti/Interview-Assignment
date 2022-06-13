
import errant
ANNOTATOR = errant.load('en')
DEVICE = 'cpu'
def load_model(path):
    from happytransformer import HappyTextToText
    return HappyTextToText("T5", "t5-base", load_path=path)




happy_tt = load_model('../model_dir')


def break_up_paragraph(text):
    return text.split('. ') #gets the sentences from the text



def correct(input_sentence, max_candidates=1):
    correction_prefix = "gec: "
    input_sentence = correction_prefix + input_sentence
    input_ids = happy_tt.tokenizer.encode(input_sentence, return_tensors='pt')
    input_ids = input_ids.to(DEVICE)

    preds = happy_tt.model.to(DEVICE).generate(
        input_ids,
        do_sample=True, 
        max_length=128, 
        top_k=50, 
        top_p=1.5, 
        early_stopping=True,
        num_return_sequences=max_candidates)

    corrected = set()
    for pred in preds:  
        corrected.add((happy_tt.tokenizer.decode(pred, skip_special_tokens=True).strip()))
    return corrected



def get_corrections(original_text):
    broken_up_text = break_up_paragraph(original_text)
    corrections = {}

    for sentence in broken_up_text:
        corrected_sentences = correct(sentence, max_candidates=1)
        for corrected_sentence in corrected_sentences:
            corrections[sentence] = (corrected_sentence,get_edits(sentence, corrected_sentence))

    return corrections







def _get_edits(orig, cor):
    orig = ANNOTATOR.parse(orig)
    cor = ANNOTATOR.parse(cor)
    alignment = ANNOTATOR.align(orig, cor)
    edits = ANNOTATOR.merge(alignment)

    if len(edits) == 0:  
        return []

    edit_annotations = []
    for e in edits:
        e = ANNOTATOR.classify(e)
        edit_annotations.append((e.type[2:], e.o_str, e.o_start, e.o_end,  e.c_str, e.c_start, e.c_end))
            
    if len(edit_annotations) > 0:
        return edit_annotations
    else:    
        return []

def get_edits(orig, cor):
    return _get_edits(orig, cor)