# Smart-Question-Answering-System-on-Document

It's Smart-Question Answering System on short as well as long documents. It can automatically find answers to matching questions directly from documents. The deep learning language model converts the questions and documents to semantic vectors to find the matching answer.

## Approches:

<!--- Question Answering System Using Simple Split and Cosine Similarity (Naive Approach)
 - Question Answering System Using Word2Vec Embedding Technique -->
- Question Answering System with Fine-Tuned BERT Technique 

## Challenges

- Bert is a really powerful model for tackling a question-answering problem. However, it comes up with the limitation of 512 tokens and the documents were really longer than 512 tokens. In order to handle this limitation I wrote the function "expand_split_sentences", which split and expand sentences i.e., it makes paragraphs with lesser than 512 tokens and makes data frames of that paragraph. In this, more than one data frame contains the correct answer so we will find the best answer by finding the max start score.

## Pretrained Model and Dataset Used

<!-- - word2vec -->
- bert-large-uncased-whole-word-masking-finetuned-squad
- bert-squad_1.1
