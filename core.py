import yaml


class YAML:
    name = ""
    header = None
    OTHERS = []

    def __init__(self, name):
        self.OTHERS += [self]
        self.name = name

    @staticmethod
    def dump(data):
        return yaml.dump(data)

    def write(self, file):
        with open(file, "w") as f:
            f.write(YAML.dump(self.tostring()))

    @property
    def var(self):
        return self.name.replace(" ", "_").lower()

    @property
    def fullvar(self):
        return f"{self.header}.{self.var}"


class InputSelect(YAML):
    header = "input_select"
    OTHERS = []

    def __init__(self, name: str, options: list):
        super().__init__(name)
        self.options = options.copy()

    def todict(self):
        return {
            "name": self.name,
            "options": self.options,
            "initial": self.options[0],
        }

    def tostring(self):
        fulldata = {self.header: {item.var: item.todict() for item in self.OTHERS}}
        return yaml.dump(fulldata)


class InputNumber(YAML):
    header = "input_number"
    OTHERS = []

    def __init__(self, name, initial, min, max, step=1):
        super().__init__(name)
        self.initial = initial
        self.min = min
        self.max = max
        self.step = step

    def todict(self):
        return {
            "name": self.name,
            "initial": self.initial,
            "min": self.min,
            "max": self.max,
            "step": self.step,
        }

    def tostring(self):
        fulldata = {self.header: {item.var: item.todict() for item in self.OTHERS}}
        return yaml.dump(fulldata)


if __name__ == "__main__":
    settings = ["Home", "Away", "Asleep"]
    heating_setting = InputSelect("Heating Setting", settings)
    cooling_setting = InputSelect("Cooling Setting", settings)
    print(cooling_setting.tostring())

    heating_away_setpoint = InputNumber("Heating Away Setpoint", 60, 60, 80)
    heating_home_setpoint = InputNumber("Heating Home Setpoint", 70, 60, 80)
    heating_asleep_setpoint = InputNumber("Heating Asleep Setpoint", 65, 60, 80)
    print(heating_home_setpoint.tostring())
