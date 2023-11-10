
from sam.core.image_providers.base import ImageInputInterface
from sam.core.image_providers.novita import NovitaImageModel
from sam.core.image_providers.openai import OpenAIImageModel
from sam.core.image_providers.segmind import SegmindImageModel
from sam.core.image_providers.together import TogetherImageModel


# res = OpenAIImageModel().txt2img(ImageInputInterface(
#     "a white siamese cat",
#     api_key="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",
#     model="dall-e-3",
#     quality="standard",
#     n=1,
# ))

# res = TogetherImageModel().txt2img(ImageInputInterface(
#     prompt="a white siamese cat",
#     model="dall-e-3",
#     quality="standard",
#     n=1,
# ))

# res = NovitaImageModel().txt2img(ImageInputInterface(
#     prompt = "A cyan haired man on vacation enjoying the local party scene  at dawn in Mos Eisley on the planet Tatooine in Star Wars , a look of terror scared horrified , futuristic Neon cyberpunk synthwave cybernetic  Robert Hagan and by Naoko Takeuchi",
#     negative_prompt = "(nsfw nudity naked nipples:1.3)",
#     model = "dynavisionXLAllInOneStylized_release0534bakedvae_129001.safetensors",
#     sampler_name="DPM++ 2M Karras",
#     n = 1,
#     steps = 20,
#     cfg = 7,
#     seed = 3223553976,
#     size="512x512",
#     api_key="d734a50e-0fc4-4de0-8b9b-e2a6acafc302"
# ))

# res = NovitaImageModel().get_image_task_id(
#     "6de6ab39-f70b-4c7a-909a-cf9481aef2e1", "d734a50e-0fc4-4de0-8b9b-e2a6acafc302")

# res = NovitaImageModel().search_models(
#     "dyna", "d734a50e-0fc4-4de0-8b9b-e2a6acafc302")

# res = NovitaImageModel().upscale_image(
#     "C:/Users/moham/Downloads/Nibor_AAXX.jfif")

# res = NovitaImageModel().img2img(ImageInputInterface(
#     prompt = "gradient flat color (art by Andy Kehoe,) 1girl , shadows glowing particles night MOON translucent, cyan wolf spirits",
#     negative_prompt = "(nsfw nudity naked nipples:1.3)",
#     model = "dynavisionXLAllInOneStylized_release0534bakedvae_129001.safetensors",
#     sampler_name = "Euler a",
#     n = 1,
#     steps = 30,
#     cfg = 7,
#     seed = 3223553976,
#     size="1024x1024",
#     api_key="d734a50e-0fc4-4de0-8b9b-e2a6acafc302",
# ), ["C:/Users/moham/Downloads/Nibor_AAXX.jfif"])

# res = SegmindImageModel().txt2img(ImageInputInterface(
#     prompt = "gradient flat color (art by Andy Kehoe,) 1girl , shadows glowing particles night MOON translucent, cyan wolf spirits",
#     negative_prompt = "(nsfw nudity naked nipples:1.3)",
#     model = "ssd-1b",
#     sampler_name = "UniPC",
#     n = 1,
#     steps = 30,
#     cfg = 7,
#     seed = 3223553976,
#     size="1024x1024",
#     api_key="SG_5841213d9381b9be",
# ))

# print(res)