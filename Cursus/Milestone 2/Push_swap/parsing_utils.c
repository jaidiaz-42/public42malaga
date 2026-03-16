/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parsing_utils.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/03 21:09:45 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 21:09:45 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

char	*join_args(int argc, char **argv)
{
	char	*tmp;
	char	*str_general;
	int		i;

	i = 1;
	str_general = ft_strdup("");
	if (!str_general)
		return (NULL);
	while (i < argc)
	{
		tmp = str_general;
		str_general = ft_strjoin(tmp, argv[i]);
		free(tmp);
		tmp = str_general;
		str_general = ft_strjoin(tmp, " ");
		free(tmp);
		i++;
	}
	return (str_general);
}

int	check_illegal_chars(char *str)
{
	int	i;

	i = 0;
	while (str[i])
	{
		if (!((str[i] >= '0' && str[i] <= '9') || str[i] == ' '
				|| str[i] == '-' || str[i] == '+'
				|| (str[i] >= 9 && str[i] <= 13)))
			return (1);
		if ((str[i] == '-' || str[i] == '+')
			&& !(str[i + 1] >= '0' && str[i + 1] <= '9'))
			return (1);
		i++;
	}
	return (0);
}

void	fill_stack_a(t_stack **a, char **nums)
{
	int		i;
	long	val;

	i = 0;
	while (nums[i])
	{
		val = ft_atoi_ps(nums[i], a);
		stack_add_back(a, stack_new_node((int)val));
		i++;
	}
}

void	ft_free_matrix(char **matrix)
{
	int	i;

	i = 0;
	if (!matrix)
		return ;
	while (matrix[i])
	{
		free(matrix[i]);
		i++;
	}
	free(matrix);
}

t_stack	*get_next_min(t_stack *stack)
{
	t_stack	*min;
	int		has_min;

	min = NULL;
	has_min = 0;
	while (stack)
	{
		if (stack->index == -1 && (!has_min || stack->value < min->value))
		{
			min = stack;
			has_min = 1;
		}
		stack = stack->next;
	}
	return (min);
}
