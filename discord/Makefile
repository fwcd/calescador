include .env
export

.PHONY: all
all: run

.PHONY: installdeps
installdeps: requirements.txt
	pip3 install -r requirements.txt

.PHONY: run
run:
	python3 -m calescador_discord
