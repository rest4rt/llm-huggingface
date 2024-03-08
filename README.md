# Hugging Face LLM Plugin
[LLM](https://llm.datasette.io/) plugin for the HuggingFace Inference API.

Due to the unmanageable number of available models on HuggingFace, listing all of them is unfeasible and impractical, so you will need to manually add the models that you want to use. See instructions below.

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-huggingface
```

or, clone this repository and run `llm install .`.

## Configuration

Although the Inference API can supposedly work without one, I haven't tested it, so I recommend you get an API key from HuggingFace. [Here](https://huggingface.co/docs/api-inference/en/quicktour#get-your-api-token) are the instructions.

You can set that as an environment variable called `LLM_HUGGINGFACE_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set huggingface
```
```
Enter key: <paste key here>
```

## Usage

To use the plugin, you need to manually add the models you intend to use:

```bash
llm hf add <model-id> # for example, llm model hf add bigscience/bloom
```

You can also `llm hf list` to list all available models, which should also be listed when running `llm models` and `llm hf rm <model_id>` to remove a model you don't want to see in your list anymore.

Once the model is added, use llm normally.

```bash
llm -m huggingface/bigscience/bloom "What is AGI? According to"                                                         
```
```
What is AGI? According to the definition of the National Institute of Standards and Technology (NIST), AGI is a machine that
```

Available options are:
- `top_k`
- `top_p`
- `temperature`
- `length`: corresponds to the `max_new_tokens` parameter in the Inference API

```bash
llm -m huggingface/bigscience/bloom -o length 100 -o top_k 5 -o top_p 0.8 -o temperature 1.2 "What is AGI? According to"
```
```
What is AGI? According to the Wikipedia page, AGI is an artificial general intelligence. That is, an intelligence that can do any task that a human can. The article goes on to describe a few different approaches, but it is clear that no one has yet succeeded at creating a true AGI.
What is an AI? An AI is an artificial intelligence. It is a computer that is designed to think like a human. The AI is designed to do a task, or tasks, that are similar to what a human does
```

## Limitations

This was really just for me to scratch an itch and be able to play with models hosted on HuggingFace from the command line, I love llm and figured I might as well do a little extra work to be able to use it for this. It's not intended to be feature complete and it hasn't been tested much, but I'm happy to add more features if there is interest. 

- **Streaming**: not supported.
- **Chat Mode**: chat mode is untested and will almost certainly not work as expected.
- **Advanced Features**: while the plugin currently uses the `requests` library for API calls, integrating `huggingface_hub.InferenceClient` could unlock more advanced features in future versions.

## Contributing

Contributions to improve the plugin or add new features are welcome! If you encounter any issues or have suggestions for enhancements, please open an issue or submit a pull request. 

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments

- Thanks to the creator of [llm](https://github.com/simonw/llm) for the amazing CLI and the [llm-openrouter](https://github.com/simonw/llm-openrouter) plugin which I used as reference. Thanks also to [llm-ollama](https://github.com/taketwo/llm-ollama), both for the plugin and the reference.
