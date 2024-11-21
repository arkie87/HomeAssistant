import yaml


class YAML:
    name = ""
    header = None
    OTHERS = []

    def __init__(self, name):
        self.OTHERS += [self]
        self.name = name

    @property
    def var(self):
        return self.name.replace(" ", "_").lower()

    @property
    def fullvar(self):
        return f"{self.header}.{self.var}"

    def tostring(self):
        fulldata = {self.header: {item.var: item.todict() for item in self.OTHERS}}
        return yaml.dump(fulldata)


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


class SetpointSensor(YAML):
    header = "sensor"
    OTHERS = []

    def __init__(self, name, setting, pairs):
        super().__init__(name)
        self.setting = setting
        self.pairs = pairs
        self.state = []
        self.state += [f'{{% if states("{setting.fullvar}") ==  "{pairs[0][0]}"%}}']
        self.state += [f'  {{{{ states("{pairs[0][1].fullvar}") }}}}']
        for pair in pairs[1:]:
            self.state += [f'{{% elif states("{setting.fullvar}") ==  "{pair[0]}"%}}']
            self.state += [f'  {{{{ states("{pair[1].fullvar}") }}}}']

    def todict(self):
        return [{"name": self.var, "state": "".join(self.state)}]

    def tostring(self):
        fulldata = [{self.header: item.todict()} for item in self.OTHERS]
        return yaml.dump(fulldata)


settings = ["Home", "Away", "Asleep"]
heating_setting = InputSelect("Heating Setting", settings)
cooling_setting = InputSelect("Cooling Setting", settings)
print(cooling_setting.tostring())

heating_away_setpoint = InputNumber("Heating Away Setpoint", 60, 60, 80)
heating_home_setpoint = InputNumber("Heating Home Setpoint", 70, 60, 80)
heating_asleep_setpoint = InputNumber("Heating Asleep Setpoint", 65, 60, 80)
print(heating_home_setpoint.tostring())

heating_setpoint = SetpointSensor(
    "Heating Setpoint",
    heating_setting,
    [
        ("Home", heating_home_setpoint),
        ("Away", heating_away_setpoint),
        ("Asleep", heating_asleep_setpoint),
    ],
)

print(heating_setpoint.tostring())
with open("heating_setpoint.yaml", "w") as f:
    f.write(yaml.dump(heating_setpoint.tostring()))
