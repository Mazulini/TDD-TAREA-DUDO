# 🎲 Simulador del Juego Dudo Chileno

Simulación virtual del juego tradicional chileno "Dudo". La implementación está realizada en el lenguaje de programación Python e incluye la lógica del juego junto con tests que verifican su correcto funcionamiento.

## 📖 Contexto
El Dudo es un juego tradicional chileno que se juega con dados en "cachos".
El reglamento completo del juego se encuentra en el archivo reglas.txt, incluido en el proyecto en la ruta "...\TDD-TAREA-DUDO\reglas.txt".

### ⚙️ Instalación
1. Clona el repositorio en tu máquina local.

Para clonar el repositorio ejecute el siguiente comando (debe tener git instalado):
````
git clone https://github.com/Mazulini/TDD-TAREA-DUDO.git
````
2. Dirígete a la carpeta del repositorio desde la terminal. ("...\TDD-TAREA-DUDO")
3. Instala las dependencias usando el archivo "requirements.txt".

Para instalar los requerimientos use el siguente comando:
````
pip install -r requirements.txt
````
(se recomienda ejecutar el comando en un entorno virtual 🐍)

### 🧪 Ejecución de los tests
Para ejecutar los tests, después de instalar las dependencias con pip o equivalente, pueden usar:
```
pytest
o
python3 -m pytest
```

Para saber el detalle de la cobertura de los tests, pueden ejecutar:
```
pytest --cov=src --cov-report=term-missing
o
python3 -m pytest --cov=src --cov-report=term-missing
```

### 🟢 Badge de Estado
Estado actual del proyecto:
![CI Status](https://github.com/Mazulini/Tarea-Dudo-TDD/actions/workflows/ci.yml/badge.svg)

### 💻 Ejecutar Localmente

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest tests/ --cov=src --cov-report=term-missing

# Verificar formato del código
black --check src tests
isort --check-only src tests
flake8 src tests
```

### 🧑 Integrantes 
-Diego Ignacio Pérez Torres
-Matias Felipe Jener Valdebenito Valenzuela