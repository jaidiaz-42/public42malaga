/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/08 18:01:23 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/01/19 10:48:13 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

void	clean_memory(char **ptr)
{
	if (ptr && *ptr)
	{
		free(*ptr);
		*ptr = NULL;
	}
}

static char	*ft_read(int fd, char *storage)
{
	ssize_t	bytes_read;
	char	*buffer;
	char	*tmp;

	buffer = malloc((BUFFER_SIZE + 1) * sizeof(char));
	if (!buffer)
		return (clean_memory(&storage), NULL);
	if (!storage)
		storage = ft_calloc(1, 1);
	bytes_read = 1;
	while (!ft_strchr(storage, '\n') && bytes_read > 0)
	{
		bytes_read = read(fd, buffer, BUFFER_SIZE);
		if (bytes_read < 0)
			return (free(buffer), clean_memory(&storage), NULL);
		buffer[bytes_read] = '\0';
		tmp = storage;
		storage = ft_strjoin(tmp, buffer);
		free(tmp);
	}
	free(buffer);
	return (storage);
}

char	*ft_update_storage(char *storage)
{
	char	*new_storage;
	int		i;
	int		j;

	i = 0;
	while (storage[i] && storage[i] != '\n')
		i++;
	if (!storage[i])
	{
		free(storage);
		return (NULL);
	}
	new_storage = ft_calloc(ft_strlen(storage) - i + 1, sizeof(char));
	if (!new_storage)
		return (clean_memory(&storage), NULL);
	i++;
	j = 0;
	while (storage[i])
		new_storage[j++] = storage[i++];
	free(storage);
	return (new_storage);
}

char	*ft_get_line(char *storage)
{
	int		i;
	char	*line;

	i = 0;
	if (!storage || !storage[i])
		return (NULL);
	while (storage[i] && storage[i] != '\n')
		i++;
	line = malloc(i + (storage[i] == '\n') + 1);
	if (!line)
		return (NULL);
	i = 0;
	while (storage[i] != '\0' && storage[i] != '\n')
	{
		line[i] = storage[i];
		i++;
	}
	if (storage[i] == '\n')
		line[i++] = '\n';
	line[i] = '\0';
	return (line);
}

char	*get_next_line(int fd)
{
	static char	*storage;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (clean_memory(&storage), NULL);
	storage = ft_read(fd, storage);
	if (!storage)
		return (NULL);
	line = ft_get_line(storage);
	if (!line)
		return (clean_memory(&storage), NULL);
	storage = ft_update_storage(storage);
	return (line);
}
