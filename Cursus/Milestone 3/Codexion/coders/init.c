/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 11:03:22 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	parse_scheduler(const char *str, t_scheduler *sched)
{
	if (strcmp(str, "fifo") == 0)
		*sched = FIFO;
	else if (strcmp(str, "edf") == 0)
		*sched = EDF;
	else
		return (1);
	return (0);
}

static int	parse_numeric_args(t_data *data, char **argv)
{
	long long	values[7];
	int			error;
	int			i;

	error = 0;
	i = 0;
	while (i < 7)
	{
		values[i] = ft_atoll(argv[i + 1], &error);
		i++;
	}
	data->nb_coders = (int)values[0];
	data->time_to_burnout = values[1];
	data->time_to_compile = values[2];
	data->time_to_debug = values[3];
	data->time_to_refactor = values[4];
	data->nb_compiles_required = (int)values[5];
	data->dongle_cooldown = values[6];
	return (error);
}

int	init_args(t_data *data, char **argv)
{
	memset(data, 0, sizeof(t_data));
	if (parse_numeric_args(data, argv))
		return (1);
	if (data->nb_coders <= 0)
		return (1);
	if (parse_scheduler(argv[8], &data->scheduler))
		return (1);
	return (0);
}

int	init_sim_data(t_data *data)
{
	int	i;

	if (init_heap(&data->request_heap, data->nb_coders) != 0)
		return (1);
	data->dongle_state = malloc(sizeof(int) * data->nb_coders);
	data->dongle_ready_time = malloc(sizeof(long long) * data->nb_coders);
	data->dongle_mutex = malloc(sizeof(pthread_mutex_t) * data->nb_coders);
	data->coders = malloc(sizeof(t_coder) * data->nb_coders);
	if (!data->dongle_state || !data->dongle_ready_time
		|| !data->dongle_mutex || !data->coders)
		return (1);
	memset(data->dongle_state, 0, sizeof(int) * data->nb_coders);
	memset(data->dongle_ready_time, 0, sizeof(long long) * data->nb_coders);
	pthread_mutex_init(&data->write_mutex, NULL);
	pthread_mutex_init(&data->stop_mutex, NULL);
	pthread_mutex_init(&data->arbiter_mutex, NULL);
	pthread_cond_init(&data->arbiter_cond, NULL);
	i = 0;
	while (i < data->nb_coders)
	{
		pthread_mutex_init(&data->dongle_mutex[i], NULL);
		i++;
	}
	return (0);
}

int	start_simulation(t_data *data)
{
	int		i;
	t_coder	*c;

	data->start_time = get_time_ms();
	if (data->start_time == -1)
		return (1);
	i = 0;
	while (i < data->nb_coders)
	{
		c = &data->coders[i];
		c->id = i + 1;
		c->last_compile_start = data->start_time;
		c->compiles_count = 0;
		c->data = data;
		if (pthread_create(&c->thread_id, NULL, coder_routine, c) != 0)
			return (1);
		i++;
	}
	if (pthread_create(&data->monitor_thread, NULL, monitor_routine, data) != 0)
		return (1);
	return (0);
}
