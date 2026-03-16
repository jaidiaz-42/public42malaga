# *This project has been created as part of the 42 curriculum by jaidiaz-*

## Born2beroot

### Description
Born2beroot es un proyecto de la escuela 42 cuyo objetivo es aprender a configurar y administrar una máquina virtual desde cero, aplicando buenas prácticas de seguridad y gestión de usuarios.  
El proyecto consiste en instalar y configurar un sistema operativo Linux (Debian), aplicar políticas de seguridad estrictas, gestionar usuarios y grupos, y habilitar servicios básicos como SSH y firewall.  
Además, se requiere documentar las decisiones técnicas tomadas y comparar diferentes herramientas y sistemas.

### Instructions
1. **Instalación de la máquina virtual**  
   - Utilizar **VirtualBox** para crear la VM.  
   - Asignar los recursos mínimos requeridos (CPU, RAM, disco).  
   - Configurar el particionado del disco siguiendo los requisitos del bonus.  

2. **Configuración del sistema**  
   - Instalar **Debian** como sistema operativo.  
   - Configurar usuarios y grupos: `sudo` y `user42`.  
   - Aplicar las políticas de seguridad estrictas solicitadas en el subject (contraseñas seguras, sudo limitado, etc.).  
   - Instalar y configurar servicios requeridos: SSH, firewall, sudo.  

3. **Ejecución**  
   - Iniciar la máquina virtual desde VirtualBox.  
   - Conectarse vía SSH usando el usuario configurado.  
   - Verificar que las políticas de seguridad y servicios estén activos.  

### Project Design Choices
- **Sistema operativo elegido:** Debian  
  - Pros: estable, ampliamente documentado, gran comunidad.  
  - Contras: versiones de paquetes menos recientes comparadas con otras distros.  

- **Particionado del disco:** realizado según los requisitos del bonus, asegurando separación de directorios críticos.  
- **Políticas de seguridad:** contraseñas fuertes, configuración estricta de sudo, firewall activo.  
- **Usuarios y grupos:** creación de `user42` y asignación al grupo `sudo`.  
- **Servicios instalados:** SSH, firewall, sudo, y demás requeridos por el subject.  

### Comparisons
- **Debian vs Rocky Linux:** Debian es más estable y popular; Rocky es más cercano a entornos empresariales.  
- **AppArmor vs SELinux:** AppArmor es más sencillo de configurar; SELinux ofrece mayor granularidad.  
- **UFW vs firewalld:** UFW es más fácil de usar; firewalld es más flexible y potente.  
- **VirtualBox vs UTM:** VirtualBox es multiplataforma y más usado; UTM es más integrado en macOS.  

### Resources
- Guía utilizada para preparar la máquina virtual.  
- [Debian Documentation](https://www.debian.org/doc/)  
- [VirtualBox User Manual](https://www.virtualbox.org/manual/)    
- [Gitbook 42](https://42-cursus.gitbook.io/guide)

#### Uso de IA
La IA se utilizó para:  
- Estructurar el README.md.  
- Resumir comparaciones técnicas de manera clara y concisa.  
- Organizar la información en secciones coherentes y fáciles de leer.  

---
