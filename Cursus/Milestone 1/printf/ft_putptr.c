/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putptr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 15:05:44 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/12/02 13:09:59 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	ft_puthex_ulong(unsigned long n, int uppercase)
{
	char	*hex;
	int		count;
	char	c;

	count = 0;
	if (uppercase)
		hex = "0123456789ABCDEF";
	else
		hex = "0123456789abcdef";
	if (n >= 16)
		count += ft_puthex_ulong(n / 16, uppercase);
	c = hex[n % 16];
	count += write(1, &c, 1);
	return (count);
}

int	ft_putptr(void *ptr)
{
	unsigned long	addr;
	int				count;

	if (!ptr)
		return (ft_putstr("(nil)"));
	addr = (unsigned long)ptr;
	count = ft_putstr("0x");
	count += ft_puthex_ulong(addr, 0);
	return (count);
}
