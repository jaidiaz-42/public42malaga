/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   utils.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: jaidiaz- <jaidiaz-@student.42malaga.com    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/07/01 10:43:09 by jaidiaz-          #+#    #+#             */
/*   Updated: 2026/07/06 13:11:26 by jaidiaz-         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

long long	ft_atoll(const char *str, int *error)
{
	long long	res;
	int			i;

	res = 0;
	i = 0;
	if (!str || !str[i])
	{
		*error = 1;
		return (0);
	}
	while (str[i])
	{
		if (str[i] < '0' || str[i] > '9')
		{
			*error = 1;
			return (0);
		}
		res = (res * 10) + (str[i] - '0');
		i++;
	}
	return (res);
}

long long	get_time_ms(void)
{
	struct timeval	tv;

	if (gettimeofday(&tv, NULL) == -1)
		return (-1);
	return ((tv.tv_sec * 1000) + (tv.tv_usec / 1000));
}

void	ft_usleep(long long time_in_ms, t_data *data)
{
	long long	start;

	start = get_time_ms();
	while ((get_time_ms() - start) < time_in_ms)
	{
		pthread_mutex_lock(&data->stop_mutex);
		if (data->stop_simulation)
		{
			pthread_mutex_unlock(&data->stop_mutex);
			break ;
		}
		pthread_mutex_unlock(&data->stop_mutex);
		usleep(500);
	}
}

int	is_higher_priority(t_request a, t_request b)
{
	if (a.priority < b.priority)
		return (1);
	return (0);
}
