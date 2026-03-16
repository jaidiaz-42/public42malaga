/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/11 15:14:25 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/11/11 16:04:54 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t des_size)
{
	size_t	des_len;
	size_t	src_len;

	des_len = ft_strlen(dst);
	src_len = ft_strlen(src);
	if (des_len >= des_size)
		des_len = des_size;
	if (des_len == des_size)
		return (des_size + src_len);
	if (src_len < des_size - des_len)
		ft_memcpy(dst + des_len, src, src_len +1);
	else
	{
		ft_memcpy(dst + des_len, src, des_size - des_len - 1);
		dst[des_size - 1] = '\0';
	}
	return (des_len + src_len);
}
