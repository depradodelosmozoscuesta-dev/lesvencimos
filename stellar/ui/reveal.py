"""Animación de revelado: fade-in del texto con parpadeo de partículas doradas."""
import random


def reveal_frames(text, steps=20, seed=0):
    rng = random.Random(seed)
    for i in range(1, steps + 1):
        alpha = i / steps
        shown = text[: max(1, round(len(text) * alpha))]
        particles = [(rng.random(), rng.random()) for _ in range(int(10 * (1 - alpha)))]
        yield {"alpha": alpha, "text": shown, "particles": particles}
