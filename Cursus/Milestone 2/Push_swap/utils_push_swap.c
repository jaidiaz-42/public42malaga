/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils_push_swap.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/26 13:25:02 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/01/26 13:25:03 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack *stack)
{
	while (stack->next != NULL)
	{
		if (stack->value > stack->next->value)
			return (0);
		stack = stack->next;
	}
	return (1);
}

int	ft_check_arg_dup(t_stack *stack_a)
{
	t_stack	*tmp;
	t_stack	*current;

	current = stack_a;
	while (current)
	{
		tmp = current->next;
		while (tmp)
		{
			if (current->value == tmp->value)
				return (1);
			tmp = tmp->next;
		}
		current = current->next;
	}
	return (0);
}

int	ft_atoi_ps(const char *str, t_stack **stack_a)
{
	long	atoi;
	int		sign;

	atoi = 0;
	sign = 1;
	while ((*str >= 9 && *str <= 13) || *str == 32)
		str++;
	if (*str == '-' || *str == '+')
	{
		if (*str == '-')
			sign = -1;
		str++;
	}
	while (ft_isdigit(*str))
	{
		atoi *= 10;
		atoi += *str - 48;
		str++;
	}
	if (ft_isalpha(*str))
		ft_error(stack_a, NULL);
	if ((atoi * sign) > 2147483647 || (atoi * sign) < -2147483648)
		ft_error(stack_a, NULL);
	return (atoi * sign);
}

void	free_stack(t_stack **stack)
{
	t_stack	*tmp;
	t_stack	*current;

	if (!stack || !*stack)
		return ;
	current = *stack;
	while (current)
	{
		tmp = current->next;
		free(current);
		current = tmp;
	}
	*stack = NULL;
}

void	ft_error(t_stack **stack_a, t_stack **stack_b)
{
	free_stack(stack_a);
	free_stack(stack_b);
	write(2, "Error\n", 6);
	exit(1);
}
