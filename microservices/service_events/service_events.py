from microskel.service_template import ServiceTemplate

import events_module


class Events(ServiceTemplate):
    def __init__(self, name):
        super().__init__(name)

    def get_python_modules(self):
        return super().get_python_modules() + [events_module]


if __name__ == '__main__':
    Events('events').start()
