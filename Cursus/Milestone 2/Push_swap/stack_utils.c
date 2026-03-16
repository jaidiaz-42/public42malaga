/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/30 21:14:06 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 12:48:15 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*stack_new_node(int value)
{
	t_stack	*new;

	new = malloc(sizeof(t_stack));
	if (!new)
		return (NULL);
	new->value = value;
	new->index = -1;
	new->next = NULL;
	new->prev = NULL;
	new->target_node = NULL;
	return (new);
}

void	stack_add_back(t_stack **stack, t_stack *new)
{
	t_stack	*last;

	if (!stack || !new)
		return ;
	if (!*stack)
	{
		*stack = new;
		return ;
	}
	last = *stack;
	while (last->next)
		last = last->next;
	last->next = new;
	new->prev = last;
}

int	stack_size(t_stack *stack)
{
	int		size;
	t_stack	*current;

	size = 0;
	current = stack;
	while (current)
	{
		size++;
		current = current->next;
	}
	return (size);
}

t_stack	*stack_last(t_stack *stack)
{
	t_stack	*current;

	if (!stack)
		return (NULL);
	current = stack;
	while (current->next)
		current = current->next;
	return (current);
}

void	index_stack(t_stack *stack)
{
	t_stack	*next;
	int		index;
	int		size;

	index = 0;
	size = stack_size(stack);
	while (index < size)
	{
		next = get_next_min(stack);
		if (next)
			next->index = index++;
	}
}
