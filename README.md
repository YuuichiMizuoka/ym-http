# A WORD OF WARNING

### PLEASE ASSUME NOTHING IN THIS PROJECT WORKS

This is a personal "just for fun" / academic exercise project. No part of the code should be assumed to be working, well
written, etc...!

# ym-http

A simple http server written in python without using any of pythons existing http libraries

## why?

I just wanted to try writing my own http server to learn more about the http protocol and about software development

## usage

`python main.py` - Start the HTTP server using the configuration found at conf/ym-http.conf

`python main.py [folder to be served]` - Start the HTTP server delivering the given folder at /

## Configuration

The configuration can be found at conf/ym-http.conf.

### Basic syntax rules

- The configuration values themselves have to be separated with tabs and/or spaces (at least one, but they can be more if this makes your
config looks nicer). 
- Each configuration line has to be separated through a new line in the file
- The server uses a "first match" search, so if you configure the path / at the top nothing else will ever match
- empty lines and lines starting with `#` will be ignored 

### Configure folder/file delivery

A simple folder/file delivery can be configured using the line `/[HTTP_PATH] [FOLDER_PATH]  FS  NO_AUTH`. p.e:

```
/images     my_images/  FS  NO_AUTH
/           http/       FS  NO_AUTH
```
this config delivers the folder my_images at /images and the folder http at /

### Configure Basic Auth

If you wish to enable basic auth, change the `NO_AUTH` to `BASIC` followed by an arrow of allowed basic auth header
values (this will be replaced with hashes in the future). p.e:

`BASIC [YWRtaW46YWRtaW4xMjM=, Z3Vlc3Q6Z3Vlc3Q=]` to allow for admin:admin123 and guest:guest

## DONE (features?)

- simple one line start to deliver a single directory
- simple configuration for more complex path/folder mappings
- basic auth, separately configurable for each mapping
- basic headers in response object (currently just Server and www-authenticated, but it's a start)
- url encoding (percent encoding), so the server url can contain encoded non-ascii characters

## TODO (maybe)

Some things that would be fun to experiment with in the future:

- more robust http parsing and error handling (somewhat implemented)
- more robust handling of the tcp/ip socket (dynamic package sizes, streaming, etc...) (with GET supported)
- config files (simple 'deliver folder x at path y' for now, maybe a simple reverse proxy later, \<static\> \<reverse\>)
- threading
- Content-Type Header (how do you find out what encoding a file has, oh god)
- Range Header (useful when trying to download big files or for streaming video)
- support url parameters (? parameters should not be interpreted as file names)
