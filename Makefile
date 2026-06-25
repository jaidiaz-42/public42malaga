.DEFAULT_GOAL := help
MSG ?= Actualizacion automatica

.PHONY: clean gitup justgit help

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

gitup: 
	make clean
	git add .
	git commit -m "$(MSG)"
	git push

justgit: 
	git add .
	git commit -m "$(MSG)"
	git push

help:
	@echo "Uso: make [target]"
	@echo "  clean     : Limpiar caches"
	@echo "  gitup     : Actualizar y subir cambios"
	@echo "  justgit   : Subir cambios sin limpiar"
	@echo "  help      : Mostrar esta ayuda"