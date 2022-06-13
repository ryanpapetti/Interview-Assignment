# Feedback Fruits Interview Assignment

## Ryan Papetti

## June 10-12, 2022

### Prompt

Create a tool in Python that accepts a piece of text as input and returns a rephrased version of the text that is "better", as well as an explanation of why the text is "better". What "better" means is up to you, and you can scope the text to a more specific use case.


### Implementation

#### Accessing Web App (without training model)

1. Create/activate a new virtual environment using the provided `requirements.txt`

2. `cd` into `grammar_corrector` directory

3. [Download model configurations](https://s3.console.aws.amazon.com/s3/buckets/fbf-interview-project?region=eu-west-3&tab=objects) and store inside a directory called `model_dir`
    - I made the bucket ***completely public*** but if there are issues, let me know and I can send configurations some other way
    - At last resort, retraining the model would produce the appropriate configurations.

4. `cd` into `app` directory

5. Run `python main.py` and open browser to `http://127.0.0.1:8095/`

6. App should be running!
#### Accessing Web App (with training model)


1. Create/activate a new virtual environment using the provided `requirements.txt`

2. `cd` into `grammar_corrector` directory

3. Run `python train.py` or run each cell in `model_training_exploration.ipynb`. Some output will print.

4. After model training, model and updated data are added to `model_dir` and `data`, respectively

5. `cd` into `app` directory

6. Run `python main.py` and open browser to `http://127.0.0.1:8095/`

7. App should be running!



#### Final grammar_corrector tree structure

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── static
│   │   ├── duck2.gif
│   │   ├── index.css
│   │   ├── jquery.js
│   │   ├── nicepage.css
│   │   ├── nicepage.js
│   │   └── text_correction.js
│   ├── templates
│   │   └── index.html
│   └── utils.py
├── data
│   ├── jfleg_eval.csv
│   └── jfleg_train.csv
├── deployment.ipynb
├── model_dir
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── spiece.model
│   ├── tokenizer_config.json
│   └── tokenizer.json
├── model_training_exploration.ipynb
└── train.py
```

#### Implementation Overview

- Used HuggingFace T5-Base Text2Text Transformer and HuggingFace jfleg grammatical error correction dataset to train model
- Performed minor data correction by text replacement; otherwise used T5 tokenizer to encode/decode data
- Trained model locally on GPU several times. Final one uses 4 epochs and a batch size of 1 (mainly for simplicity)
- Popular errant annotation module helps match corrections between original sentence and corrected one  
- Built rudimentary client-side demo in a Flask app that allows user to input text, see suggested corrections, and generate again if need be. 


### Getting Started 

- Originally, I was torn between three ideas on how to make text "better":

    1. Improve its vocabulary
    2. Improve its success in answering a prompt
    3. Improve its grammar.

- I decided to go with 3 as my final option; 1 was too difficult to find how ML could fit in and 2 was too abstract. 


#### Choosing a Model Type

- The project **specifically** requests to train a model and use that model to produce "mutations" of the original text.

- A ML model type that could accomplish this task is Seq2Seq or Text2Text as these can accept sequences (text) as both input and output
    - In other words, a Transformer Deep Learning model

    - While not the simplest approach, HuggingFace's interface makes use *fast* and *easy*

- [Vennify's t5-base grammar correction model](https://huggingface.co/vennify/t5-base-grammar-correction) served as foundational piece for this implementation


#### Choosing a Dataset

- Vennify's model makes use of [HuggingFace's jfleg English grammatical error correction corpus](https://huggingface.co/datasets/jfleg)

    - Same dataset is used for this project's model

- Some minor preprocessing is done to help standardize input and output text (and also improve generation)




### Biggest Joys + Challenges

#### What I Enjoyed

- HuggingFace & errant (first serious time using them)

- Researching various NLP model architectures

- Building Flask app / deploying model

- Testing (qualitatively) model's ability


#### What I Found Challenging

- Choosing an idea to pursue

- Finding an actionable dataset (both in terms of size and usability)

- Tuning transformer model hyperparameters after training

- Controlling generative output (model overfits fast on dataset and sometimes produces bad output)


### If I Had More Time... 

In order of perceived importance...

1. Either create or find a larger dataset (with same or higher quality instances)
2. Augment model with a fluency scoring model (for improving output's readability)
3. Benchmark/compare model against state-of-the-art implementations (such as [Grammarly's GECTOR](https://github.com/grammarly/gector))
4. Further preprocess data with regex or manual editing to improve data quality
5. Dockerize Flask app (had too many bugs) 



### Special Thanks To...

- [Gramformer Model](https://github.com/PrithivirajDamodaran/Gramformer), for showing how errant can be used in a user-friendly manner for output

- Vennify AI's, for their [advice](https://www.vennify.ai/fine-tune-grammar-correction/) on implementing a HuggingFace grammar correction model 

- HappyTransformer and HuggingFace, for providing great resources on training, using, and deploying HuggingFace transformer models
