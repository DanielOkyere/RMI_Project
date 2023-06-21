#! /usr/bin/env python3
"""this code runs the examples"""

import Pyro4
import sys
import Pyro4.util
from person import Person

sys.excepthook = Pyro4.util.excepthook



warehouse = Pyro4.Proxy("PYRONAME:example.warehouse")

janet = Person("Janet")
henry = Person("Henry")

janet.visit(warehouse)
henry.visit(warehouse)