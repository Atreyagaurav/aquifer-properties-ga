CC = gcc
CFLAGS = -Wall -lm
DEPS = model.h
OBJ = model.o genetic.o

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c -o $@ $<

genes: genetic.o model.o
	gcc $(CFLAGS) -o $@ $^

model: model.o
	gcc $(CFLAGS) -o $@ $^
