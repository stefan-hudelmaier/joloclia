from prompt_toolkit import prompt
from subprocess import check_output
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

from pyjolokia import Jolokia


class MBean:
    def __init__(self, object_name, description):
        self.object_name = object_name
        self.description = description
        self.attributes = []

    def add_attribute(self, attribute):
        self.attributes.append(attribute)


class Attribute:
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name


# def get_bottom_toolbar_tokens(cli):
#    return [(Token.Toolbar, ' Topic: %s' % selected_topic)]


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})


class TopicCompleter(Completer):
    def get_completions(self, document, complete_event):
        yield Completion('completion', start_position=0)


# def get_topics():
#    return [topic for topic in
#            check_output("cd %s && bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181" % KAFKA_HOME,
#                         shell=True).split('\n') if topic != ""]


# def get_topic_completer():
#    return WordCompleter(get_topics())


def create_attribute(attribute_name, json):
    print(attribute_name, json)


def create_mbean(object_name, json):
    mbean = MBean(object_name=object_name, description=json['desc'])

    print(json)
    if 'attr' in json:

        for attribute_name in json['attr'].keys():
            print(json['attr'][attribute_name])
            mbean.add_attribute(create_attribute(attribute_name, json['attr'][attribute_name]))


if __name__ == '__main__':

    j = Jolokia('http://127.0.0.1:8161/api/jolokia')
    j.auth(httpusername='admin', httppassword='admin')

    request = j.request(type='list')
    domains = request['value'].keys()

    mbeans = []

    for domain in domains:
        object_names = request['value'][domain].keys()

        for object_name in object_names:
            mbeans.append(create_mbean(object_name, request['value'][domain][object_name]))
            # print(request['value'][domain])

    #print(domains())
    """
    while True:

        answer = prompt(u'Choose topic: ', get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                        completer=get_topic_completer(), style=style)

        selected_topic = answer
        """
