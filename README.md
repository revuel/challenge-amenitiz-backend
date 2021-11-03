# Challenge [amenitiz.io](https://www.amenitiz.io/)

---

## Requirements
- python 3.7.z
- pip
- virtualenv

## Project Structure
- src
  - application (_Business Logic Layer_)
  - domain (_Domain Layer_)
  - infrastructure (_Infrastructure Layer_)
  - presentation (_Presentation Layer_)
- tests
  - unit
    - application
    - domain
    - infrastructure
    - presentation

### Details
- App has been organised this way in an attempt to reflect Hexagonal Architecture in the code base
- The Domain Layer has been implemented with SQL Alchemy declarative Base style
- The Infrastructure layer SQL Alchemy along its ORM has been chosen
- The Presentation layer has been implemented using FastAPI
- The Business Logic Layer consists in a set of services where each method is executed in a transactional fashion (see Transaction class)

**The heart of the challenge can be found at RuleEngine class**

The idea behind this approach is to keep each layer as much as isolated as possible.

## Run

### Create a virtual environment
[Just follow virtualenv documentation](https://virtualenv.pypa.io/en/latest/installation.html#installation)

### Install requirements
1. Enable virtualenv
```
# From project's root directory (assuming virtualenv was named 'venv')
source venv/bin/activate
```
2. 
```
# From project's root directory
pip install -r requirements.txt
```

### Launch app

```
# From project's root directory
python -m src.main
```
