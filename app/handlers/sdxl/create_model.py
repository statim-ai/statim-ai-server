from diffusers import AutoPipelineForText2Image
 

def create_model(local_files_only=True):
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", variant="fp16", local_files_only=local_files_only)
    pipe.to("cpu")
    return pipe