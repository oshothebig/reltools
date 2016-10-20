RM=rm -f
RMFORCE=rm -rf
SRCS= genGoStructRst.go
all: exe

exe: $(SRCS)
	go build $(SRCS)

clean:
	$(RM) genGoStructRst rstFiles/*.rst
