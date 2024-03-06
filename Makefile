.PHONY: tests
PORT=8000

up:
	uvicorn app:app --reload --port $(PORT)

tests:
	pytest -s ./tests