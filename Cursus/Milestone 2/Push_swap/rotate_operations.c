/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rotate_operations.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 20:24:12 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 20:24:12 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ra(t_stack **a)
{
	t_stack	*first;
	t_stack	*last;

	if (!*a || !(*a)->next)
		return ;
	first = *a;
	*a = first->next;
	(*a)->prev = NULL;
	last = stack_last(*a);
	last->next = first;
	first->prev = last;
	first->next = NULL;
	write(1, "ra\n", 3);
}

void	rb(t_stack **b)
{
	t_stack	*first;
	t_stack	*last;

	if (!*b || !(*b)->next)
		return ;
	first = *b;
	*b = first->next;
	(*b)->prev = NULL;
	last = stack_last(*b);
	last->next = first;
	first->prev = last;
	first->next = NULL;
	write(1, "rb\n", 3);
}

void	rr(t_stack **a, t_stack **b)
{
	t_stack	*first;
	t_stack	*last;

	if (a && *a && (*a)->next)
	{
		first = *a;
		*a = first->next;
		(*a)->prev = NULL;
		last = stack_last(*a);
		last->next = first;
		first->prev = last;
		first->next = NULL;
	}
	if (b && *b && (*b)->next)
	{
		first = *b;
		*b = first->next;
		(*b)->prev = NULL;
		last = stack_last(*b);
		last->next = first;
		first->prev = last;
		first->next = NULL;
	}
	write(1, "rr\n", 3);
}
