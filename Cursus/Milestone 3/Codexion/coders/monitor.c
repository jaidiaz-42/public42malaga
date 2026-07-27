/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 12:06:52 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	check_all_compiled(t_data *data)
{
	int	i;
	int	reached;

	pthread_mutex_lock(&data->arbiter_mutex);
	i = 0;
	reached = 1;
	while (i < data->nb_coders)
	{
		if (data->coders[i].compiles_count < data->nb_compiles_required)
		{
			reached = 0;
			break ;
		}
		i++;
	}
	pthread_mutex_unlock(&data->arbiter_mutex);
	return (reached);
}

static int	activate_stop(t_data *data)
{
	int	already_stopped;

	pthread_mutex_lock(&data->stop_mutex);
	already_stopped = data->stop_simulation;
	data->stop_simulation = 1;
	pthread_mutex_unlock(&data->stop_mutex);
	pthread_mutex_lock(&data->arbiter_mutex);
	pthread_cond_broadcast(&data->arbiter_cond);
	pthread_mutex_unlock(&data->arbiter_mutex);
	return (!already_stopped);
}

static int	coder_burned_out(t_data *data, t_coder *c, long long now)
{
	int	burned;

	pthread_mutex_lock(&data->arbiter_mutex);
	burned = (c->compiles_count < data->nb_compiles_required
			&& now - c->last_compile_start >= data->time_to_burnout);
	pthread_mutex_unlock(&data->arbiter_mutex);
	return (burned);
}

static int	detect_burnout(t_data *data)
{
	int			i;
	long long	now;

	i = 0;
	while (i < data->nb_coders)
	{
		now = get_time_ms();
		if (coder_burned_out(data, &data->coders[i], now))
		{
			if (activate_stop(data))
			{
				pthread_mutex_lock(&data->write_mutex);
				printf("%lld %d burned out\n", now - data->start_time,
					data->coders[i].id);
				pthread_mutex_unlock(&data->write_mutex);
			}
			return (1);
		}
		i++;
	}
	return (0);
}

void	*monitor_routine(void *arg)
{
	t_data	*data;
	int		finished;

	data = (t_data *)arg;
	while (!check_stop(data))
	{
		finished = detect_burnout(data);
		if (!finished && check_all_compiled(data))
		{
			activate_stop(data);
			finished = 1;
		}
		if (finished)
			break ;
		usleep(500);
	}
	return (NULL);
}
