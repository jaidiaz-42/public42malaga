NAME		= codexion

CC			= cc
CFLAGS		= -Wall -Wextra -Werror -pthread

SRCS		= main.c \
			  init.c \
			  utils.c \
			  heap.c \
			  dongles.c \
			  arbiter.c \
			  routine.c \
			  monitor.c \
			  clean.c

OBJS		= $(SRCS:.c=.o)

%.o: %.c codexion.h
	$(CC) $(CFLAGS) -c $< -o $@

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

all: $(NAME)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

test1:
	./$(NAME) 5 800 200 200 200 3 10 fifo

test2:
	./$(NAME) 5 800 200 200 200 3 10 edf

.PHONY: all clean fclean re test1 test2