# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/11/05 14:40:29 by jaidiaz-          #+#    #+#              #
#    Updated: 2025/11/05 14:40:29 by jaidiaz-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# 1. Configuración General
NAME = libft.a
SRC_DIR = srcs
INC_DIR = includes
SRC =	$(SRC_DIR)/ft_putchar.c $(SRC_DIR)/ft_putstr.c $(SRC_DIR)/ft_strcmp.c $(SRC_DIR)/ft_strlen.c $(SRC_DIR)/ft_swap.c
OBJ = $(SRC:.c=.o)
CC = cc
CFLAGS = -Wall -Wextra -Werror -g -I$(INC_DIR) 

# 2. Regla principal
all: $(NAME)

# 3. Crear la librería estática
$(NAME): $(OBJ)
	ar rcs $(NAME) $(OBJ)

# 4. Compilar cada archivo fuente
$(SRC_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

# 5. Limpiar archivos objeto
clean:
	rm -f $(OBJ)

# 6. Limpiar todo
fclean: clean
	rm -f $(NAME)

# 7. Recompilar todo
re: fclean all

# 8. Objetivos falsos
.PHONY: all clean fclean re
