/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_rev_params.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com>   +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/09/24 16:12:41 by jaidiaz-          #+#    #+#             */
/*   Updated: 2025/09/24 16:12:44 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>

void	ft_putchar(char c)
{
	write(1, &c, 1);
}

int	main(int argc, char **argv)
{
	int	i;
	int	j;
	int	len;

	i = 1;
	len = argc -1;
	while (i < argc)
	{
		j = 0;
		while (argv[len][j])
		{
			ft_putchar(argv[len][j]);
			j++;
		}
		ft_putchar('\n');
		i++;
		len--;
	}
	return (0);
}
