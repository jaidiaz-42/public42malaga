/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/09 09:01:41 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/09/12 10:48:01 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

unsigned int	ft_strlen(const char *s)
{
	unsigned int	i;

	i = 0;
	while (s[i] != '\0')
	{
		i++;
	}
	return (i);
}

unsigned int	ft_strlcat(char *dest, char *src, unsigned int size)
{
	unsigned int	deslen;
	unsigned int	srclen;
	unsigned int	i;

	deslen = 0;
	srclen = ft_strlen(src);
	i = 0;
	while (deslen < size && dest[deslen] != '\0')
	{
		deslen++;
	}
	if (deslen == size)
	{
		return (size + srclen);
	}
	while (src[i] != '\0' && (deslen + i + 1) < size)
	{
		dest[deslen + i] = src[i];
		i++;
	}
	dest[deslen + i] = '\0';
	return (deslen + srclen);
}

int main(void)
{
    char    dest[50] = "Hola, ";
    char    src[] = "mundo!";
    unsigned int    size = sizeof(dest);
    unsigned int    result;

    printf("Antes de ft_strlcat:\n");
    printf("dest = \"%s\"\n", dest);
    printf("src  = \"%s\"\n", src);

    result = ft_strlcat(dest, src, size);

    printf("\nDespués de ft_strlcat:\n");
    printf("dest = \"%s\"\n", dest);
    printf("Longitud total que intentó crear: %u\n", result);

    // También probamos ft_strlen
    printf("\nPrueba de ft_strlen:\n");
    printf("Longitud de \"%s\" = %u\n", src, ft_strlen(src));

    return (0);
}
