from diffusers.pipelines.stable_diffusion_xl.pipeline_stable_diffusion_xl import StableDiffusionXLPipeline
import torch

pipe = StableDiffusionXLPipeline.from_single_file(
    pretrained_model_link_or_path="D:/AI/stable-diffusion-webui/models/Stable-diffusion/dreamshaperXL10_alpha2Xl10.safetensors",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
)
pipe.to("cuda")
pipe.enable_xformers_memory_efficient_attention()
pipe.enable_model_cpu_offload()

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
images = pipe(prompt).images
for i, image in enumerate(images):
    image.save(f"{prompt}-of-{i}.png")
