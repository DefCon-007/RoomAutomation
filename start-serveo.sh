#!/bin/bash
nohup ssh -R autobot:80:localhost:1234 serveo.net & 
