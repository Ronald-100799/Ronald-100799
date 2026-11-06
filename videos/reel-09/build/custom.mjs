      import * as THREE from "./assets/three/three.module.min.js";
      const RED = new THREE.Color("#E10600"), WHITE = new THREE.Color("#f4f4f6");
      const clamp = (x) => Math.min(Math.max(x, 0), 1);
      const ease = (x) => 1 - Math.pow(1 - clamp(x), 3);
      const mat = (color, r = 0.45, m = 0.1) => new THREE.MeshStandardMaterial({ color, roughness: r, metalness: m });
      const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById("barsCv"), alpha: true, antialias: true, preserveDrawingBuffer: true });
      renderer.setPixelRatio(1); renderer.setSize(900, 620, false); renderer.setClearColor(0, 0);
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(30, 900 / 620, 0.1, 50);
      camera.position.set(0, 1.4, 9.2); camera.lookAt(0, 0, 0);
      scene.add(new THREE.HemisphereLight(0xffffff, 0x200606, 1.5));
      const key = new THREE.DirectionalLight(0xfff3ea, 2.6); key.position.set(3, 4, 5); scene.add(key);
      const rim = new THREE.DirectionalLight(0xff4a3a, 2.0); rim.position.set(-4, 1, -4); scene.add(rim);
      // biceps thickness gain: internal focus +12.4% (red) vs external +6.9% (white)
      const g = new THREE.Group(); g.position.y = -1.7; scene.add(g);
      const base = new THREE.Mesh(new THREE.BoxGeometry(5.2, 0.05, 1.8), mat(WHITE, 0.6)); g.add(base);
      const bars = [[12.4, RED, -1.25], [6.9, WHITE, 1.25]].map(([v, c, x]) => {
        const m = new THREE.Mesh(new THREE.BoxGeometry(1.5, 1, 1.5), mat(c)); m.position.x = x; m.userData.h = 3.3 * v / 12.4; m.userData.v = v; g.add(m); return m;
      });
      function renderAt(T) {
        const t = T - 37.2;
        if (t < -0.05 || t > 4.75) return;
        g.rotation.y = -0.28 + 0.05 * t; g.rotation.x = 0.1;
        bars.forEach((m, i) => {
          const k = ease((t - 0.7 - (1 - i) * 0.35) / 0.9);   // white first, red lands on "5.5%" (39.15)
          m.scale.y = Math.max(0.001, m.userData.h * k); m.position.y = m.scale.y / 2;
          const el = document.getElementById("cV" + i);
          if (el) el.textContent = "+" + (m.userData.v * k).toFixed(1) + "%";
        });
        renderer.render(scene, camera);
      }
      window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
      renderAt(window.__hfThreeTime || 0);
