/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   arbiter.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 11:55:32 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_request	register_request(t_coder *coder)
{
	t_request	req;
	t_data		*d;

	d = coder->data;
	req.coder_id = coder->id;
	if (d->scheduler == FIFO)
		req.priority = get_time_ms();
	else
		req.priority = coder->last_compile_start + d->time_to_burnout;
	insert_heap(d, req);
	return (req);
}

static int	rival_can_proceed(t_coder *coder, t_request *mine)
{
	t_data		*d;
	t_request	rival;
	int			nl;
	int			nr;
	int			i;

	d = coder->data;
	i = 0;
	while (i < d->request_heap.size)
	{
		rival = d->request_heap.array[i];
		i++;
		if (rival.coder_id == coder->id || !is_higher_priority(rival, *mine))
			continue ;
		nl = rival.coder_id - 1;
		nr = rival.coder_id % d->nb_coders;
		if (d->dongle_state[nl] || d->dongle_state[nr])
			continue ;
		if (get_time_ms() < d->dongle_ready_time[nl])
			continue ;
		if (get_time_ms() < d->dongle_ready_time[nr])
			continue ;
		return (1);
	}
	return (0);
}

static int	try_acquire(t_coder *coder, t_request *mine)
{
	t_data	*d;
	int		nl;
	int		nr;

	d = coder->data;
	if (rival_can_proceed(coder, mine))
		return (ATTEMPT_BLOCKED);
	nl = coder->id - 1;
	nr = coder->id % d->nb_coders;
	if (d->dongle_state[nl] || d->dongle_state[nr])
		return (ATTEMPT_BLOCKED);
	if (get_time_ms() < d->dongle_ready_time[nl]
		|| get_time_ms() < d->dongle_ready_time[nr])
		return (ATTEMPT_COOLDOWN);
	extract_node(d, coder->id);
	lock_dongles(d, nl, nr);
	d->dongle_state[nl] = 1;
	d->dongle_state[nr] = 1;
	return (ATTEMPT_SUCCESS);
}

static int	wait_for_turn(t_coder *coder, t_request *mine, t_data *d)
{
	int	state;

	state = ATTEMPT_BLOCKED;
	while (!check_stop(d) && state != ATTEMPT_SUCCESS)
	{
		state = try_acquire(coder, mine);
		if (state == ATTEMPT_COOLDOWN)
		{
			pthread_mutex_unlock(&d->arbiter_mutex);
			usleep(1000);
			pthread_mutex_lock(&d->arbiter_mutex);
		}
		else if (state == ATTEMPT_BLOCKED)
			pthread_cond_wait(&d->arbiter_cond, &d->arbiter_mutex);
	}
	return (state);
}

int	take_dongles(t_coder *coder)
{
	t_data		*d;
	t_request	mine;
	int			state;

	d = coder->data;
	pthread_mutex_lock(&d->arbiter_mutex);
	mine = register_request(coder);
	state = wait_for_turn(coder, &mine, d);
	if (state == ATTEMPT_SUCCESS)
	{
		coder->last_compile_start = get_time_ms();
		pthread_cond_broadcast(&d->arbiter_cond);
	}
	pthread_mutex_unlock(&d->arbiter_mutex);
	return (state == ATTEMPT_SUCCESS);
}
