from core import YAML


class Template(YAML):
    OTHERS = []


class TemplateSensor(Template):
    header = "sensor"

    def __init__(self, name, state):
        super().__init__(name)
        self.state = state

    def todict(self):
        return [{"name": self.var, "state": ">" + "".join(self.state)}]

    def tostring(self):
        fulldata = {"template": [{self.header: item.todict()} for item in self.OTHERS]}
        return self.dump(fulldata)


class TemperatureSensor(TemplateSensor):
    def __init__(self, name, temperature):
        state = f"{{{{{temperature}|float}}}}"
        super().__init__(name, state)


class ThermostatModeSensor(TemplateSensor):
    def __init__(self, name, temperature, heating_setpoint, cooling_setpoint):
        self.temperature = temperature
        self.heating = heating_setpoint
        self.cooling = cooling_setpoint
        state = []
        state += [
            f'{{% if states("{temperature.fullvar}")|float <  states("{heating_setpoint.fullvar}")|float %}}'
        ]
        state += ["heat"]
        state += [
            f'{{% elif states("{temperature.fullvar}")|float >  states("{cooling_setpoint.fullvar}")|float %}}'
        ]
        state += ["cool"]
        state += [f"{{% else %}}"]
        state += ["off"]
        state += [f"{{% endif %}}"]

        super().__init__(name, state)


class SetpointSensor(TemplateSensor):
    def __init__(self, name, setting, pairs):
        self.setting = setting
        self.pairs = pairs
        state = []
        state += [f'{{% if states("{setting.fullvar}") ==  "{pairs[0][0]}"%}}']
        state += [f'  {{{{ states("{pairs[0][1].fullvar}") }}}}']
        for pair in pairs[1:]:
            state += [f'{{% elif states("{setting.fullvar}") ==  "{pair[0]}"%}}']
            state += [f'  {{{{ states("{pair[1].fullvar}") }}}}']

        state += [f"{{% endif %}}"]
        super().__init__(name, state)


if __name__ == "__main__":
    from core import InputNumber, InputSelect

    settings = ["Home", "Away", "Asleep"]
    heating_setting = InputSelect("Heating Setting", settings)
    cooling_setting = InputSelect("Cooling Setting", settings)

    heating_away_setpoint = InputNumber("Heating Away Setpoint", 60, 60, 80)
    heating_home_setpoint = InputNumber("Heating Home Setpoint", 70, 60, 80)
    heating_asleep_setpoint = InputNumber("Heating Asleep Setpoint", 65, 60, 80)

    cooling_away_setpoint = InputNumber("Heating Away Setpoint", 60, 60, 80)
    cooling_home_setpoint = InputNumber("Heating Home Setpoint", 70, 60, 80)
    cooling_asleep_setpoint = InputNumber("Heating Asleep Setpoint", 65, 60, 80)

    heating_setpoint = SetpointSensor(
        "Heating Setpoint",
        heating_setting,
        [
            ("Home", heating_home_setpoint),
            ("Away", heating_away_setpoint),
            ("Asleep", heating_asleep_setpoint),
        ],
    )

    cooling_setpoint = SetpointSensor(
        "Cooling Setpoint",
        cooling_setting,
        [
            ("Home", cooling_home_setpoint),
            ("Away", cooling_away_setpoint),
            ("Asleep", cooling_asleep_setpoint),
        ],
    )
    temperature = TemperatureSensor("Temperature", 70)
    ThermostatModeSensor("Mode", temperature, heating_setpoint, cooling_setpoint)

    print(heating_setpoint.tostring())

    heating_setpoint.write("templates.yaml")
