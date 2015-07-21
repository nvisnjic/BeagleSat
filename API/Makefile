# project name (generate executable with this name)
TARGET   = beaglesat_sensor

CC       = gcc
# compiling flags here
CFLAGS   = -std=c99 -Wall -I.

LINKER   = gcc -o
# linking flags here
LFLAGS   = -Wall -I. -lm

# change these to set the proper directories where each files should be
SRCDIR   = ./src
OBJDIR   = ./obj
BINDIR   = ./bin
DOCDIR   = ./docs


SOURCES  := $(wildcard $(SRCDIR)/*.c)
INCLUDES := $(wildcard $(SRCDIR)/*.h)
OBJECTS  := $(SOURCES:$(SRCDIR)/%.c=$(OBJDIR)/%.o)
rm       = rm -f

SRCS =  $(OBJECTS:.o=.c)

$(BINDIR)/$(TARGET): $(OBJECTS)
	@$(LINKER) $@ $(LFLAGS) $(OBJECTS)
	@echo "Linking complete!"

$(OBJECTS): $(OBJDIR)/%.o : $(SRCDIR)/%.c
	@$(CC) $(CFLAGS) -c $< -o $@
	@echo "Compiled "$<" successfully!"

.PHONEY: clean
clean:
	@$(rm) $(OBJECTS)
	@echo "Cleanup complete!"

.PHONEY: remove
remove: clean
	@$(rm) $(BINDIR)/$(TARGET)
	@echo "Executable removed!"


.PHONY: all clean distclean doxy

# If makefile changes, maybe the list of sources has changed, so update doxygens list
doxyfile.inc: Makefile
		echo INPUT         =  $(SRCDIR) $(SRCDIR)/*.h> ./docs/doxyfile.inc
		echo FILE_PATTERNS =  *.h $(SRCS) >> ./docs/doxyfile.inc
		echo OUTPUT_DIRECTORY = $(DOCDIR) >> ./docs/doxyfile.inc

doxy: doxyfile.inc $(SRCS) 
		doxygen ./docs/doxyfile.mk
