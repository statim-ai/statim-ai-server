import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
 

def create_model(local_files_only=True):
    model = AutoModelForCausalLM.from_pretrained("Writer/palmyra-small", local_files_only=local_files_only)
    tokenizer = AutoTokenizer.from_pretrained("Writer/palmyra-small", local_files_only=local_files_only)

    return (tokenizer, model)