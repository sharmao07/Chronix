# Chronix Planning

## Project Overview

Chronix is a custom digital alarm clock built around the Seeed XIAO ESP32C3.

The clock will use a 2.25 inch TFT display, Mechanical keyboard switches, a buzzer, a custom PCB, and a custom 3D printed enclosure.

## Main Features

- Digital clock
- Date and day display
- Configurable alarm
- Snooze function
- Alarm dismissal
- Wake up challenge
- TFT based user interface
- Mechanical key controls
- Buzzer alarm

## Hardware

- Seeed XIAO ESP32C3
- 2.25 inch TFT display
- 12 keyboard switches
- 12 keycaps
- 12 diodes
- 3.3v buzzer
- Screen wiring
- Screws
- Heat set inserts

### Planned Usage

I'm planning to use 9 switches in a 3×3 matrix.

## Controls

| Key | Function |
|---|---|
| 1 | Previous / Left |
| 2 | Up |
| 3 | Next / Right |
| 4 | Alarm |
| 5 | Select |
| 6 | Back |
| 7 | Down |
| 8 | Snooze |
| 9 | Stop / Dismiss |

## Display

The main screen will show:

- Current time
- Current day/date
- Alarm time
- Alarm status

## Wake-up Challenge

When the alarm activates, Chronix will display a simple challenge
that must be completed before the alarm can be dismissed.

## GPIO Plan

The BLARE documentation provides 11 GPIO pins on the XIAO ESP32C3.

Planned allocation:

- 4 GPIOs for the TFT
- 1 GPIO for the buzzer
- 6 GPIOs for the 3×3 key matrix

The exact GPIO numbers will be finalized during PCB design.

## Enclosure

Chronix will use a custom 3D-printed enclosure.

The enclosure will contain:

- TFT opening
- Mechanical switch openings
- PCB mounting points
- ESP32 clearance
- Buzzer opening
- Screw or heat set insert locations

## Design Goals

- Compact desktop form factor
- Clean user interface
- Easy physical controls
- Custom PCB
- Custom enclosure
- Fully functional alarm clock
