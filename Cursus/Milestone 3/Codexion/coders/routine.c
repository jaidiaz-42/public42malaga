/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   routine.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 11:23:14 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	check_stop(t_data *data)
{
	int	stop;

	pthread_mutex_lock(&data->stop_mutex);
	stop = data->stop_simulation;
	pthread_mutex_unlock(&data->stop_mutex);
	return (stop);
}

void	print_action(t_coder *coder, char *action)
{
	long long	elapsed;

	pthread_mutex_lock(&coder->data->write_mutex);
	if (!check_stop(coder->data))
	{
		elapsed = get_time_ms() - coder->data->start_time;
		printf("%lld %d %s\n", elapsed, coder->id, action);
	}
	pthread_mutex_unlock(&coder->data->write_mutex);
}

static void	solo_coder_life(t_coder *coder)
{
	print_action(coder, "has taken a dongle");
	ft_usleep(coder->data->time_to_burnout + 10, coder->data);
}

static void	compile_debug_refactor(t_coder *coder)
{
	print_action(coder, "has taken a dongle");
	print_action(coder, "has taken a dongle");
	print_action(coder, "is compiling");
	ft_usleep(coder->data->time_to_compile, coder->data);
	drop_dongles(coder);
	print_action(coder, "is debugging");
	ft_usleep(coder->data->time_to_debug, coder->data);
	print_action(coder, "is refactoring");
	ft_usleep(coder->data->time_to_refactor, coder->data);
}

void	*coder_routine(void *arg)
{
	t_coder	*coder;
	int		done;

	coder = (t_coder *)arg;
	if (coder->data->nb_coders == 1)
	{
		solo_coder_life(coder);
		return (NULL);
	}
	while (!check_stop(coder->data))
	{
		pthread_mutex_lock(&coder->data->arbiter_mutex);
		done = (coder->compiles_count >= coder->data->nb_compiles_required);
		pthread_mutex_unlock(&coder->data->arbiter_mutex);
		if (done)
			break ;
		if (take_dongles(coder))
			compile_debug_refactor(coder);
	}
	return (NULL);
}
