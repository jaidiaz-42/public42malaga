/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongles.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 10:57:17 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	sorted_indexes(int l, int r, int *lo, int *hi)
{
	if (l < r)
	{
		*lo = l;
		*hi = r;
	}
	else
	{
		*lo = r;
		*hi = l;
	}
}

void	lock_dongles(t_data *d, int l, int r)
{
	int	lo;
	int	hi;

	sorted_indexes(l, r, &lo, &hi);
	pthread_mutex_lock(&d->dongle_mutex[lo]);
	pthread_mutex_lock(&d->dongle_mutex[hi]);
}

void	unlock_dongles(t_data *d, int l, int r)
{
	int	lo;
	int	hi;

	sorted_indexes(l, r, &lo, &hi);
	pthread_mutex_unlock(&d->dongle_mutex[hi]);
	pthread_mutex_unlock(&d->dongle_mutex[lo]);
}

void	drop_dongles(t_coder *coder)
{
	t_data		*d;
	int			nl;
	int			nr;
	long long	ready_at;

	d = coder->data;
	nl = coder->id - 1;
	nr = coder->id % d->nb_coders;
	unlock_dongles(d, nl, nr);
	pthread_mutex_lock(&d->arbiter_mutex);
	coder->compiles_count++;
	ready_at = get_time_ms() + d->dongle_cooldown;
	d->dongle_state[nl] = 0;
	d->dongle_state[nr] = 0;
	d->dongle_ready_time[nl] = ready_at;
	d->dongle_ready_time[nr] = ready_at;
	pthread_cond_broadcast(&d->arbiter_cond);
	pthread_mutex_unlock(&d->arbiter_mutex);
}
