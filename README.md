# 2d Scroller Game With Server

A simple 2d game made with pygame, written to incorporate a connection to a remote websocket server. Multiple players may connect to the server, and see eachother moving around.

## Requirements

You need to have python installed, watch a youtube video for this if you don't know how.

## Installation

Download the project as a .zip file, then extract to a folder

```bash
cd folder
pip install -r requirements.txt
```

## Running the script

For server:
```bash
python server.py
```

For client:
```bash
python client.py
```

## Other notes

- The client will not run if there is no server to connect to, so even if you have nobody else to play with, you have to run a server.
- The server ip has to be specified in the config.json file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
