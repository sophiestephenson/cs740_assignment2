#!/bin/sh

ps -ax | grep chord.py | awk '{print $1}' | xargs kill