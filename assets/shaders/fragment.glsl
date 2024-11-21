#version 330 core

in vec3 fragPos;
in vec3 normal;

uniform vec3 lightPos;
uniform vec3 lightColor;
uniform vec3 objectColor;

out vec4 FragColor;

float random(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233)))*43758.5453);
}

vec3 monte_carlo_GI(vec3 fragPos, vec3 normal) {
    int samples = 64; // Aumenta para mayor precisión
    vec3 indirectLight = vec3(0.0);

    for (int i = 0; i < samples; i++) {
        // Generar una dirección aleatoria
        vec3 randomDir = normalize(vec3(
            random(vec2(i, fragPos.x)),
            random(vec2(i, fragPos.y)),
            random(vec2(i, fragPos.z))
        ));

        if (dot(randomDir, normal) > 0.0) {
            // Calcula la contribución de la luz en esa dirección
            float cosTheta = max(dot(randomDir, normal), 0.0);
            indirectLight += lightColor * cosTheta / float(samples);
        }
    }
    return indirectLight;
}

void main() {
    vec3 lightDir = normalize(lightPos - fragPos);

    float diff = max(dot(normal, lightDir), 0.0);

    vec3 directLight = diff * lightColor;

    vec3 indirectLight = monte_carlo_GI(fragPos, normal);

    vec3 lighting = (directLight + indirectLight) * objectColor;

    FragColor = vec4(lighting, 1.0);
}