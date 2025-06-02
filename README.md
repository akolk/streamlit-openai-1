[![PyPI version](https://badge.fury.io/py/streamlit-openai.svg)](https://badge.fury.io/py/streamlit-openai)

Welcome to the `streamlit-openai` package!

This package provides a Streamlit component for building interactive chat 
interfaces powered by OpenAI.

Here’s a quick overview of the package’s key features:

- Easily create chat interfaces in Streamlit
- Real-time streaming responses using the Responses API
- Integration with OpenAI tools: function calling, file search, code interpreter, vision, and more
- File input support for richer interactions
- Fully customizable chat interface, including model selection, temperature settings, and more
- Support for saving and retrieving chat history

# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Schematic Diagram](#schematic-diagram)
- [Features](#features)
  - [Function Calling](#function-calling)
  - [File Inputs](#file-inputs)
    - [Message Attachments](#message-attachments)
    - [Static File Upload](#static-file-upload)
    - [File Uploader Widget](#file-uploader-widget)
- [Chat Completions API](#chat-completions-api)
  - [Function Calling](#function-calling-1)
  - [Vision](#vision)
- [Assistants API](#assistants-api)
  - [Function Calling](#function-calling-2)
  - [File Search](#file-search)
  - [Code Interpreter](#code-interpreter)
  - [Existing Assistant Retrieval](#existing-assistant-retrieval)
  - [Existing Vector Store Retrieval](#existing-vector-store-retrieval)
- [Customization](#customization)
  - [Model Selection](#model-selection)
  - [Temperature](#temperature)
  - [Instructions](#instructions)
  - [Avatar Image](#avatar-image)
  - [Welcome Message](#welcome-message)
  - [Example Messages](#example-messages)
  - [Info Message](#info-message)
  - [Input Box Placeholder](#input-box-placeholder)
  - [Chat History](#chat-history)
  - [Function Calling](#function-calling-3)
    - [Image Generation Example](#image-generation-example)
    - [Web Search Example](#web-search-example)
    - [Audio Transcription Example](#audio-transcription-example)

# Installation

```sh
$ pip install streamlit-openai streamlit openai
```

# Usage

Export your OpenAI API key:

```sh
$ export OPENAI_API_KEY='sk-...'
```

Save the following code to `app.py`:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Chat()

st.session_state.chat.run()
```

Run the app:

```sh
$ streamlit run app.py
```

# Schematic Diagram

The following diagram illustrates the `Container` and `Block` classes used
to create a chat interface:

![Schematic diagram](schematic_diagram.png)

# Features

## Function Calling

You can define and invoke custom functions within a chat using OpenAI's 
function calling capabilities. To create a custom function, provide the 
`name`, `description`, `parameters`, and `handler` arguments when initializing 
a `CustomFunction`.

Below is an example of a custom function that generates an image based on a 
user-provided prompt:

```python
import streamlit as st
import openai
import streamlit_openai

if "chat" not in st.session_state:
    def handler(prompt):
        client = openai.OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    
    generate_image = streamlit_openai.CustomFunction(
        name="generate_image",
        description="Generate an image based on a given prompt.",
        parameters={
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "A description of the image to be generated.",
                }
            },
            "required": ["prompt"]
        },
        handler=handler
    )

    st.session_state.chat = streamlit_openai.Chat(functions=[generate_image])

st.session_state.chat.run()
```

## File Inputs

You can provide file inputs to the chat interface, allowing the assistant
to access and utilize the content of the files during the conversation.

### Message Attachments

You can upload files in the chat by clicking the attachment icon or dragging 
them into the input box. Uploaded files are sent along with your message, and 
the assistant can access their content. This behavior is controlled by the 
`accept_file` parameter when initializing the `Chat` class. Below is an 
example of how to enable file uploads in the chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Chat(
        accept_file="multiple" # Allow multiple file uploads (default)
        # accept_file=True,    # Allow only one file upload
        # accept_file=False,   # Disable file uploads entirely
    )

st.session_state.chat.run()
```

### Static File Upload

You can upload files statically by providing the `uploaded_files` parameter
when initializing the `Chat` class. This allows you to include files that
are always available in the chat interface. Below is an example of how to
upload a PDF file statically:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Chat(
        uploaded_files=["example.pdf"]
    )

st.session_state.chat.run()
```

### File Uploader Widget

You can use `st.file_uploader` to let users upload files dynamically. While the 
widget allows file removal, the files remain in the chat history and context. 
Here's an example of how to use it:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Chat()
    
uploaded_files = st.sidebar.file_uploader("Upload Files", accept_multiple_files=True)

st.session_state.chat.run(uploaded_files=uploaded_files)
```

## Vision
The `Chat` class supports OpenAI's vision capabilities, enabling image input 
processing in chat. Here's an example:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Chat(
        message_files=["example.jpeg"]
    )

st.session_state.chat.run()
```

## File Search

You can allow models to search your files for relevant information before 
generating a response by using OpenAI’s File Search capabilities. To enable 
File Search, set the `file_search` parameter to `True` when initializing the 
`Assistants` class. Note that this feature is available only in the Assistants 
API and not in the Chat Completions API from OpenAI. Below is an example of
how to enable File Search in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Assistants(file_search=True)
    
uploaded_files = st.sidebar.file_uploader("Upload Files", accept_multiple_files=True)

st.session_state.chat.run(uploaded_files=uploaded_files)
```

## Code Interpreter

You can allow models to run Python code in a sandboxed execution environment 
using OpenAI’s Code Interpreter capabilities. To enable Code Interpreter, set 
the `code_interpreter` parameter to `True` when initializing the `Assistants` 
class. Note that this feature is available only in the Assistants API and not 
in the Chat Completions API from OpenAI. Below is an example of how to enable 
Code Interpreter in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Assistants(code_interpreter=True)

st.session_state.chat.run()
```

## Existing Assistant Retrieval
You can retrieve an existing assistant by providing its ID when initializing
the `Assistants` class. This allows you to continue a conversation with an
existing assistant without losing context. Below is an example of how to
retrieve an existing assistant in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Assistants(assistant_id="asst_...")
    
st.session_state.chat.run()
```

## Existing Vector Store Retrieval
You can retrieve one or more existing vector stores by providing their IDs when
initializing the `Assistants` class. This allows you to use pre-existing vector
stores for searching and retrieving relevant information during the chat. Note 
that the `vector_store_ids` parameter is only applicable when the 
`file_search` parameter is set to `True`. Below is an example of how to 
retrieve existing vector stores in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.Assistants(
        file_search=True,
        vector_store_ids=["vs_...", "vs_..."]
    )
st.session_state.chat.run()
```

# Customization

## Model Selection
The default model used by the assistant in the chat interface is `gpt-4o`. You
can customize the model used by the assistant by providing the `model` parameter
when initializing the `ChatCompletions` or `Assistants` class. Below is an
example of how to customize the model in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(model="o3-mini")

st.session_state.chat.run()
```

## Temperature
You can customize the temperature used by the assistant in the chat interface
by providing the `temperature` parameter when initializing the `ChatCompletions`
or `Assistants` class. The temperature controls the randomness of the 
assistantant's responses. Below is an example of how to customize the 
temperature in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(temperature=0.5)

st.session_state.chat.run()
```

## Instructions
You can customize the instructions provided to the assistant in the chat
interface by providing the `instructions` parameter when initializing the
`ChatCompletions` or `Assistants` class. The instructions provide context
for the assistant and can help guide its responses. Below is an example of
how to customize the instructions in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(
        instructions="You are a helpful assistant."
    )

st.session_state.chat.run()
```

## Avatar Image
You can customize the avatar images for the assistant and user in the chat interface
by providing the `assistant_avatar` and `user_avatar` parameters when initializing
the `ChatCompletions` or `Assistants` class. Below is an example of how to
customize the avatar images in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(assistant_avatar="🦖")

st.session_state.chat.run()
```

## Welcome Message
You can customize the welcome message displayed in the chat interface by
providing the `welcome_message` parameter when initializing the `ChatCompletions`
or `Assistants` class. Below is an example of how to customize the welcome
message in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(
        welcome_message="Hello! How can I assist you today?"
    )

st.session_state.chat.run()
```

## Example Messages
You can use the `example_messages` parameter to provide example messages in 
the chat interface, helping users understand how to interact with the 
assistant. Below is an example of how to provide example messages in a chat 
interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(
        example_messages=[
            "Can you tell me a joke?",
            "What is the capital of France?",
            "How do you make a paper airplane?",
            "What is the weather like today?",
        ],
    )

st.session_state.chat.run()
```

## Info Message
The `info_message` parameter allows you to display an informational message 
within the chat interface, helping users grasp key details about how to 
interact effectively with the assistant. Here's an example of how to include 
such a message in the chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(
        info_message="This is an informative and helpful message.",
    )

st.session_state.chat.run()
```

## Input Box Placeholder
You can customize the placeholder text for the input box in the chat interface
by providing the `placeholder` parameter when initializing the `ChatCompletions`
or `Assistants` class. Below is an example of how to customize the placeholder
text in a chat interface:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(
        placeholder="Type your message here..."
    )

st.session_state.chat.run()
```

## Chat History
You can save chat history to allow users to continue conversations across 
different sessions. The `ChatCompletions` and `Assistants` classes include a 
`save` method for this purpose. The chat history will be saved as a ZIP file. 
Note that currently, only text content is saved -- other file types (e.g., 
images) are not supported. Below is an example of how to save a chat history:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions()
    
with st.sidebar:
    if st.button("Save"):
        st.session_state.chat.save("history.zip")

st.session_state.chat.run()
```

After saving the chat history, you can load it in a new session by passing the 
history parameter when initializing the `ChatCompletions` or `Assistants` 
class. Below is an example of how to load a chat history:

```python
import streamlit as st
import streamlit_openai

if "chat" not in st.session_state:
    st.session_state.chat = streamlit_openai.ChatCompletions(history="history.zip")

st.session_state.chat.run()
```

## Function Calling
You can define and call custom functions within a chat using OpenAI’s function
calling capabilities. To create a custom function, define a `CustomFunction`
class that takes two input arguments: `definition` (a dictionary describing
the function) and `function` (the actual callable method).

### Image Generation Example
You can create a custom function to generate an image from a given prompt. 
Below is an example:

```python
import streamlit as st
import openai
import streamlit_openai

if "chat" not in st.session_state:
    definition = {
        "name": "generate_image",
        "description": "Generate an image based on a given prompt.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "A description of the image to be generated.",
                }
            },
            "required": ["prompt"]
        }
    }

    def function(prompt):
        client = openai.OpenAI()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    
    generate_image = streamlit_openai.utils.CustomFunction(definition, function)

    st.session_state.chat = streamlit_openai.Assistants(
        functions=[generate_image],
    )

st.session_state.chat.run()
```

### Web Search Example
You can create a custom function to search the web using a given query. Below 
is an example:

```python
import streamlit as st
import openai
import streamlit_openai

if "chat" not in st.session_state:
    definition = {
        "name": "search_web",
        "description": "Searches the web using a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Search query.",
                }
            },
            "required": ["prompt"]
        }
    }

    def function(prompt):
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content
    
    search_web = streamlit_openai.utils.CustomFunction(definition, function)

    st.session_state.chat = streamlit_openai.ChatCompletions(
        functions=[search_web],
    )

st.session_state.chat.run()
```

### Audio Transcription Example

You can create a custom function to transcribe audio files. Below is an 
example:

```python
import streamlit as st
import openai
import streamlit_openai

if "chat" not in st.session_state:
    definition = {
        "name": "transcribe_audio",
        "description": "Convert speech to text.",
        "parameters": {
            "type": "object",
            "properties": {
                "audio_file": {
                    "type": "string",
                    "description": "The audio file to transcribe.",
                }
            },
            "required": ["audio_file"]
        }
    }

    def function(audio_file):
        client = openai.OpenAI()
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=open(audio_file, "rb"),
        )
        return response.text
    
    transcribe_audio = streamlit_openai.utils.CustomFunction(definition, function)

    st.session_state.chat = streamlit_openai.ChatCompletions(
        functions=[transcribe_audio],
    )

uploaded_files = st.sidebar.file_uploader("Upload Files", accept_multiple_files=True)

st.session_state.chat.run(uploaded_files=uploaded_files)
```