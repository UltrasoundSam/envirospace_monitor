# EnviroSpace Monitor

## Overview

EnviroSpace Monitor is an environmental sensing platform designed to monitor and characterise sensory conditions within campus spaces.

The project aims to support neurodivergent students and staff by collecting objective environmental measurements that may influence sensory comfort. Using a Raspberry Pi Zero and Pimoroni Enviro sensor platform, the system captures environmental parameters such as temperature, humidity, light levels, and ambient noise. These data can then be used to build a clearer understanding of how different spaces are experienced and to support the development of sensory-aware campus navigation tools.

The long-term vision is to create a distributed network of sensing nodes capable of identifying and mapping environmental conditions across campus, helping users make informed decisions about where to study, work, or socialise.

## Project Aims

The objectives of the project are to:

- Monitor environmental conditions within campus spaces.
- Identify factors that may contribute to sensory stimulation.
- Build a dataset describing sensory characteristics of different locations.
- Support the development of sensory accessibility tools.
- Investigate how Internet of Things (IoT) technologies can improve accessibility and inclusivity for neurodivergent individuals.

## Features

### Current Features

- Continuous environmental monitoring
- Temperature measurement
- Humidity measurement
- Ambient light monitoring
- Noise level monitoring
- Timestamped data collection
- Local data storage
- Wireless connectivity via Raspberry Pi

### Planned Features

- Centralised data aggregation
- Real-time environmental dashboards
- Sensory accessibility maps
- Historical trend analysis
- Mobile application integration
- Environmental alerts and notifications
- Predictive analytics for sensory load estimation

## Hardware Platform

The prototype currently uses:

| Component | Purpose |
| --------- | ------- |
| Raspberry Pi Zero | Edge computing platform |
| Pimoroni Enviro | Environmental sensor suite |
| Wi-Fi Connectivity | Data transmission |
| MicroSD Card | Local storage |
| Power Supply | Continuous operation |

## Environmental Parameters

The system currently measures:

| Parameter | Relevance |
| --------- | --------- |
| Temperature | General comfort and environmental conditions |
| Humidity | Environmental comfort and air quality context |
| Light Level | Identification of brightly lit environments |
| Noise Level | Identification of acoustically stimulating spaces |
| Atmospheric Pressure | Additional environmental context |

## System Architecture

```text
┌─────────────────┐
│ Campus Location │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Raspberry Pi    │
│ Zero + Enviro   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Collection │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Publish via MQTT│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Database Ingest │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analytics &     │
│ Accessibility   │
│ Applications    │
└─────────────────┘
```

---

## Repository Structure

```text
envirospace-monitor/
│
├── src/
│   ├── sensors/
│   ├── data_collection/
│   ├── processing/
│   └── communication/
│
├── debug_data/
│
├── data/
│
├── tests/
│
├── docs/
│
├── deploy/
│
├── pyproject.toml
│
├── README.md
│
└── main.py
```

## Installation

### Prerequisites

- Raspberry Pi OS
- Python 3.13+

### Clone the Repository

```bash
git clone https://github.com/UltrasoundSam/envirospace-monitor.git
cd envirospace-monitor
```

<!--
### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the System

Start environmental monitoring:

```bash
python main.py
```

Run automated tests:

```bash
pytest
```

---

## Example Output

```json
{
  "timestamp": "2026-11-18T15:30:00Z",
  "temperature": 21.8,
  "humidity": 47.2,
  "light_level": 320,
  "noise_level": 53.1
}
```

-->
## Accessibility Focus

EnviroSpace Monitor is intended to support accessibility and inclusion by providing objective measurements of environmental conditions that may influence sensory comfort.

The system does not attempt to determine how an individual experiences a space. Instead, it provides environmental information that can help users make informed decisions based on their own preferences and sensory needs.

## Ethical Considerations

This project:

- Does not collect personally identifiable information.
- Focuses solely on environmental measurements.
- Seeks to operate transparently and responsibly.
- Is designed with privacy-by-design principles.
- Supports research into accessible and inclusive campus environments.

## Future Work

Potential future enhancements include:

- Multiple distributed sensing nodes across campus.
- Live web-based dashboards.
- Interactive campus sensory maps.
- Machine learning approaches for environmental classification.
- Occupancy estimation.
- User feedback integration.
- Personalised sensory preference profiles.

## Research Context

This project forms part of a wider investigation into how Internet of Things (IoT) technologies and environmental sensing can be used to improve accessibility for neurodivergent individuals within educational environments.

The platform provides a foundation for collecting real-world environmental data that can support future research into sensory accessibility and inclusive campus design.

## Licence

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Status

🚧 **Research Prototype / Active Development**

EnviroSpace Monitor is currently under active development and evaluation.
