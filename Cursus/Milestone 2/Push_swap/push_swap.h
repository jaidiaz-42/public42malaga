/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/28 18:07:20 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/02/03 12:51:44 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <unistd.h>
# include <limits.h>

typedef struct s_stack
{
	int				value;
	int				index;
	struct s_stack	*prev;
	struct s_stack	*next;
	struct s_stack	*target_node;
}	t_stack;

void	pa(t_stack **a, t_stack **b);
void	pb(t_stack **a, t_stack **b);
void	sa(t_stack **a);
void	sb(t_stack **b);
void	ss(t_stack **a, t_stack **b);
void	ra(t_stack **a);
void	rb(t_stack **b);
void	rr(t_stack **a, t_stack **b);
void	rra(t_stack **a);
void	rrb(t_stack **b);
void	rrr(t_stack **a, t_stack **b);

void	sort_three(t_stack **stack_a);
void	sort_five(t_stack **stack_a, t_stack **stack_b);
void	radix_sort(t_stack **stack_a, t_stack **stack_b);

char	*join_args(int argc, char **argv);
int		check_illegal_chars(char *str);
void	fill_stack_a(t_stack **a, char **nums);
void	ft_free_matrix(char **matrix);
t_stack	*get_next_min(t_stack *stack);
int		is_sorted(t_stack *stack);
int		ft_check_arg_dup(t_stack *stack_a);
int		ft_atoi_ps(const char *str, t_stack **stack_a);
void	free_stack(t_stack **stack);
void	ft_error(t_stack **stack_a, t_stack **stack_b);

t_stack	*stack_new_node(int value);
void	stack_add_back(t_stack **stack, t_stack *new);
int		stack_size(t_stack *stack);
t_stack	*stack_last(t_stack *stack);
void	index_stack(t_stack *stack);

size_t	ft_strlen(const char *s);
char	*ft_strdup(const char *s1);
char	*ft_strjoin(char const *s1, char const *s2);
char	**ft_split(char const *s, char c);
int		ft_isdigit(int c);
int		ft_isalpha(int c);

#endif
