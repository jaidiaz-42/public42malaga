/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 15:05:17 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/12/01 14:53:12 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex(unsigned int n, int uppercase)
{
	char			c;
	int				char_count;
	char			*hex;

	char_count = 0;
	if (uppercase)
		hex = "0123456789ABCDEF";
	else
		hex = "0123456789abcdef";
	if (n >= 16)
		char_count += ft_puthex(n / 16, uppercase);
	c = hex[n % 16];
	char_count += write(1, &c, 1);
	return (char_count);
}
