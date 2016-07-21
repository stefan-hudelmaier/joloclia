from urlparse import urlparse

from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from collections import defaultdict

from pyjolokia import Jolokia

from completer import JolokiaCliCompleter


class MBean:
    def __init__(self, object_name, domain, description):
        self.absolute_object_name = "%s:%s" % (domain, object_name)
        self.object_name = object_name
        self.description = description
        self.domain = domain
        self.attributes = []

    def add_attribute(self, attribute):
        self.attributes.append(attribute)


class Attribute:
    def __init__(self, attribute_name, attribute_type):
        self.attribute_name = attribute_name
        self.attribute_type = attribute_type


# def get_bottom_toolbar_tokens(cli):
#    return [(Token.Toolbar, ' Topic: %s' % selected_topic)]


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#333333',
})


def get_completer(mbeans):
    return JolokiaCliCompleter(mbeans)


def create_attribute(attribute_name, json):
    # print(json)
    return Attribute(attribute_name, json['type'])


def create_mbean(object_name, domain, json):
    mbean = MBean(object_name=object_name, domain=domain, description=json['desc'])

    if 'attr' in json:

        for attribute_name in json['attr'].keys():
            mbean.add_attribute(create_attribute(attribute_name, json['attr'][attribute_name]))

    return mbean


if __name__ == '__main__':

    url_string = 'http://127.0.0.1:8161/api/jolokia'
    url = urlparse(url_string)

    j = Jolokia(url.geturl())
    j.auth(httpusername='admin', httppassword='admin')

    request = j.request(type='list')
    domains = request['value'].keys()

    # Multimap
    mbeans_by_domain = defaultdict(list)
    mbeans = []

    for domain in domains:
        object_names = request['value'][domain].keys()

        for object_name in object_names:
            mbean = create_mbean(object_name, domain, request['value'][domain][object_name])
            mbeans.append(mbean)

            mbeans_by_domain[domain].append(mbean)
            # print(request['value'][domain])

    while True:
        # answer = prompt(u'Choose topic: ', get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
        answer = prompt(u'%s%s# ' % (url.netloc, url.path), completer=get_completer(mbeans), style=style)

        command_with_arguments = answer.split(" ")

        if len(command_with_arguments) == 0:
            continue

        command = command_with_arguments[0]
        arguments = command_with_arguments[1:]

        if command == "read":
            if len(arguments) == 0:
                print 'Missing argument'
                continue

            # print "Reading", arguments[0]
            response = j.request(type='read', mbean=arguments[0], attribute=arguments[1])

            print response['value']
