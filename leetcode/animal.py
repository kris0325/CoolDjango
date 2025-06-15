"""
以下是关于Fortinet OA（在线评估）中涉及的Python面向对象设计（OOD）部分的解决方案示例，特别是与动物园相关的设计。

动物园管理系统设计示例
在这个示例中，我们将设计一个简单的动物园管理系统。这个系统将包含动物、饲养员和动物园的基本功能。

设计思路说明
1.Animal类：这是一个基类，定义了动物的基本属性和行为（如发出声音）。子类（如Lion和Elephant）实现了具体的行为。
2.Zookeeper类：表示饲养员，负责喂养动物。
3.Zoo类：管理动物和饲养员，提供添加和显示功能。

"""


class Animal:
    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def make_sound(self):
        raise NotImplementedError("Subclasses should implement this method!")


class Lion(Animal):
    def make_sound(self):
        return "Roar!"


class Elephant(Animal):
    def make_sound(self):
        return "Trumpet!"


class Zookeeper:
    def __init__(self, name: str):
        self.name = name

    def feed_animal(self, animal: Animal):
        print(f"{self.name} is feeding {animal.name} the {animal.species}.")


class Zoo:
    def __init__(self):
        self.animals = []
        self.zookeeper = []

    def add_animal(self, animal: Animal):
        self.animals.append(animal)

    def add_zookeeper(self, zookeeper: Zookeeper):
        self.zookeeper.append(zookeeper)

    def show_animals(self):
        for animal in self.animals:
            print(f"{animal.name} the {animal.species} says {animal.make_sound()}")


if __name__ == "__main__":
    lion = Lion("Leo", "Lion")
    elephant = Elephant("Dumbo", "Elephant")
    zookeeper = Zookeeper("Alice")

    zoo = Zoo()
    zoo.add_animal(lion)
    zoo.add_animal(elephant)
    zoo.add_zookeeper(zookeeper)

    zoo.show_animals()
    zookeeper.feed_animal(lion)
