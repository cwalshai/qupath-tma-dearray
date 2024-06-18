# qupath-tma-dearray

This is a QuPath script to dearray TMA cores.

## Installation

1. Clone this repository.

2. Create a new python environment and install the required packages.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Update the path to the TMA whole slide image in the `dearray.py` script.

4. Update the path to the TMA GeoJSON file in the `dearray.py` script.

5. Run the script.

```bash
python dearray.py
```

Dearrated core images will be saved in the `cores` directory.