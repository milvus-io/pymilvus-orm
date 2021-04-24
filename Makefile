
unittest:
	PYTHONPATH=`pwd` pytest --cov=pymilvus_orm --cov-report=xml tests -x -rxXs

