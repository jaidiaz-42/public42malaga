/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 12:13:46 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	force_stop_and_clean(t_data *data)
{
	pthread_mutex_lock(&data->stop_mutex);
	data->stop_simulation = 1;
	pthread_mutex_unlock(&data->stop_mutex);
	join_and_clean(data);
	return (1);
}

int	abort_simulation(t_data *data)
{
	return (force_stop_and_clean(data));
}

static int	launch(t_data *data, char **argv)
{
	if (init_args(data, argv))
	{
		printf("Error: Invalid argument values or scheduler.\n");
		return (1);
	}
	if (init_sim_data(data))
	{
		free_all_data(data);
		return (1);
	}
	if (start_simulation(data))
		return (abort_simulation(data));
	join_and_clean(data);
	return (0);
}

int	main(int argc, char **argv)
{
	t_data	d;

	if (argc != 9)
	{
		printf("Error: Invalid arguments.\n");
		return (1);
	}
	return (launch(&d, argv));
}
