"""Module to download and init Models."""

# ⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️
# This is a example file

from typing import Any

from transformers import AutoModelForCausalLM, AutoTokenizer


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
    model = AutoModelForCausalLM.from_pretrained(
        "Writer/palmyra-small", local_files_only=local_files_only
    )
    tokenizer = AutoTokenizer.from_pretrained(
        "Writer/palmyra-small", local_files_only=local_files_only
    )

    return (tokenizer, model)
