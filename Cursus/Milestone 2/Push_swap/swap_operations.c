/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   swap_operations.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 20:24:32 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 20:24:32 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sa(t_stack **a)
{
	t_stack	*first;
	t_stack	*second;

	if (!*a || !(*a)->next)
		return ;
	first = *a;
	second = first->next;
	first->next = second->next;
	if (second->next)
		second->next->prev = first;
	second->next = first;
	second->prev = NULL;
	first->prev = second;
	*a = second;
	write(1, "sa\n", 3);
}

void	sb(t_stack **b)
{
	t_stack	*first;
	t_stack	*second;

	if (!*b || !(*b)->next)
		return ;
	first = *b;
	second = first->next;
	first->next = second->next;
	if (second->next)
		second->next->prev = first;
	second->next = first;
	second->prev = NULL;
	first->prev = second;
	*b = second;
	write(1, "sb\n", 3);
}

void	ss(t_stack **a, t_stack **b)
{
	t_stack	*tmp;

	if (a && *a && (*a)->next)
	{
		tmp = *a;
		*a = (*a)->next;
		tmp->next = (*a)->next;
		if (tmp->next)
			tmp->next->prev = tmp;
		(*a)->next = tmp;
		(*a)->prev = NULL;
		tmp->prev = *a;
	}
	if (b && *b && (*b)->next)
	{
		tmp = *b;
		*b = (*b)->next;
		tmp->next = (*b)->next;
		if (tmp->next)
			tmp->next->prev = tmp;
		(*b)->next = tmp;
		(*b)->prev = NULL;
		tmp->prev = *b;
	}
	write(1, "ss\n", 3);
}
