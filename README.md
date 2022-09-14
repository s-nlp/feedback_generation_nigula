# feedback_generation_nigula

This repository presents the solution of team __nigula__ in [GenChal 2022](https://fcg.sharedtask.org/) shared task dedicated to the feedback comment generation for writing learning. Feedback comment generation is a task where, given an input text, a system generates hints or explanatory notes that help language learners improve their writing skills.

The model is trained to generate a feedback to sucf errors as misuse of prepositions and other writing items such as discourse and lexical choice. 

# How to use

## Installation
```python
!pip install feedback_generation_nigula
```

## Generating feedback
```python

from feedback_generation_nigula.generator import FeedbackGenerator

fg = FeedbackGenerator(cuda_index = 0)
text_with_error = "The smoke flow my face ."
error_span = (10,17)

fg.get_feedback([text_with_error ], [error_span ]) 

# expected output ["When the <verb> <<flow>> is used as an <intransitive verb> to express'' to move in a stream'', a <preposition> needs to be placed to indicate the direction"]

```

## Augmentation of the dataset

The main feature of our solution was special method for augmentation of the initial dataset. Our approach to augmentation consists of two parts. First, we cut the initial sentence by the last word which is syntactically related to the words withn error span. Second, we use the rest of the text as a prompt to the language model so it generates an alternative end to the sentence with a given prefix.

Below is the function which truncate the sentence in such way that the words related to the error are kept and everything after them is skipped.
```python

from feedback_generation_nigula.augment import  get_smart_truncated_string

text = 'They can help their father or mother about money that we must use in the university too .'
offset = [37, 42]

truncated_text = get_smart_truncated_string(text, offset)

truncated_text
# expected output 'they can help their father or mother about money'
```

The truncated text is used as a prompt to a large pretrained language model and new sentences with slightly different content but with similar error are obtained.

```python
from feedback_generation_nigula.augment import Augmenter

aug = Augmenter(cuda_index = 0, model_name = "EleutherAI/gpt-neo-1.3B")
# the model here is quiet big (EleutherAI/gpt-neo-1.3B) so it is recommended to launch this with GPU on the machine with big RAM. 
# You can also use an alternative language model which fits your machine
# To select a different model use `model_name` variable when initializing Augmenter class
 
aug.augment(truncated_text, is_text_truncated = True)

aug.augment(text, is_text_truncated = False, err_word_offset = offset)

```

## Augmented version of train data

We used our augmentation approach to generate an augmented version of the original dataset from the organizers of the shared task. The augmented version can be found [here](feedback_generation_nigula/augmented_data.csv)

# Competition results

| rank | Participant ID | Precision | Recall |  F1.0  |
|------|:--------------:|:---------:|:------:|:------:|
| 1    | ihmana         | 0.6244    | 0.6186 | 0.6215 |
| 2    | nigula (ours)  | 0.6093    | 0.6093 | 0.6093 |
| 3    | TMUUED         | 0.6132    | 0.6047 | 0.6089 |

The official results page is [here](https://fcg.sharedtask.org/results/)

# Contacts

If you have any questions feel free to drop a line to [Nikolay](mailto:bbkhse@gmail.com)
