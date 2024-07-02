APP = sniff7
SOURCES = $(wildcard *.c)
OBJECTS = $(SOURCES:.c=.o)

$(APP): $(OBJECTS)
	$(CC) $(CFLAGS) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $(APP)

# Objects
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@
