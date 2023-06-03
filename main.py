import os
import json
import pandas as pd
import numpy as np


class ParserGeneric:
    file_path_configuration = os.path.join(os.path.dirname(__file__), "plugins.json")
    df = None

    def __init__(self, file_path_configuration=None):
        self.file_path = file_path_configuration or self.file_path_configuration

    def parse(self, **kwargs):
        input_value = kwargs.get("input_value")
        type_input = kwargs.get("type_input")
        acepted_types = self.get_acepted_types()
        if type_input not in acepted_types:
            raise Exception("Type not acepted")

        path_plugin = self.get_path_plugin(type_input)
        return_from_plugin = self.call_plugin(path_plugin, input_value)

        if isinstance(return_from_plugin, pd.DataFrame):
            self.df = return_from_plugin
        else:
            raise Exception("Return from parser error, return type not acepted")

        return return_from_plugin

    def get_acepted_types(self):
        full_json = json.load(open(self.file_path, "r"))
        return full_json.keys()

    def get_path_plugin(self, type_input):
        full_json = json.load(open(self.file_path, "r"))
        return full_json.get(type_input)

    def call_plugin(self, path_plugin, file_input):
        path_plugin = os.path.join(os.path.dirname(__file__), path_plugin)
        plugin = __import__(path_plugin)
        return plugin.parse(file_input)