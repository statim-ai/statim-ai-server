import os
from importlib import import_module

MODELS_PATH = f'{os.getcwd()}/download_models'
MODEL_MODULE = '{}.create_model'

# Get model directories
directories = []
for _, subdirs, _ in os.walk(MODELS_PATH):
    for dir in subdirs:
        directories.append(dir)


# For each model directory
model_modules_names = []
for directory in directories:
    model_modules_names.append(MODEL_MODULE.format(directory))


# Load model modules
model_modules = map(import_module, model_modules_names)
for model_module in model_modules:
    model_module.create_model(local_files_only=False)
