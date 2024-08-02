from abc import ABC, abstractmethod
import threading
from decouple import config
class LoadBalancer(ABC):
    @abstractmethod
    def get_instance(self, instances):
        pass


class RoundRobin(LoadBalancer):
    def __init__(self):
        self.index = 0

    def get_instance(self, instances):
        instance = instances[self.index]
        self.index = (self.index + 1) % len(instances)
        return instance


class LeastConnections(LoadBalancer):
    def __init__(self):
        self.connections = {}

    def get_instance(self, instances):
        for instance in instances:
            if instance not in self.connections:
                self.connections[instance] = 0

        least_connections_instance = min(instances, key=lambda instance: self.connections[instance])
        self.connections[least_connections_instance] += 1

        return least_connections_instance

    def release_instance(self, instance):
        if instance in self.connections:
            self.connections[instance] -= 1

LOAD_BALANCER_STRATEGIES = {
    'ROUND_ROBIN': RoundRobin,
    'LEAST_CONNECTIONS': LeastConnections
}

def get_load_balancer(strategy_name: str):
    strategy_class = LOAD_BALANCER_STRATEGIES.get(strategy_name)
    if strategy_class is None:
        raise ValueError(f"Unknown load balancer strategy: {strategy_name}")
    return strategy_class()


