#include <unistd.h>
#include <fcntl.h>
#include <unistd.h>
#define BUFFER_SIZE 1024

int	ft_process_file(char *name)
{
	int		file;
	int		bytes_read;	
	char	buffer[BUFFER_SIZE];

	file = open(name, O_RDONLY);
	if (file == -1)
		return (1);
	bytes_read = read(file, buffer, BUFFER_SIZE);
	while (bytes_read > 0)
	{
		write(1, &buffer, bytes_read);
		bytes_read = read(file, buffer, BUFFER_SIZE);
	}
	close(file);
	return (0);
}

int	main(int argc, char *argv[])
{
	if (argc < 2)
		write(1, "File name missing.\n", 19);
	else if (argc > 2)
		write(1, "Too many arguments.\n", 20);
	else if (ft_process_file(argv[1]) == 1)
		write(1, "Cannot read file.\n", 18);
	return (0);
}