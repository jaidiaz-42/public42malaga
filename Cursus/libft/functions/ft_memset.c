/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/10 21:14:01 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/11/10 21:14:01 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *str, int c, size_t size)
{
	size_t	i;
	char	*temp;

	i = 0;
	temp = (char *)str;
	while (i < size)
	{
		temp[i] = c;
		i++;
	}
	return (str);
}
