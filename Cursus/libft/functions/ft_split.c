/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/13 11:07:46 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/11/14 18:47:43 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*free_all(char **str_to_free, int iterator)
{
	while (iterator >= 0)
	{
		free(str_to_free[iterator]);
		iterator--;
	}
	free(str_to_free);
	return (NULL);
}

int	count_words(const char *str, char delim_char)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (str[i])
	{
		while (str[i] && str[i] == delim_char)
			i++;
		if (str[i] && str[i] != delim_char)
		{
			count++;
			while (str[i] && str[i] != delim_char)
				i++;
		}
	}
	return (count);
}

int	word_len(const char *str, char delim_char, int i_pos)
{
	int	this_len;

	this_len = 0;
	while (str[i_pos + this_len] && str[i_pos + this_len] != delim_char)
		this_len++;
	return (this_len);
}

char	*get_word(const char *str, int start, int word_lenght)
{
	char	*this_word;
	int		i;

	i = 0;
	this_word = malloc(sizeof(char) * word_lenght + 1);
	if (!this_word)
		return (NULL);
	while (i < word_lenght)
	{
		this_word[i] = str[start + i];
		i++;
	}
	this_word[i] = '\0';
	return (this_word);
}

char	**ft_split(char const *s, char c)
{
	char	**new_str;
	int		i;
	int		j;

	i = 0;
	j = 0;
	new_str = malloc((sizeof(char *)) * (count_words(s, c) + 1));
	if (!new_str || !s)
		return (NULL);
	while (s[i])
	{
		while (s[i] == c && s[i])
			i++;
		if (word_len(s, c, i) > 0)
		{
			new_str[j] = get_word(s, i, word_len(s, c, i));
			if (!new_str[j])
				return (free_all(new_str, j));
			j++;
			i += word_len(s, c, i);
		}
	}
	new_str[j] = NULL;
	return (new_str);
}
