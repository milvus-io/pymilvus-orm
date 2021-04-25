
unittest:
	PYTHONPATH=`pwd` pytest --cov=pymilvus_orm tests -x -rxXs

codecov:
	PYTHONPATH=`pwd` pytest --cov=pymilvus_orm --cov-report=xml tests -x -rxXs

example:
	PYTHONPATH=`pwd` python examples/example.py
