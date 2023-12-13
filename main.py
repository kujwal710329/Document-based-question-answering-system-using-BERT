# pip install pdfplumber
# pip install indic-transliteration

# pip install googletrans==3.1.0a0

# pip install nltk
# pip install -U gensim
# !pip install transformers
# pip install torch

import uvicorn
import pickle
# import request
from flask import Flask, jsonify, request
import pdfplumber
from googletrans import Translator
from fastapi import FastAPI, HTTPException, File, UploadFile




app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# ...

origins = ["*"]

# origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def index():
   return {"message":"hello world"}



# from fastapi import FastAPI, File, UploadFile

# @app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
# 	if not file.filename.endswith('.pdf'):
# 			return {"error": "Invalid file type, only PDF files allowed"}

# 	pdf = pdfplumber.open(file.filename)
# 	page = pdf.pages[0]
# 	pdf_txt = page.extract_text()
# 	pdf.close()
	
# 	return {"message": "File uploaded successfully", 'content':pdf_txt}

pdf_txt = ""

@app.post("/get_data")
async def get_data(data: dict):
	pdf_txt = data
	translator = Translator()
	def translate_text(text):
			translation = translator.translate(text, src='hi', dest='en')
			return translation.text
	pdf_txt = translate_text(pdf_txt)
	file = open('paragraph.txt', 'w') 
	file.write(pdf_txt) 
	file.close() 
	return pdf_txt
	print(pdf_txt)

@app.post("/ask_question")
async def get_answer(data:dict):
	import json
	question = json.dumps(data)
	# question = data
	# question = data['question']
	import nltk
	nltk.download('punkt')
	file = open("paragraph.txt", "r")
	pdf_txt = file.read()
	# print(content)
	file.close()

	tokens = nltk.sent_tokenize(pdf_txt)
			

	# import re
	# import gensim
	# from gensim.parsing.preprocessing import remove_stopwords

	# def clean_sentence(sentence, stopwords=False):
	# 	sentence = sentence.lower().strip()
	# 	sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
	# 	if stopwords:
	# 		sentence = remove_stopwords(sentence)
	# 	return sentence

	# def get_cleaned_sentences(tokens, stopwords=False):
	# 	cleaned_sentences = []
	# 	for row in tokens:
	# 		cleaned = clean_sentence(row, stopwords)
	# 		cleaned_sentences.append(cleaned)
	# 	return cleaned_sentences

	# cleaned_sentences = get_cleaned_sentences(tokens, stopwords=True)
	# cleaned_sentences_with_stopwords = get_cleaned_sentences(tokens, stopwords=False)


	import torch
	translator = Translator()
	# from transformers import BertForQuestionAnswering
	# model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

	# from transformers import BertTokenizer
	# tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')


	tokenizer = pickle.load(open('tokenizer.pkl', 'rb'))
	model = pickle.load(open('model.pkl', 'rb'))

	# question = "What factors have driven India's digital revolution in recent years?"
	answer = "";


	def answer_question(question, answer_text):

			input_ids = tokenizer.encode(question, answer_text, max_length=512, truncation=True)

			sep_index = input_ids.index(tokenizer.sep_token_id)

			num_seg_a = sep_index + 1

			num_seg_b = len(input_ids) - num_seg_a

			segment_ids = [0]*num_seg_a + [1]*num_seg_b

			assert len(segment_ids) == len(input_ids)

			start_scores, end_scores = model(torch.tensor([input_ids]), token_type_ids=torch.tensor([segment_ids]),return_dict = False)

			all_tokens = tokenizer.convert_ids_to_tokens(input_ids)

			score = float(torch.max(start_scores))
			answer_start = torch.argmax(start_scores)
			answer_end = torch.argmax(end_scores)
			tokens = tokenizer.convert_ids_to_tokens(input_ids)
			answer = tokens[answer_start]

			for i in range(answer_start + 1, answer_end + 1):

					if tokens[i][0:2] == ' ':
							answer += tokens[i][2:]

					else:
							answer += ' ' + tokens[i]
			return answer, score



	def expand_split_sentences(pdf_txt):
		new_chunks = nltk.sent_tokenize(pdf_txt)
		length = len(new_chunks)

		new_df = [];
		for i in range(length):
			paragraph = ""
			for j in range(i, length):
				tmp_token = tokenizer.encode(paragraph + new_chunks[j])
				length_token = len(tmp_token)
				if length_token < 510:
					paragraph = paragraph + new_chunks[j]
				else:
					break;
			new_df.append(translator.translate(paragraph).text)
		return new_df

	max_score = 0;
	final_answer = ""
	new_df = expand_split_sentences(pdf_txt)
	for new_context in new_df:
		ans, score = answer_question(question, new_context)
		if score > max_score:
			max_score = score
			final_answer = ans


	corrected_answer = ''

	for word in final_answer.split():

			if word[0:2] == '##':
					corrected_answer += word[2:]
			else:
					corrected_answer += ' ' + word

	result = {
		"corrected_answer":corrected_answer,
		"max_score":max_score,
		"txt":pdf_txt
	}
	return result
	print(corrected_answer)
	print(max_score)

# python -m uvicorn main:app --reload

if __name__ == '__main__':
  uvicorn.run(app, host='127.0.0.1', port=8000)