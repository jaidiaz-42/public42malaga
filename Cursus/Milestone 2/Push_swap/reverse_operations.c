/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   reverse_operations.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 20:25:21 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 20:25:21 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	rra(t_stack **a)
{
	t_stack	*last;
	t_stack	*second_last;

	if (!*a || !(*a)->next)
		return ;
	last = stack_last(*a);
	second_last = last->prev;
	if (second_last)
		second_last->next = NULL;
	last->prev = NULL;
	last->next = *a;
	(*a)->prev = last;
	*a = last;
	write(1, "rra\n", 4);
}

void	rrb(t_stack **b)
{
	t_stack	*last;
	t_stack	*second_last;

	if (!*b || !(*b)->next)
		return ;
	last = stack_last(*b);
	second_last = last->prev;
	if (second_last)
		second_last->next = NULL;
	last->prev = NULL;
	last->next = *b;
	(*b)->prev = last;
	*b = last;
	write(1, "rrb\n", 4);
}

void	rrr(t_stack **a, t_stack **b)
{
	t_stack	*last;

	if (a && *a && (*a)->next)
	{
		last = stack_last(*a);
		last->prev->next = NULL;
		last->next = *a;
		last->prev = NULL;
		(*a)->prev = last;
		*a = last;
	}
	if (b && *b && (*b)->next)
	{
		last = stack_last(*b);
		last->prev->next = NULL;
		last->next = *b;
		last->prev = NULL;
		(*b)->prev = last;
		*b = last;
	}
	write(1, "rrr\n", 4);
}
