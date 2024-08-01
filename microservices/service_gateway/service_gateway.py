from microskel.service_template import ServiceTemplate
import events_client_module
import weather_client_module


class GatewayService(ServiceTemplate):

    def get_modules(self):
        return super().get_modules() + [events_client_module.GatewayModule(self),
                                        weather_client_module.GatewayModule(self)]

    def get_python_modules(self):
        return super().get_python_modules() + [events_client_module, weather_client_module]

    def custom_function(self, city):  # ca si exemplu
        data = self.injector.get(events_client_module.GatewayModule).get_events(city)
        return data


if __name__ == '__main__':
    GatewayService().start()