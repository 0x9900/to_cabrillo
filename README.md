# to_cabrillo

Convert ADIF log files to Cabrillo contest format for amateur radio contest submissions.

## Overview

`to_cabrillo` is a Python utility that reads Amateur Data Interchange Format (ADIF) log files and generates Cabrillo format files suitable for submitting contest logs.

## Features

- Reads standard ADIF log files
- Generates properly formatted Cabrillo v3.0 files
- Supports various contest types
- Handles multiple bands and modes
- Validates QSO data during conversion
- Command-line interface

## Installation

### From PyPI

```bash
pip install to_cabrillo
```

### From Source

```bash
git clone https://github.com/0x9900/to_cabrillo.git
cd to_cabrillo
pip install .
```

## Usage

### Basic Usage

```bash
to_cabrillo -a CSSB2025.adi -c - --config ./contest-template.toml

START-OF-LOG: 3.0
CONTEST: CQ-WW-SSB
CALLSIGN: W6BSD
LOCATION: SCV
CATEGORY-OPERATOR: SINGLE-OP
CATEGORY-TRANSMITTER: ONE
CATEGORY-BAND: ALL
CATEGORY-POWER: LOW
CATEGORY-MODE: SSB
CATEGORY-ASSISTED: NON-ASSISTED
CATEGORY-STATION: FIXED
CATEGORY-OVERLAY: CLASSIC
EMAIL: f4wfx@bsdworld.org
NAME: Fred C.
SOAPBOX: RTTY contests are the best

QSO:  3730 PH 2025-02-22 0600 W6BSD  599    1 F8GAF    599  71 0
QSO:  3730 PH 2025-02-22 0600 W6BSD  599    2 F5TYQ    599  59 0
QSO:  3730 PH 2025-02-22 0600 W6BSD  599    3 PE1EWR   599   1 0
QSO:  3730 PH 2025-02-22 0601 W6BSD  599    4 F4KJN    599  46 0
QSO:  3730 PH 2025-02-22 0601 W6BSD  599    5 F8CRS    599  67 0
QSO:  3730 PH 2025-02-22 0601 W6BSD  599    6 TM3P     599  38 0
QSO:  3730 PH 2025-02-22 0601 W6BSD  599    7 F4GOP    599  61 0
QSO:  3730 PH 2025-02-22 0601 W6BSD  599    8 SE4E     599   2 0
END-OF-LOG:
```

### Command Line Options

```bash
usage: to_cabrillo [-h] [--config CONFIG] -a ADIF_FILE -c CABRILLO_FILE

ADIF to Cabrillo

options:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file (default: config.toml)
  -a ADIF_FILE, --adif-file ADIF_FILE
                        Adif filename
  -c CABRILLO_FILE, --cabrillo-file CABRILLO_FILE
                        Cabrillo filename (output)
```

## Requirements

- Python 3.12 or higher
- Standard Python libraries (no external dependencies)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the BSD 2-Clause License. See the LICENSE file for details.

## Author

Fred C. (0x9900)

## Resources

- [Cabrillo Format Specification](https://wwrof.org/cabrillo/)
- [ADIF Specification](https://adif.org/)
- [CQ World Wide Contest Information](https://cqww.com)

## Support

For issues, questions, or suggestions, please open an issue on the [GitHub repository](https://github.com/0x9900/to_cabrillo/issues).

---

**73 de 0x9900** 📻
