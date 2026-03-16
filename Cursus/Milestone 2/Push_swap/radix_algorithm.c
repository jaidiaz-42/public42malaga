/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   radix_algorithm.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 20:03:33 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 20:03:33 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	radix_sort(t_stack **stack_a, t_stack **stack_b)
{
	int	current_bit;
	int	i;
	int	size;
	int	max_bits;

	size = stack_size(*stack_a);
	max_bits = 0;
	while (((size - 1) >> max_bits) != 0)
		max_bits++;
	current_bit = 0;
	while (current_bit < max_bits)
	{
		i = 0;
		while (i++ < size)
		{
			if ((((*stack_a)->index >> current_bit) & 1) == 1)
				ra(stack_a);
			else
				pb(stack_a, stack_b);
		}
		while (stack_size(*stack_b) > 0)
			pa(stack_a, stack_b);
		current_bit++;
	}
}
