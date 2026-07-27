/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 10:48:00 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	init_heap(t_heap *heap, int capacity)
{
	heap->array = (t_request *)malloc(sizeof(t_request) * capacity);
	if (!heap->array)
		return (1);
	heap->size = 0;
	heap->capacity = capacity;
	return (0);
}

static void	heapify_up(t_data *data, int i)
{
	int			parent;
	t_request	temp;
	t_heap		*h;

	h = &data->request_heap;
	while (i != 0)
	{
		parent = (i - 1) / 2;
		if (!is_higher_priority(h->array[i], h->array[parent]))
			break ;
		temp = h->array[i];
		h->array[i] = h->array[parent];
		h->array[parent] = temp;
		i = parent;
	}
}

static void	heapify_down(t_data *data, int i)
{
	int			s;
	int			l;
	int			r;
	t_request	t;
	t_request	*a;

	s = i;
	l = 2 * i + 1;
	r = 2 * i + 2;
	a = data->request_heap.array;
	if (l < data->request_heap.size && is_higher_priority(a[l], a[s]))
		s = l;
	if (r < data->request_heap.size && is_higher_priority(a[r], a[s]))
		s = r;
	if (s != i)
	{
		t = a[i];
		a[i] = a[s];
		a[s] = t;
		heapify_down(data, s);
	}
}

void	insert_heap(t_data *data, t_request req)
{
	int	i;

	i = data->request_heap.size;
	data->request_heap.array[i] = req;
	data->request_heap.size++;
	heapify_up(data, i);
}

void	extract_node(t_data *data, int coder_id)
{
	int		i;
	t_heap	*h;

	h = &data->request_heap;
	i = 0;
	while (i < h->size)
	{
		if (h->array[i].coder_id == coder_id)
			break ;
		i++;
	}
	if (i == h->size)
		return ;
	h->array[i] = h->array[h->size - 1];
	h->size--;
	if (i < h->size)
	{
		heapify_up(data, i);
		heapify_down(data, i);
	}
}
