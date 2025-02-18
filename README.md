
@autores:

Tristán Del Rosal Aguirre

Natalie Pilkington González

# Streamlit App - Generación de Imágenes con Stable Diffusion

![](https://github.com/tristandelrosal/SD_webui/blob/main/img/placeholder.png?raw=true)

## Descripción

Esta aplicación desarrollada en **Streamlit** se conecta con la **API de Stable Diffusion Web UI** para generar imágenes a partir de descripciones en lenguaje natural. 
Utiliza el modelo "**Realistic Vision V6.0 B1**" de **Civit.ai**, optimizado mediante **prompt engineering** para crear imágenes detalladas y realistas.

### Características principales:
- **Generación de imágenes** a partir de descripciones personalizadas proporcionadas por el usuario.
- **Integración con Stable Diffusion** a través de la API.
- **Modelo personalizado**: Realistic Vision V6.0 B1, con ajustes específicos para mejorar la calidad y precisión de las imágenes.
- **Prompt optimizado** para crear una imagen de un dragón rojo colosal en el estilo de *Dungeons & Dragons 5e*.

### Prompt utilizado:
```
A colossal red dragon in Dungeon & Dragons 5e style, perched atop a ruined tower, with glowing eyes and smoke rising from its nostrils,
painterly fantasy illustration, rich detail
```

## Requisitos previos

- Python 3.10
- Stable Diffusion Web UI (clonado desde el repositorio oficial de GitHub)
- Streamlit

## Instalación y Configuración

1. **Clonar el repositorio de Stable Diffusion:**
   ```bash
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   cd stable-diffusion-webui
   ```

2. **Ejecutar Stable Diffusion con la API habilitada:**
   En el entorno local, ejecuta el siguiente comando:
   ```bash
   webui-user.bat --api
   ```

3. **Cargar el modelo Realistic Vision V6.0 B1:**
   - Descarga el modelo desde [Civit.ai](https://civit.ai/models)
   - Coloca el archivo del modelo en la carpeta `models/Stable-diffusion` dentro del directorio de Stable Diffusion.
   - También puedes cargar el modelo directamente en la interfaz gráfica de Stable Difussion:
   - Copia la url del modelo en civit.ai y pega el enlace en Stable Diffusion webui -> extensions -> civitai helper -> download

4. **Configurar y ejecutar la aplicación de Streamlit:**
   Desde una terminal diferente a donde se está ejecutando Stable Difussion webui, clona el el repositorio de este proyecto.    
   Asegúrate de estar en el directorio adecuado donde se encuentra `app.py`. Luego instala las dependencias y ejecuta la aplicación:

   ```bash
   git clone https://github.com/tristandelrosal/SD_webui/
   cd SD_webui
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Uso de la Aplicación

1. **Acceso a la interfaz**: Una vez ejecutada la aplicación, accede a través del navegador en la dirección:
   ```
   http://localhost:8501
   ```

2. **Generar imágenes**: Ingresa una descripción en lenguaje natural (prompt) y la aplicación generará una imagen utilizando el modelo Realistic Vision V6.0 B1.

### Ejemplo de uso de la app con capturas de pantalla ### 

**Descibe tu imagen ideal**

![Principal](https://github.com/tristandelrosal/SD_webui/blob/main/screenshots/captura1.png?raw=true)

**Imagen generada con éxito**

![Imagen generada](https://github.com/tristandelrosal/SD_webui/blob/main/screenshots/captura2.png?raw=true)

**Historial de generaciones**

![Historial de generaciones](https://github.com/tristandelrosal/SD_webui/blob/main/screenshots/captura3.png?raw=true
)


## Notas adicionales

- Es importante asegurarse de que Stable Diffusion Web UI esté ejecutándose con la opción `--api` para permitir la comunicación con la aplicación de Streamlit.
- El modelo "Realistic Vision V6.0 B1" está optimizado para generar ilustraciones detalladas de estilo fantástico.

## Créditos

- **Stable Diffusion Web UI**: [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- **Modelo Realistic Vision V6.0 B1**: Disponible en [Civit.ai](https://civit.ai)
- **Desarrollado con Streamlit**: [Streamlit.io](https://streamlit.io)

