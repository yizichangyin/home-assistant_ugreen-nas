## NAS picture

![image](https://github.com/user-attachments/assets/9b46ddb6-3854-4943-af14-e08ba20b9138)

```yaml
type: picture
image: /local/images/ugreen_dxp.png
       # corresponds to /www/images/ugreen_dxp.png in VS Code
```

## Volume occupied / free I

![image](https://github.com/user-attachments/assets/881d55ed-7125-4ad9-a1f4-777acf9d4a89)

```yaml
type: horizontal-stack
cards:
  - type: gauge
    entity: sensor.ugreen_nas_storage_volume_1_used
    unit: GB
    needle: false
    min: 0
    max: 440
    name: Vol1 - VM, dB, Containers
  - type: gauge
    entity: sensor.ugreen_nas_storage_volume_2_used
    unit: GB
    needle: false
    min: 0
    max: 3710
    name: Vol 2 - Data
```

## Volume occupied / free II

![image](https://github.com/user-attachments/assets/16f7680b-6f78-40c9-b191-1e6002b27b01)

```yaml
type: horizontal-stack
cards:
  - name: Vol1 - VM, dB, Containers
    type: gauge
    entity: sensor.ugreen_nas_storage_volume_1_used
    needle: true
    min: 0
    max: 440
    unit: GB
    severity:
      green: 0
      yellow: 330
      red: 400
  - name: Vol 2 - Data
    type: gauge
    entity: sensor.ugreen_nas_storage_volume_2_used
    needle: true
    min: 0
    max: 3710
    unit: GB
    severity:
      green: 0
      yellow: 2780
      red: 3340
```

## Status view

![image](https://github.com/user-attachments/assets/f6b25bc0-be26-47c3-8296-bb0638e087eb)

_Requires card-mod, mini-graph-card!_

```yaml
type: horizontal-stack
cards:
  - type: custom:mini-graph-card
    hours_to_show: 24
    points_per_hour: 2
    animate: true
    hour24: true
    height: 150
    entities:
      - sensor.ugreen_nas_cpu_usage
    icon: mdi:chip
    decimals: 0
    state_adaptive_color: true
    show_state: true
    name: CPU Load
    line_color: "#00ff26"
    line_width: 7
    color_thresholds:
      - value: 20
        color: "#00ff26"
      - value: 50
        color: "#ddff00"
      - value: 60
        color: "#ff8c00"
      - value: 80
        color: "#ff5900"
      - value: 90
        color: "#ff0000"
    show:
      extrema: true
      name_adaptive_color: true
      icon_adaptive_color: true
    card_mod:
      style: |
        ha-card { 
          background: transparent;
        }  
  - type: custom:mini-graph-card
    hours_to_show: 24
    points_per_hour: 2
    animate: true
    hour24: true
    height: 150
    entities:
      - sensor.ugreen_nas_cpu_temperature
    state_adaptive_color: true
    show_state: true
    name: CPU Temp
    line_color: "#00ff26"
    line_width: 7
    color_thresholds:
      - value: 20
        color: "#00ff26"
      - value: 50
        color: "#ddff00"
      - value: 60
        color: "#ff8c00"
      - value: 80
        color: "#ff5900"
      - value: 90
        color: "#ff0000"
    show:
      extrema: true
      name_adaptive_color: true
      icon_adaptive_color: true
    card_mod:
      style: |
        ha-card { 
          background: transparent;
        }  
  - name: RAM Load
    type: custom:mini-graph-card
    hours_to_show: 24
    points_per_hour: 2
    animate: true
    hour24: true
    height: 150
    entities:
      - sensor.ugreen_nas_ram_usage
    decimals: 0
    icon: mdi:memory
    state_adaptive_color: true
    show_state: true
    line_color: "#00ff26"
    line_width: 7
    color_thresholds:
      - value: 20
        color: "#00ff26"
      - value: 50
        color: "#ddff00"
      - value: 60
        color: "#ff8c00"
      - value: 80
        color: "#ff5900"
      - value: 90
        color: "#ff0000"
    show:
      extrema: true
      name_adaptive_color: true
      icon_adaptive_color: true
    card_mod:
      style: |
        ha-card { 
          background: transparent;
        }  
```
