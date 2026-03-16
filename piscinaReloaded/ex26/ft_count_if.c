int	ft_count_if(char **tab, int (*f)(char*))
{
	int	i;
	int	cont;

	i = 0;
	cont = 0;
	while (tab[i] != 0)
	{
		if (f(tab[i]) == 1)
			cont++;
		i++;
	}
	return (cont);
}