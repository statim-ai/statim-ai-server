"""Module to download and init Models."""

# ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
# This is a example file

from typing import Any

from diffusers import AutoPipelineForText2Image


def create_model(local_files_only=True) -> Any:
    """
    Creates a Model.
    Model cration should be done in this method, to be used by:
    - Docker image build phase;
    - Normal service operation.

    Parameters
    ----------
    local_files_only : bool
        Definies if the model is restricted to only local files vs. downloading them.

    Returns
    -------
    Any
        The model object.

    """
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", variant="fp16", local_files_only=local_files_only)
    pipe.to("cpu")
    return pipe
