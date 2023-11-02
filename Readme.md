# Chatbot development with chatterbot

## Introduction to Chatbot "Charlie"
Users interact with the chatbot through a web interface by opening 
[charlie.html](http://10.10.240.11:4040/charlie.html) in a browser of their choice. 

The port 4040 is used to reach the author's docker environment, for students the ports 4041 and 4042 are reserved.

A nginx web server serves the page "charlie.html". Whenever a user enters a question it is sent to the 
web server which in turn forwards it to a python server (based on unicorn + flask) 
that actually hosts the chatterbot-based chatbot.

For more information about ChatterBot see [here](https://chatterbot.readthedocs.io/en/stable/examples.html).

The chatbot has one function "get_answer" in file charlie.py (technically reached through the 
REST endpoint "chat"). The quality of Charlie's answers strongly depends on the training performed beforehand.

## Starting the server environment

- goto project directory: `cd cai-bot`
- Start nginx web server: enter `docker compose up -d` to start the nginx + flask server

## Stopping the server environment

- terminate docker servers: `docker compose down` in directory `cai-bot`

## Training the chatbot

To train the chatbot open the file `charlie.py` (e.g. in nice editor - command is `ne`) and enter 
chat sequences. Technically a chat sequence is a list of strings:

```python
    trainer.train([
        "Hi!", 		# users question or statement
        "Hey there!", 	# chatbot answer
    ])
```
