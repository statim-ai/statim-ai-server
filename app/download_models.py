import os

files = os.listdir(f'{os.getcwd()}/download_models')

create_model_files = [file for file in files if file.endswith('_create_model.py')]
create_model_files = map(lambda file: file.replace('.py', ''), create_model_files)

modules = map(__import__, create_model_files)
for module in modules:
    module.create_model(local_files_only=False)