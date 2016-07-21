from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.contrib.completers import WordCompleter

COMMANDS = ["read", "describe"]


class JolokiaCliCompleter(Completer):
    def __init__(self, mbeans):
        self.mbean_dict = {mbean.absolute_object_name: mbean for mbean in mbeans}
        self.mbean_completer = WordCompleter([mbean.absolute_object_name for mbean in mbeans])

    def get_completions(self, document, complete_event):

        text_before_cursor = document.text_before_cursor
        words_before_cursor = text_before_cursor.split(" ")

        if len(words_before_cursor) > 1:
            # Command is already complete
            command = words_before_cursor[0]

            if command in ["read"]:
                if len(words_before_cursor) == 2:
                    for completion in self.mbean_completer.get_completions(document, complete_event):
                        yield completion
                elif len(words_before_cursor) == 3:
                    absolute_object_name = words_before_cursor[1]
                    if absolute_object_name in self.mbean_dict:
                        attributes = self.mbean_dict[absolute_object_name].attributes
                        attribute_completer = WordCompleter([attribute.attribute_name for attribute in attributes])
                        for completion in attribute_completer.get_completions(document, complete_event):
                            yield completion

        elif len(words_before_cursor) == 1:
            for possible_command in COMMANDS:
                if possible_command.startswith(words_before_cursor[0]):
                    yield Completion(possible_command, -len(possible_command))
