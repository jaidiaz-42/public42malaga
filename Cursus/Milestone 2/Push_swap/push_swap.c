/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/26 13:24:57 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/09 12:29:24 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push_swap(t_stack **a, t_stack **b)
{
	int	size;

	size = stack_size(*a);
	if (size == 2)
		sa(a);
	else if (size == 3)
		sort_three(a);
	else if (size <= 5)
		sort_five(a, b);
	else
		radix_sort(a, b);
}

static void	process_input(int argc, char **argv, t_stack **a)
{
	char	*str_gen;
	char	**nums;

	str_gen = join_args(argc, argv);
	if (!str_gen)
		exit(1);
	if (check_illegal_chars(str_gen))
	{
		free(str_gen);
		write(2, "Error\n", 6);
		exit(1);
	}
	nums = ft_split(str_gen, ' ');
	free(str_gen);
	if (!nums)
		exit(1);
	fill_stack_a(a, nums);
	ft_free_matrix(nums);
}

int	main(int argc, char **argv)
{
	t_stack	*a;
	t_stack	*b;

	a = NULL;
	b = NULL;
	if (argc < 2)
		return (0);
	process_input(argc, argv, &a);
	if (!a)
		ft_error(&a, &b);
	if (ft_check_arg_dup(a))
		ft_error(&a, &b);
	index_stack(a);
	if (!is_sorted(a))
		push_swap(&a, &b);
	free_stack(&a);
	free_stack(&b);
	return (0);
}
