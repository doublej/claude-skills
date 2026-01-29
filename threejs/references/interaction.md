# Interaction and Picking

## Raycasting

```ts
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

canvas.addEventListener("pointermove", (e) => {
  pointer.x = (e.offsetX / canvas.clientWidth) * 2 - 1;
  pointer.y = -(e.offsetY / canvas.clientHeight) * 2 + 1;
});

canvas.addEventListener("click", () => {
  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(scene.children, true);
  if (hits.length > 0) {
    console.log("Clicked:", hits[0].object.name);
    console.log("Point:", hits[0].point);
    console.log("Face:", hits[0].face);
  }
});
```

## Raycaster Options

```ts
raycaster.near = 0;              // Start distance
raycaster.far = Infinity;        // Max distance
raycaster.layers.set(1);         // Only intersect specific layers

// For points/lines
raycaster.params.Points.threshold = 0.1;
raycaster.params.Line.threshold = 0.1;
```

## Hover State

```ts
let hovered: THREE.Object3D | null = null;

function onPointerMove(e: PointerEvent) {
  pointer.x = (e.offsetX / canvas.clientWidth) * 2 - 1;
  pointer.y = -(e.offsetY / canvas.clientHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(interactiveObjects);

  if (hits.length > 0) {
    const obj = hits[0].object;
    if (hovered !== obj) {
      if (hovered) onPointerLeave(hovered);
      hovered = obj;
      onPointerEnter(obj);
    }
  } else if (hovered) {
    onPointerLeave(hovered);
    hovered = null;
  }
}

function onPointerEnter(obj: THREE.Object3D) {
  canvas.style.cursor = "pointer";
  (obj as THREE.Mesh).material.emissive?.setHex(0x333333);
}

function onPointerLeave(obj: THREE.Object3D) {
  canvas.style.cursor = "default";
  (obj as THREE.Mesh).material.emissive?.setHex(0x000000);
}
```

## GPU Picking

For large numbers of objects, render to offscreen buffer with object IDs:

```ts
const pickingScene = new THREE.Scene();
const pickingTexture = new THREE.WebGLRenderTarget(1, 1);
const pixelBuffer = new Uint8Array(4);

const idToObject = new Map<number, THREE.Object3D>();

// Create picking materials
scene.traverse((obj) => {
  if (obj.isMesh) {
    const id = obj.id;
    const pickingMaterial = new THREE.MeshBasicMaterial({
      color: new THREE.Color(id)
    });
    const pickingMesh = new THREE.Mesh(obj.geometry, pickingMaterial);
    pickingMesh.matrixAutoUpdate = false;
    pickingScene.add(pickingMesh);
    idToObject.set(id, obj);
  }
});

function pick(x: number, y: number) {
  camera.setViewOffset(
    canvas.clientWidth, canvas.clientHeight,
    x, y, 1, 1
  );

  renderer.setRenderTarget(pickingTexture);
  renderer.render(pickingScene, camera);
  renderer.setRenderTarget(null);
  camera.clearViewOffset();

  renderer.readRenderTargetPixels(pickingTexture, 0, 0, 1, 1, pixelBuffer);
  const id = (pixelBuffer[0] << 16) | (pixelBuffer[1] << 8) | pixelBuffer[2];

  return idToObject.get(id) || null;
}
```

## Orbit Controls

```ts
import { OrbitControls } from "three/addons/controls/OrbitControls.js";

const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 2;
controls.maxDistance = 50;
controls.maxPolarAngle = Math.PI / 2;  // Prevent going below ground

// In render loop
controls.update();
```

## Fly Controls

```ts
import { FlyControls } from "three/addons/controls/FlyControls.js";

const controls = new FlyControls(camera, canvas);
controls.movementSpeed = 10;
controls.rollSpeed = 0.5;
controls.dragToLook = true;

// In render loop
controls.update(delta);
```

## Pointer Lock

```ts
import { PointerLockControls } from "three/addons/controls/PointerLockControls.js";

const controls = new PointerLockControls(camera, canvas);

canvas.addEventListener("click", () => controls.lock());
controls.addEventListener("lock", () => console.log("Locked"));
controls.addEventListener("unlock", () => console.log("Unlocked"));

// Movement
const velocity = new THREE.Vector3();
const direction = new THREE.Vector3();
let moveForward = false, moveBackward = false;

document.addEventListener("keydown", (e) => {
  if (e.code === "KeyW") moveForward = true;
  if (e.code === "KeyS") moveBackward = true;
});

// In render loop
if (controls.isLocked) {
  direction.z = Number(moveForward) - Number(moveBackward);
  direction.normalize();
  velocity.z -= direction.z * 400 * delta;
  controls.moveForward(-velocity.z * delta);
}
```

## Drag and Drop

```ts
import { DragControls } from "three/addons/controls/DragControls.js";

const controls = new DragControls(draggableObjects, camera, canvas);

controls.addEventListener("dragstart", (e) => {
  orbitControls.enabled = false;
  e.object.material.emissive.setHex(0xaaaaaa);
});

controls.addEventListener("dragend", (e) => {
  orbitControls.enabled = true;
  e.object.material.emissive.setHex(0x000000);
});

controls.addEventListener("drag", (e) => {
  // Constrain to plane
  e.object.position.y = 0;
});
```

## Transform Controls

```ts
import { TransformControls } from "three/addons/controls/TransformControls.js";

const transformControls = new TransformControls(camera, canvas);
scene.add(transformControls);

transformControls.attach(selectedObject);
transformControls.setMode("translate"); // "translate" | "rotate" | "scale"
transformControls.setSpace("world");     // "world" | "local"

transformControls.addEventListener("dragging-changed", (e) => {
  orbitControls.enabled = !e.value;
});
```
