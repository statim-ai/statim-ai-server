from transformers import T5Tokenizer, T5ForConditionalGeneration
 

def create_model(local_files_only=True):
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small", local_files_only=local_files_only)
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small", local_files_only=local_files_only)

    return (tokenizer, model)