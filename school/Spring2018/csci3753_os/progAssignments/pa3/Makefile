obj=multi-lookup.o

multi-lookup: multi-lookup.o
	gcc -Wall -pthread -o multi-lookup $(obj)

multi-lookup.o: multi-lookup.c
	gcc -Wall -c multi-lookup.c
#
#thread.o: thread.c
#	gcc -Wall -c thread.c
#
.PHONY: clean
clean:
	rm -f $(obj)
