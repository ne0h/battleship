# PE4 - Battleship++

## Deployment

### Client

#### Dependencies

* Python 3
* PyQt5
* Sphinx with autodoc to build the documentation

#### Run

Navigate to `/client` and run `python3 main.py`.

#### Build documentation

Navigate to `/docs` and run:

1. `sphinx-apidoc -f -o . ..` to scan source files
1. `make html` to build html documentation
