/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   clean.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 12:13:18 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	destroy_dongle_mutexes(t_data *data)
{
	int	i;

	if (!data->dongle_mutex)
		return ;
	i = 0;
	while (i < data->nb_coders)
	{
		pthread_mutex_destroy(&data->dongle_mutex[i]);
		i++;
	}
	free(data->dongle_mutex);
}

static void	free_arrays(t_data *data)
{
	if (data->dongle_state)
		free(data->dongle_state);
	if (data->dongle_ready_time)
		free(data->dongle_ready_time);
	if (data->coders)
		free(data->coders);
	if (data->request_heap.array)
		free(data->request_heap.array);
}

void	free_all_data(t_data *data)
{
	destroy_dongle_mutexes(data);
	pthread_mutex_destroy(&data->write_mutex);
	pthread_mutex_destroy(&data->stop_mutex);
	pthread_mutex_destroy(&data->arbiter_mutex);
	pthread_cond_destroy(&data->arbiter_cond);
	free_arrays(data);
}

static void	join_all_coders(t_data *data)
{
	int	i;

	i = 0;
	while (i < data->nb_coders)
	{
		if (data->coders[i].thread_id)
			pthread_join(data->coders[i].thread_id, NULL);
		i++;
	}
}

void	join_and_clean(t_data *data)
{
	join_all_coders(data);
	if (data->monitor_thread)
		pthread_join(data->monitor_thread, NULL);
	free_all_data(data);
}
