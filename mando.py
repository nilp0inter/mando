#!/usr/bin/env python3.6
import requests
import cmd2
import environconfig


class Config(environconfig.EnvironConfig):
    SERVER = environconfig.StringVar(default="localhost")
    PORT = environconfig.IntVar(default=8080)


def create_command(name):
    def _send_command(self, *args):
        requests.get(f"http://{Config.SERVER}:{Config.PORT}/sendCommand/{name}")
    return _send_command


class Mando(cmd2.Cmd):
    prompt = "mando> "
    pass

commands = requests.get(f"http://{Config.SERVER}:{Config.PORT}/getCommands").json()

for path in commands:
    name = f"do_{path.replace('/', '_')}"
    setattr(Mando, name, create_command(path))

Mando().cmdloop(intro="Welcome to Mando!")
