# Makefile for Enhanced Inflationary Domain Theory (IDT) with Hidden Regions

# Compiler and flags
CC = gcc
CCFLAG = -g -Wall -Wextra -std=c99
LDFLAG = -lm

# Directories
INCDIR = include
SRCDIR = src
OBJDIR = build
BINDIR = bin

# Source files
HIDDEN_REGIONS_SRC = $(SRCDIR)/hidden_regions/hidden_regions.c
BACKGROUND_SRC = $(SRCDIR)/background/background_w_fld_with_hidden_regions.c
INPUT_SRC = $(SRCDIR)/input/input_hidden_regions.c
MAIN_SRC = $(SRCDIR)/main.c

# Object files
HIDDEN_REGIONS_OBJ = $(OBJDIR)/hidden_regions.o
BACKGROUND_OBJ = $(OBJDIR)/background_w_fld_with_hidden_regions.o
INPUT_OBJ = $(OBJDIR)/input_hidden_regions.o
MAIN_OBJ = $(OBJDIR)/main.o

# Include paths
INCLUDES = -I$(INCDIR)

# Target executable
TARGET = $(BINDIR)/idt_class

# Default target
all: directories $(TARGET)

# Create necessary directories
directories:
	mkdir -p $(OBJDIR)
	mkdir -p $(BINDIR)

# Compile hidden regions module
$(HIDDEN_REGIONS_OBJ): $(HIDDEN_REGIONS_SRC)
	$(CC) $(CCFLAG) $(INCLUDES) -c $< -o $@

# Compile background module
$(BACKGROUND_OBJ): $(BACKGROUND_SRC)
	$(CC) $(CCFLAG) $(INCLUDES) -c $< -o $@

# Compile input module
$(INPUT_OBJ): $(INPUT_SRC)
	$(CC) $(CCFLAG) $(INCLUDES) -c $< -o $@

# Compile main program
$(MAIN_OBJ): $(MAIN_SRC)
	$(CC) $(CCFLAG) $(INCLUDES) -c $< -o $@

# Link all object files
$(TARGET): $(HIDDEN_REGIONS_OBJ) $(BACKGROUND_OBJ) $(INPUT_OBJ) $(MAIN_OBJ)
	$(CC) $(CCFLAG) $^ -o $@ $(LDFLAG)

# Clean build files
clean:
	rm -rf $(OBJDIR)
	rm -rf $(BINDIR)

# Run the enhanced model
run_enhanced:
	$(TARGET) config/enhanced_model.ini

# Run the LCDM model
run_lcdm:
	$(TARGET) config/lcdm_model.ini

# Compare the results
compare: run_enhanced run_lcdm
	python tools/compare_results.py

.PHONY: all directories clean run_enhanced run_lcdm compare
