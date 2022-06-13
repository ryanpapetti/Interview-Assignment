

from happytransformer import HappyTextToText, TTTrainArgs

import errant,csv
ANNOTATOR = errant.load('en')
DEVICE = 'cpu'
happy_tt = HappyTextToText("T5", "t5-base")

import gc
from datasets import load_dataset

gc.collect()
import torch
torch.cuda.empty_cache()
# print(torch.cuda.memory_summary(device=None, abbreviated=False))






def remove_excess_spaces(text):

    replacements = [
    (" .", "."), 
    (" ,", ","),
    (" '", "'"),
    (" ?", "?"),
    (" !", "!"),
    (" :", "!"),
    (" ;", "!"),
    (" n't", "n't"),
    (" v", "n't"),
    (" 've", "'ve"),
    ("2 0 0 6", "2006"),
    ("5 5", "55"),
    ("4 0 0", "400"),
    ("1 7-5 0", "1750"),
    ("2 0 %", "20%"),
    ("5 0", "50"),
    ("1 2", "12"),
    ("1 0", "10"),
    ('" ballast water', '"ballast water') #specific example
    ]
    for rep in replacements:
        text = text.replace(rep[0], rep[1])

        return text








def generate_csv(csv_path, dataset):
    with open(csv_path, 'w', newline='') as csvfile:
        writter = csv.writer(csvfile)
        writter.writerow(["input", "target"])
        for case in dataset:
            input_text = "grammar: " + case["sentence"]
            for correction in case["corrections"]:
                # a few of the cases are blank strings. So we'll skip them
                if input_text and correction:
                    writter.writerow([remove_excess_spaces(input_text), remove_excess_spaces(correction)])










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




def break_up_paragraph(text):
    return text.split('. ') #gets the sentences from the text





def get_corrections(original_text):
    broken_up_text = break_up_paragraph(original_text)
    corrections = {}

    for sentence in broken_up_text:
        corrected_sentences = correct(sentence, max_candidates=1)
        for corrected_sentence in corrected_sentences:
            corrections[sentence] = (corrected_sentence,get_edits(sentence, corrected_sentence))

    return corrections






def main():

    train_dataset = load_dataset("jfleg", split='validation[:]')
    eval_dataset = load_dataset("jfleg", split='test[:]')
    generate_csv("data/jfleg_train.csv", train_dataset)
    generate_csv("data/jfleg_eval.csv", eval_dataset)


    before_result = happy_tt.eval("data/jfleg_eval.csv")
    print("Before loss: ", before_result.loss)


    args = TTTrainArgs(batch_size=1, num_train_epochs=4)
    happy_tt.train("data/jfleg_train.csv", args=args)
    happy_tt.save("model_dir")



    after_result = happy_tt.eval("data/jfleg_eval.csv")
    print("After loss:", after_result.loss)

    sample_text = "We was at the garden and seen plants. Green plants, with strong roots, survive the best."

    corrections = get_corrections(sample_text)


    for original_sentence, proposed_edits in corrections.items():
        new_sentence, edits = proposed_edits
        print(f"In order to improve your original sentence:\n\n {original_sentence}\n\ntry the proposed changes:\n")
        for ind,edit in enumerate(edits):
            print(f"{ind+1}: Change '{edit[1]}' to '{edit[4]}' ({edit[0]})\n\n")
        print(f"After changes, the new sentence could read: {new_sentence}\n\n")




if __name__ == '__main__':
    main()





