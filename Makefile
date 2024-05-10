install-requirements:
	pip install -r requirements.txt

build_and_run:
	docker build -t my_first_llm . && docker run --rm -it my_first_llm

run:
	python main.py
