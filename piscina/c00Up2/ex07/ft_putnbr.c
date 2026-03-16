/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/19 10:54:23 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/09/22 09:09:27 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write (1, &c, 1);
}

void	ft_putnbr(int nb)
{
	long int	numb;

	numb = nb;
	if (numb < 0)
	{
		write(1, "-", 1);
		numb = numb * (-1);
	}
	if (numb > 9)
	{
		ft_putnbr(numb / 10);
	}
	ft_putchar(numb % 10 + '0');
}
