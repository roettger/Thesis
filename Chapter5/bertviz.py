from transformers import AutoTokenizer 
from bertviz.transformers_neuron_view import BertModel 
from bertviz. neuron_view import show 
model_ckpt = "bert-base-uncased" 
tokenizer = AutoTokenizer.from_pretrained(model_ckpt) 
model = BertModel.from_pretrained(model_ckpt) 
text = "I have been scared out of my senses for just now" 
show(model, "bert", tokenizer, text, display_mode="light", layer=0, head=8)