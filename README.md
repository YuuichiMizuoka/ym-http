# THIS IS A "JUST FOR FUN PROJECT", PLEASE DON'T ACTUALLY USE THIS
# ym-http
A simple http server written in python without using any of pythons existing http libraries
## why?
I just wanted to try writing my own http server to learn more about the http protocol and about software development

## usage
`python main.py` (Start the HTTP server delivering the http folder inside the project structure)
`python main.py [folder to be served]` (Start the HTTP server delivering the given folder)

## TODO (maybe)
Some things i would still like to experiment with in the future are:
- more robust http parsing and error handling
- more robust handling of the tcp/ip socket (dynamic package sizes, streaming, etc...)
- basic header support (basically just to return any header, instead of the current none)
- config files
- basic auth
- threading
- Content-Type Header 
- Range Header (useful when trying to download big files or for streaming video)