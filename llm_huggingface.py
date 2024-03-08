import click
import json
import llm
import requests
import os

from typing import Optional

DEBUG=False

def read_models():
    models_file = str(llm.user_dir()) + '/hf_models.txt'
    if not os.path.exists(models_file):
        return []

    with open(models_file, 'r') as file:
        content = file.read()
    models = content.split("\n")
    return models

def write_models(models):
    models_file = str(llm.user_dir()) + '/hf_models.txt'
    with open(models_file, 'w') as file:
        file.write('\n'.join(models))

@llm.hookimpl
def register_commands(cli):
    @cli.group(name="hf")
    def hf_group():
        "Commands for working with HuggingFace models"

    @hf_group.command(name="add")
    @click.argument('model_id')
    def add_model(model_id):
        """Add a new model."""
        models = read_models()
        models.append(model_id)
        write_models(sorted(models))

    @hf_group.command(name="rm")
    @click.argument('model_id')
    def rm_model(model_id):
        """Remove a model."""
        models = read_models()
        models = [ m for m in models if m != model_id ]
        write_models(sorted(models))

    @hf_group.command(name="list")
    def list_models():
        """List models that have been made available through HuggingFace."""
        for model in read_models():
            click.echo(model)

@llm.hookimpl
def register_models(register):
    for model in read_models():
        register(HuggingFace(model))

class HuggingFace(llm.Model):
    can_stream = False
    needs_key = "huggingface"

    class Options(llm.Options):
        length:      Optional[int]   = None
        top_k:       Optional[int]   = None
        top_p:       Optional[float] = None
        temperature: Optional[float] = None

    def __init__(self, model_id):
        self.model_id = 'huggingface/' + model_id
        self.url = "https://api-inference.huggingface.co/models/" + model_id

        key = llm.get_key("", "huggingface", "LLM_HUGGINGFACE_KEY")
        if key is None:
            raise llm.LLMError("Please set the key for huggingface or the environment variable LLM_HUGGINGFACE_KEY")
        self.headers = {"Authorization": f"Bearer {key}" }

    def __str__(self):
        return "HuggingFace: {}".format(self.model_id)

    def build_parameters(self, options):
        parameters = {}
        if options['length']:
            parameters['max_new_tokens'] = options['length']
        for opt in ['top_k','top_p','temperature']:
            if options[opt]:
                parameters[opt] = options[opt]
        return parameters

    def execute(self, prompt, stream, response, conversation=None):
        payload = { "inputs": prompt.prompt, "parameters": self.build_parameters(prompt.options.dict()) }
        yield self.query(payload)

    def query(self, payload):
        if DEBUG:
            print(f"URL: {self.url}, headers: {self.headers}")
            print(f"Payload: {payload}")

        response = requests.post(self.url, headers=self.headers, json=payload)
        if response.ok:
            resp = response.json()
            if DEBUG:
                print(f"Response: {resp}")
            return resp[0]['generated_text']
        else:
            return None

if __name__ == '__main__':
    model = HuggingFace('bigscience/bloom')
    resp = model.query({ "inputs": "The meaning of life is" })
    print(resp)
