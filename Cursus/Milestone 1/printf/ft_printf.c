/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/27 12:41:56 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/12/01 10:55:29 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	format_handler(const char format, va_list vargs)
{
	int	char_count;

	char_count = 0;
	if (format == 'c')
		char_count += ft_putchar(va_arg(vargs, int));
	else if (format == 's')
		char_count += ft_putstr(va_arg(vargs, char *));
	else if (format == 'd' || format == 'i')
		char_count += ft_putnbr(va_arg(vargs, int));
	else if (format == 'u')
		char_count += ft_putunbr(va_arg(vargs, unsigned int));
	else if (format == 'X')
		char_count += ft_puthex(va_arg(vargs, unsigned int), 1);
	else if (format == 'x')
		char_count += ft_puthex(va_arg(vargs, unsigned int), 0);
	else if (format == 'p')
		char_count += ft_putptr(va_arg(vargs, void *));
	else if (format == '%')
		char_count += ft_putchar('%');
	return (char_count);
}

int	ft_printf(const char *str, ...)
{
	va_list	vargs;
	int		char_count;
	int		pos;

	va_start(vargs, str);
	char_count = 0;
	pos = 0;
	while (str[pos])
	{
		if (str[pos] != '%')
		{
			write(1, &str[pos], 1);
			char_count++;
		}
		else if (str[pos + 1] != '\0')
		{
			char_count += format_handler(str[pos + 1], vargs);
			pos++;
		}
		pos++;
	}
	va_end(vargs);
	return (char_count);
}
