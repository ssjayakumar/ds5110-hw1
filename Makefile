# Optional shortcut for macOS/Linux: `make` runs the whole pipeline.
# On Windows, use the command in the README instead.

.PHONY: all clean

all:
	python src/analysis.py

clean:
	rm -f output/*.csv output/*.png output/summary.txt
