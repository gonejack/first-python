from dataclasses import dataclass
from typing import List

from kafka import KafkaConsumer


@dataclass
class Config:
    topic: List[str]
    brokers: List[str]
    groupId: str


class Consumer:
    consumer: KafkaConsumer

    config: Config

    def __init__(self, config: Config):
        self.config = config

    def start(self):
        self.consumer = KafkaConsumer(*self.config.topic,
                                      bootstrap_servers=self.config.brokers,
                                      group_id=self.config.groupId)

        for msg in self.consumer:
            print(msg)
            print(msg.value.decode(encoding="utf-8"))


if __name__ == '__main__':
    config: Config = Config(
        topic=["test_topic"],
        brokers=[
            "192.168.11.30:9093",
            "192.168.11.31:9093",
            "192.168.11.32:9093",
        ],
        groupId="test_group"
    )

    consumer = Consumer(config)
    consumer.start()
