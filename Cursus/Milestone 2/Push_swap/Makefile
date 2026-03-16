NAME        = push_swap
CC          = cc
CFLAGS      = -Wall -Wextra -Werror
RM          = rm -f

# Lista de archivos fuente basada en lo que me has pasado
SRC         = push_swap.c \
              radix_algorithm.c \
              sorting.c \
              stack_utils.c \
              parsing_utils.c \
              libft_functions.c \
              libft_strings.c \
              push_operations.c \
              swap_operations.c \
              rotate_operations.c \
              reverse_operations.c \
              utils_push_swap.c

# Transformación de .c a .o
OBJ         = $(SRC:.c=.o)

# Regla principal
all: $(NAME)

# Compilación del ejecutable
$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

# Compilación de objetos individuales
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Limpieza de objetos
clean:
	$(RM) $(OBJ)

# Limpieza total
fclean: clean
	$(RM) $(NAME)

# Re-compilación total
re: fclean all

# Declaración de reglas que no son archivos
.PHONY: all clean fclean re