#!/usr/bin/env python3.6
import requests
import cmd2
import environconfig

RELOAD = False

class ReloadCommands(Exception):
    """Reload the commands from server."""
    pass


class Config(environconfig.EnvironConfig):
    SERVER = environconfig.StringVar(default="localhost")
    PORT = environconfig.IntVar(default=8080)


def create_command(name):
    def _send_command(self, *args):
        requests.get(f"http://{Config.SERVER}:{Config.PORT}/sendCommand/{name}")
    return _send_command


class Mando(cmd2.Cmd):
    prompt = "mando> "
    @classmethod
    def from_commands(cls, commands):
        class _Mando(cls):
            pass

        for path in commands:
            setattr(_Mando,
                    f"do_{path.replace('/', '_')}",
                    create_command(path))
        return _Mando

    @staticmethod
    def get_commands():
        return requests.get(f"http://{Config.SERVER}:{Config.PORT}/getCommands").json()

    def do_learn(self, name):
        global RELOAD
        print(requests.get(f"http://{Config.SERVER}:{Config.PORT}/learnCommand/{name}").content)
        RELOAD = True
        return True

    def do_forget(self, name):
        global RELOAD
        print(requests.get(f"http://{Config.SERVER}:{Config.PORT}/forgetCommand/{name}").content)
        RELOAD = True
        return True


if __name__ == '__main__':
    commands = Mando.get_commands()
    mando = Mando.from_commands(commands)
    mando().cmdloop(intro="Welcome to Mando!")
    while RELOAD:
        RELOAD = False
        commands = Mando.get_commands()
        mando = Mando.from_commands(commands)
        mando().cmdloop(intro="Commands reloaded...")
