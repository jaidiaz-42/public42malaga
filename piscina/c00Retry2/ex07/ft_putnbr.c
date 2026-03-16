#include <unistd.h>

void	ft_putchar(char c)
{
	write (1, &c, 1);
}

void	ft_putnbr(int nb)
{
	ft_putchar(nb / 10 + '0');
	ft_putchar(nb % 10 + '0');
}
