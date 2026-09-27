import * as THREE from 'three';
import { WebGPURenderer } from 'three/examples/jsm/renderers/webgpu/WebGPURenderer.js';
import { 
    color, 
    uv, 
    sin, 
    atan, 
    mix, 
    mul, 
    sub, 
    uniform 
} from 'three/tsl';

// 1. Scene & WebGPU Renderer Setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 0, 4);

const renderer = new WebGPURenderer({ antialias: true });
await renderer.init(); // WebGPU requires asynchronous initialization
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

// 2. Define TSL Uniforms for dynamic color control
const uBaseColor = uniform(new THREE.Color(0x051c24));     // Midnight blue base
const uHighlightColor = uniform(new THREE.Color(0x40a9ff)); // Rayé highlight

// 3. Construct the TSL Procedural Sunburst Material Node Graph
const material = new THREE.MeshPhysicalNodeMaterial({
    metalness: 0.2,
    roughness: 0.1
});

// Center UVs from (0 to 1) to (-0.5 to 0.5)
const centeredUv = sub(uv(), 0.5);

// Calculate polar angle: atan(y, x)
const angle = atan(centeredUv.y, centeredUv.x);

// Generate high-frequency radial ray micro-grooves using sine waves
const sunburstPattern = sin(mul(angle, 180.0)).mul(0.5).add(0.5);

// Blend base color and highlight color based on the ray pattern
material.colorNode = mix(uBaseColor, uHighlightColor, sunburstPattern.mul(0.3));

// 4. Create Mesh & Add to Scene
const dialGeometry = new THREE.CylinderGeometry(1.0, 1.0, 0.02, 64);
const dialMesh = new THREE.Mesh(dialGeometry, material);
scene.add(dialMesh);

// 5. Render Loop
function animate() {
    requestAnimationFrame(animate);
    dialMesh.rotation.y += 0.005; // Rotate to watch the TSL sunburst highlights shift
    renderer.render(scene, camera);
}
animate();

// Handle Window Resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
