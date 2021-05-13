
unittest:
	PYTHONPATH=`pwd` pytest --cov=pymilvus_orm tests -x -rxXs

lint:
	PYTHONPATH=`pwd` pylint --rcfile=pylint.conf pymilvus_orm

codecov:
	PYTHONPATH=`pwd` pytest --cov=pymilvus_orm --cov-report=xml tests -x -rxXs

example:
	PYTHONPATH=`pwd` python examples/example.py

example_index:
	PYTHONPATH=`pwd` python examples/example_index.py
