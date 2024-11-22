class HeatPumpThermostat:
    def __init__(self, room):
        self.room = room

    def write(self, file):
        with open(file, "w") as f:
            f.write(self.tostring().strip())

    def tostring(self):
        return f"""
input_select:
  {self.room}_heating_setting:
    name: "{self.room} Heating Setting"
    options:
      - Home
      - Away
      - Asleep
    initial: Home
  {self.room}_cooling_setting:
    name: "{self.room} Cooling Setting"
    options:
      - Home
      - Away
      - Asleep
    initial: Home

input_number:
  {self.room}_heating_home_setpoint:
    initial: 70
    step: 1
    min: 60
    max: 80
  {self.room}_heating_away_setpoint:
    initial: 60
    step: 1
    min: 60
    max: 80
  {self.room}_heating_asleep_setpoint:
    initial: 65
    step: 1
    min: 60
    max: 80
  {self.room}_cooling_home_setpoint:
    initial: 72
    step: 1
    min: 60
    max: 80
  {self.room}_cooling_away_setpoint:
    initial: 80
    step: 1
    min: 60
    max: 80
  {self.room}_cooling_asleep_setpoint:
    initial: 76
    step: 1
    min: 60
    max: 80

template:
  - sensor:
      - name: {self.room}_heating_setpoint
        state: >
          {{% if states("input_select.{self.room}_heating_setting") == "Home" %}}
            {{{{states("input_number.{self.room}_heating_home_setpoint")}}}}

          {{% elif states("input_select.{self.room}_heating_setting") == "Away" %}}
            {{{{states("input_number.{self.room}_heating_away_setpoint")}}}}

          {{% elif states("input_select.{self.room}_heating_setting") == "Asleep" %}}
            {{{{states("input_number.{self.room}_heating_asleep_setpoint")}}}}

          {{% endif %}}
  - sensor:
      - name: {self.room}_cooling_setpoint
        state: >
          {{% if states("input_select.{self.room}_cooling_setting") == "Home" %}}
            {{{{states("input_number.{self.room}_cooling_home_setpoint")}}}}

          {{% elif states("input_select.{self.room}_cooling_setting") == "Away" %}}
            {{{{states("input_number.{self.room}_cooling_away_setpoint")}}}}

          {{% elif states("input_select.{self.room}_cooling_setting") == "Asleep" %}}
            {{{{states("input_number.{self.room}_cooling_asleep_setpoint")}}}}

          {{% endif %}}


automation:
  id: "{self.room.capitalize()}HeatPumpOn"
  alias: "{self.room.capitalize()} Heat Pump On 2"
  triggers:
    - trigger: template
      value_template: >
        {{{{ states("sensor.{self.room}_temperature")|float < states("sensor.{self.room}_heating_setpoint")|float}}}}
  conditions:
    - condition: template
      value_template: >
        {{{{ states("binary_sensor.disableheatpumps") == "off" }}}}
  actions:
    - action: climate.set_temperature
      metadata: {{}}
      data:
        hvac_mode: heat
        temperature: '{{{{ states("sensor.{self.room}_heating_setpoint")|float + 4}}}}'
      target:
        entity_id: climate.{self.room}

  id: "{self.room.capitalize()}HeatPumpOff"
  alias: "{self.room.capitalize()} Heat Pump Off 2"
  triggers:
    - trigger: template
      value_template: >
        {{{{ states("sensor.{self.room}_temperature"|float >= states("sensor.{self.room}_heating_setpoint)|float)}}}}
  conditions: []
  actions:
    - action: climate.set_temperature
      metadata: {{}}
      data:
        hvac_mode: off
        temperature: '{{{{ states("sensor.{self.room}_heating_setpoint")|float + 4}}}}'
      target:
        entity_id: climate.{self.room}




 """


if __name__ == "__main__":
    hpt = HeatPumpThermostat("den")
    print(hpt.tostring())
