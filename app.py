import streamlit as st
import requests
import base64
import os
from typing import Optional, Dict, Any
import json
import time

class StableDiffusionAPI:
    """Clase para manejar las interacciones con la API de Stable Diffusion."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:7860"):
        self.base_url = base_url
        self.default_params = {
            "steps": 30,
            "width": 512,
            "height": 512,
            "cfg_scale": 7,
            "sampler_index": "Euler a"
        }
    
    def generate_image(self, prompt: str, negative_prompt: str = "", **kwargs) -> Optional[str]:
        """
        Genera una imagen usando Stable Diffusion.
        
        Args:
            prompt: Descripción positiva de la imagen
            negative_prompt: Elementos a evitar en la imagen
            **kwargs: Parámetros adicionales de generación
        
        Returns:
            Optional[str]: Ruta de la imagen generada o None si hay error
        """
        payload = {**self.default_params, **kwargs}
        payload.update({
            "prompt": prompt,
            "negative_prompt": negative_prompt
        })
        
        try:
            response = requests.post(
                f"{self.base_url}/sdapi/v1/txt2img",  # Update the endpoint URL if necessary
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            image_data = result["images"][0]
            image_bytes = base64.b64decode(image_data)
            
            os.makedirs("generated_images", exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            image_path = f"generated_images/image_{timestamp}.png"
            
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            return image_path
            
        except Exception as e:
            st.error(f"Error en la generación: {str(e)}")
            return None

def load_config() -> Dict[Any, Any]:
    """Carga la configuración desde config.json."""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "default_negative_prompt": "ugly, deformed, noisy, blurry, low quality, cartoon, flat shading, watermark, text, logo, duplicates, out of frame",
            "prompts": {
                "Pueblos": "fantasy, medieval, village, town, city, architecture, buildings, houses, streets, market, people, shops, tavern, inn, castle, church, square, fountain, flowers, animals, pets, birds, sky, clouds",
                "Mazmorras": "Dark, underground, cave, High fantasy concept art, ultra-detailed environment. Dungeons and Dragons 5e, fantasy illustration, detailed, book style",
                "Paisajes": "landscape, oilpainting, drawn, ilustration, dungeons and dragons, detailed, nature, mountains, forest, river, lake, sky, clouds, calm, peaceful, serene, tranquil, quiet, beautiful, scenic, picturesque",
                "Retratos": "portrait, realistic, detailed, drawn, face, barroque, oil painting, Dungeons and Dragons 5e, fantasy illustration, detailed, book style",
                "Monstruos": "Dungeons and Dragons 5e, fantasy illustration, detailed, book style, high fantasy, dark"
            }
        }

def init_session_state():
    """Inicializa el estado de la sesión."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'advanced_options' not in st.session_state:
        st.session_state.advanced_options = False

def create_ui():
    """Configura la interfaz de usuario."""
    st.set_page_config(
        page_title="Generador de Imágenes Avanzado con SD",
        page_icon="🎨",
        layout="wide"
    )
    
    st.markdown("""
        <style>
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            background: linear-gradient(45deg, #FF4500, #FF8C00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 20px 0;
        }
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: #1E90FF;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #FF4500;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FF6347;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    init_session_state()
    create_ui()
    config = load_config()
    sd_api = StableDiffusionAPI()
    
    st.markdown("<h1 class='title'>Generador de Imágenes para juegos de rol con Stable Diffusion</h1>", unsafe_allow_html=True)
    
    # Área principal de entrada
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h2 class='subtitle'>Describe tu imagen ideal</h2>", unsafe_allow_html=True)
        
        # Selector de tipo de imagen
        image_type = st.selectbox(
            "Tipo de imagen",
            list(config["prompts"].keys()),
            help="Selecciona el tipo de imagen que deseas generar"
        )
        
        # Campo de descripción principal
        prompt = st.text_area(
            "Descripción detallada:",
            placeholder="Describe la imagen que deseas generar...",
            height=100
        )
        
        # Opciones avanzadas
        with st.expander("Opciones Avanzadas 🛠️"):
            st.session_state.advanced_options = True
            
            negative_prompt = st.text_area(
                "Prompt Negativo:",
                value=config["default_negative_prompt"],
                help="Describe elementos que NO deseas en la imagen"
            )
            
            col_adv1, col_adv2, col_adv3 = st.columns(3)
            
            with col_adv1:
                steps = st.slider("Pasos de generación", 20, 150, 30)
            with col_adv2:
                cfg_scale = st.slider("Escala CFG", 1.0, 20.0, 7.0)
            with col_adv3:
                seed = st.number_input("Seed", value=-1)
    
    with col2:
        image_path = "img/placeholder.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"Image file not found: {image_path}")
    
    # Botón de generación
    if st.button("🎨 Generar Imagen 🎨"):
        if not prompt:
            st.warning("Por favor, introduce una descripción para la imagen.")
            return
        
        with st.spinner("🔮 Generando tu obra maestra..."):
            # Construir el prompt final
            final_prompt = f"{prompt}, {config['prompts'][image_type]}"
            
            # Generar la imagen
            image_path = sd_api.generate_image(
                prompt=final_prompt,
                negative_prompt=negative_prompt,
                steps=steps if st.session_state.advanced_options else 30,
                cfg_scale=cfg_scale if st.session_state.advanced_options else 7.0,
                seed=seed if st.session_state.advanced_options else -1
            )
            
            if image_path:
                # Mostrar la imagen generada
                st.success("¡Imagen generada con éxito!")
                st.image(image_path, caption="Imagen Generada", width=400)  # Ajusta el ancho de la imagen
                
                # Guardar en el historial
                st.session_state.history.append({
                    "prompt": prompt,
                    "style": image_type,
                    "path": image_path,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
    # Historial de generaciones
    if st.session_state.history:
        with st.expander("Historial de Generaciones 📜"):
            for i, item in enumerate(reversed(st.session_state.history[-5:])):
                st.write(f"**{item['timestamp']}**")
                st.write(f"Prompt: {item['prompt']}")
                st.write(f"Estilo: {item['style']}")
                st.image(item['path'], width=200)  # Ajusta el ancho de las imágenes en el historial
                st.divider()

if __name__ == "__main__":
    main()