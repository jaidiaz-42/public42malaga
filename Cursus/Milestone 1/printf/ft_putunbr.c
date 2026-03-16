/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunbr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 14:59:22 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/11/27 15:04:10 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunbr(unsigned int nb)
{
	unsigned int	num;
	int				count;

	count = 0;
	num = nb;
	if (num >= 10)
		count += ft_putunbr(num / 10);
	count += ft_putchar((num % 10) + '0');
	return (count);
}
