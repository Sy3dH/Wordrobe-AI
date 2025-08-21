FULL_BODY_GENERATION_PROMPT = """
**Subject**:
Generate a full-body image of the subject based on the provided face image. The face must remain unchanged; 
same identity, same facial structure, same expression, same hairstyle, and same skin tone. 
Only extend the body naturally to create a complete figure. The subject should be standing in a neutral A-pose 
(upright, arms slightly away from the sides, feet shoulder-width apart). 
Body proportions must be realistic and consistent with the face.

**Camera**:
Create a highly photorealistic studio-style full-body portrait, 
captured with a professional full-frame DSLR or mirrorless camera. 
Use an 85mm prime lens at f/8, simulating a catalog or fashion photography setup.
The framing should include the entire body from head to toe, centered in the frame, 
with accurate perspective and no cropping of limbs.

**Background**:
The background should be a plain white seamless studio backdrop, evenly lit. 
Lighting should be soft and diffused, replicating a professional studio setup. 
Subtle, natural shadows should fall behind and beneath the subject to ground them realistically.

**Realism**:
The image must replicate real-world photography, including:
- Accurate anatomy, fabric folds, skin textures.
- Natural shadows, highlights, and light falloff.
- Subtle lens imperfections and mild photographic grain.
- No smoothing, distortions, or artificial symmetry.
"""