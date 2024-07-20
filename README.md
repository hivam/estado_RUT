# NIT Validation Script

## Overview

This script automates the process of validating NIT (Número de Identificación Tributaria) against the DIAN (Dirección de Impuestos y Aduanas Nacionales) website. It reads a list of NIT from a CSV file, checks each NIT to see if it has already been validated, and if not, queries the DIAN website for the current status. The results are saved in new CSV files.

![UML sequence diagram](/flow_chart.png)

## License

This program is distributed under the terms of the GNU Lesser General Public License (LGPL) v3. See the [LICENSE](http://www.gnu.org/licenses/) file for details.

## Author

- **Name:** Hector Ivan Valencia Muñoz

## Requirements

This script run over Robocorp an this provides an extension for Visual Studio Code. See [How to](https://robocorp.com/docs/visual-studio-code).

## Installation

1. **Clone the repository
2. **Run over Robocorp extension for Visual Studio Code

## Usage

1. Prepare the input CSV files:

* nid_validar.csv: A CSV file containing the NIT to be validated. Ensure it has the following columns:

  - nid
  - dv

* nid_validados.csv: A CSV file containing previously validated NIT with the following columns:

  - nid, dv, apl1, apl2, nom1, nom2, raz, estado

2. Run the script

3. Output files:

  - nid_validar_result.csv: A CSV file with the validation results for the NIT.
  - nid_validados.csv: Updated CSV file with newly validated NIT.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Acknowledgements

Special thanks to the Robocorp team for their excellent tools and documentation.